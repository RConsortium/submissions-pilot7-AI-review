#!/usr/bin/env python3
"""Package harvesters shared with the submission-lineage toolkit (copied from build_manifest.py).

Merges two layers into one machine-readable graph:
  * declared  - what the sponsor states (declarations.yaml)
  * harvested - what the package itself shows: define.xml or a metacore-style
                spec workbook, XPT or Dataset-JSON datasets, ADaM and TLF
                R programs, helper code, the renv lockfile and PDFs

Works on both R Consortium Pilot 1 (XPT + define.xml) and Pilot 5
(Dataset-JSON + spec workbook, SDTM and ADaM programs).

Usage:
    python3 build_manifest.py PACKAGE_ROOT declarations.yaml -o lineage-manifest.json \
        [--dsjson-schema dataset.schema.json]

Requires: Python 3.10+, pandas, openpyxl, PyYAML, jsonschema (only with
--dsjson-schema) and poppler-utils (pdfinfo, pdftotext, pdfimages) on PATH.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd
import yaml

NS = {"odm": "http://www.cdisc.org/ns/odm/v1.3", "def": "http://www.cdisc.org/ns/def/v2.0"}
XLINK_HREF = "{http://www.w3.org/1999/xlink}href"
NOT_IN_ECTD = {"README.md", ".gitignore", "project.Rproj", "LICENSE", ".gitkeep"}
NUMERIC_TYPES = {"integer", "decimal", "float", "double"}
WRITE_CALLS = ("write_rtf", "writeLines", "pdf", "png", "ggsave", "saveRDS", "write.csv")
TITLE_CALLS = ("hf_line", "rtf_title", "basic_table", "draw_label", "ggtitle")
DATASET_WRITERS = ("write_dataset_json_with_metadata", "write_dataset_json", "write_xpt", "xportr_write")


# ----------------------------------------------------------------- helpers
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def strip_r_comments(code: str) -> str:
    """Remove R '#' comments, leaving '#' inside string literals alone (keeps line numbers)."""
    out = []
    for line in code.splitlines():
        buf, quote, i = [], None, 0
        while i < len(line):
            ch = line[i]
            if quote:
                buf.append(ch)
                if ch == "\\" and i + 1 < len(line):
                    buf.append(line[i + 1])
                    i += 1
                elif ch == quote:
                    quote = None
            elif ch in ("'", '"', "`"):
                quote = ch
                buf.append(ch)
            elif ch == "#":
                break
            else:
                buf.append(ch)
            i += 1
        out.append("".join(buf))
    return "\n".join(out)


def string_literals(code: str) -> list[str]:
    return [a or b for a, b in re.findall(r'"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'', code)]


def call_bodies(code: str, fn: str) -> list[tuple[str, int]]:
    """(argument text, 1-based line) for every call to `fn(` with balanced parentheses."""
    out = []
    for m in re.finditer(rf"(?<![\w.]){re.escape(fn)}\s*\(", code):
        depth, j = 1, m.end()
        while j < len(code) and depth:
            depth += {"(": 1, ")": -1}.get(code[j], 0)
            j += 1
        out.append((code[m.end(): j - 1], code.count("\n", 0, m.start()) + 1))
    return out


def upper_tokens(code: str) -> set[str]:
    return set(re.findall(r"\b[A-Z][A-Z0-9]{1,7}\b", code))


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


# ----------------------------------------------------------------- datasets
def _to_numeric(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.map(lambda v: v.strip() if isinstance(v, str) else v)
                          .replace({"NA": None, "": None}), errors="coerce")


def read_dataset(path: Path) -> tuple[pd.DataFrame, dict | None]:
    """Return (data, Dataset-JSON document or None). Numeric columns come back numeric."""
    if path.suffix.lower() == ".xpt":
        df = pd.read_sas(path, format="xport", encoding="latin-1")
        # pandas' IBM-float decoding can return ~5e-79 for an exact zero; snap it back.
        for c in df.select_dtypes("number").columns:
            df.loc[df[c].abs() < 1e-60, c] = 0.0
        return df, None
    doc = json.loads(path.read_text(encoding="utf-8"))
    cols = doc.get("columns", [])
    df = pd.DataFrame(doc.get("rows", []), columns=[c["name"] for c in cols])
    for c in cols:
        if c.get("dataType") in NUMERIC_TYPES:
            df[c["name"]] = _to_numeric(df[c["name"]])
    return df, doc


DECIMAL_LEXICAL = re.compile(r"^[+-]?(\d+(\.\d*)?|\.\d+)$")


def dsjson_conformance(doc: dict, schema: dict | None) -> dict:
    """Header validation against the CDISC schema plus value-encoding checks the schema cannot express."""
    header = {k: v for k, v in doc.items() if k != "rows"}
    schema_errors = []
    if schema is not None:
        import jsonschema
        v = jsonschema.Draft201909Validator(schema)
        schema_errors = sorted({f"{'/'.join(map(str, e.absolute_path)) or '(root)'}: {e.message}"
                                for e in v.iter_errors({**header, "rows": []})})
    issues: dict[str, dict] = {}

    def bump(col, kind, example):
        d = issues.setdefault(col, {})
        k = d.setdefault(kind, {"count": 0, "example": example})
        k["count"] += 1

    cols = doc.get("columns", [])
    rows = doc.get("rows", [])
    for j, c in enumerate(cols):
        dtype = c.get("dataType")
        for r in rows:
            v = r[j] if j < len(r) else None
            if v is None:
                continue
            if dtype in NUMERIC_TYPES and isinstance(v, str) and v.strip() in ("NA", "NaN", "."):
                bump(c["name"], "missing-as-string", v)
            elif dtype == "decimal":
                if not isinstance(v, str):
                    bump(c["name"], "decimal-not-string", v)
                elif v != v.strip():
                    bump(c["name"], "decimal-padded", v)
                elif not DECIMAL_LEXICAL.match(v):
                    bump(c["name"], "decimal-not-lexical", v)
            elif dtype == "integer" and (isinstance(v, (str, bool)) or (isinstance(v, float) and not v.is_integer())):
                bump(c["name"], "integer-not-integer", v)   # 63.0 is a valid JSON Schema integer
            elif dtype == "string" and not isinstance(v, str):
                bump(c["name"], "string-not-string", v)
        if dtype == "decimal" and c.get("targetDataType") != "decimal":
            issues.setdefault(c["name"], {})["decimal-without-targetDataType"] = {"count": 1, "example": None}
    return {
        "schemaErrors": schema_errors,
        "recordsMatchesRows": doc.get("records") == len(rows),
        "keyVariables": [c["name"] for c in sorted((c for c in cols if "keySequence" in c),
                                                    key=lambda c: c["keySequence"])],
        "valueIssues": issues,
    }


def harvest_dataset(path: Path, root: Path, schema: dict | None) -> dict:
    df, doc = read_dataset(path)
    small = {}
    for c in ("STUDYID", "PARAMCD", "DTYPE"):
        if c in df.columns:
            small[c] = sorted(str(v) for v in df[c].dropna().unique().tolist() if str(v).strip() != "")
    out = {
        "path": rel(path, root),
        "format": "xpt" if doc is None else "dataset-json",
        "role": "tabulation" if "tabulations" in path.parts else "analysis",
        "records": int(len(df)),
        "columns": list(df.columns),
        "distinctValues": small,
    }
    if doc is not None:
        out["header"] = {k: v for k, v in doc.items() if k not in ("rows", "columns")}
        out["columnMeta"] = [{k: c.get(k) for k in ("itemOID", "name", "dataType", "targetDataType", "keySequence")}
                             for c in doc.get("columns", [])]
        out["conformance"] = dsjson_conformance(doc, schema)
    return out


# ----------------------------------------------------------------- metadata
def harvest_define(path: Path, root: Path) -> dict:
    xml_root = ET.parse(path).getroot()
    raw = path.read_text(encoding="utf-8", errors="replace")
    study = xml_root.find("odm:Study", NS)
    mdv = study.find("odm:MetaDataVersion", NS)
    items = {i.get("OID"): i for i in mdv.findall("odm:ItemDef", NS)}
    methods = {m.get("OID"): m for m in mdv.findall("odm:MethodDef", NS)}
    codelists = {c.get("OID"): c for c in mdv.findall("odm:CodeList", NS)}

    def text_of(el):
        t = el.find("odm:Description/odm:TranslatedText", NS) if el is not None else None
        return " ".join((t.text or "").split()) if t is not None else None

    def cl_values(oid):
        c = codelists.get(oid)
        if c is None:
            return None
        return [e.get("CodedValue") for e in c.findall("odm:CodeListItem", NS)] + \
               [e.get("CodedValue") for e in c.findall("odm:EnumeratedItem", NS)]

    datasets = {}
    for ig in mdv.findall("odm:ItemGroupDef", NS):
        leaf = ig.find("def:leaf", NS)
        variables = {}
        for ref in ig.findall("odm:ItemRef", NS):
            it = items[ref.get("ItemOID")]
            origin = it.find("def:Origin", NS)
            cl = it.find("odm:CodeListRef", NS)
            moid = ref.get("MethodOID")
            variables[it.get("Name")] = {
                "itemOID": it.get("OID"), "label": text_of(it),
                "origin": origin.get("Type") if origin is not None else None,
                "methodOID": moid, "methodText": text_of(methods.get(moid)) if moid else None,
                "codelistOID": cl.get("CodeListOID") if cl is not None else None,
                "codelistValues": cl_values(cl.get("CodeListOID")) if cl is not None else None,
                "predecessor": None,
            }
        datasets[ig.get("Name")] = {"itemGroupOID": ig.get("OID"),
                                    "leaf": leaf.get(XLINK_HREF) if leaf is not None else None,
                                    "variables": variables}
    gv = study.find("odm:GlobalVariables", NS)
    return {
        "source": "define.xml", "path": rel(path, root), "oidsDeclared": True,
        "studyOID": study.get("OID"), "metaDataVersionOID": mdv.get("OID"),
        "studyName": gv.findtext("odm:StudyName", namespaces=NS),
        "hasAnalysisResultsMetadata": ("AnalysisResultDisplays" in raw) or ("/ns/arm/" in raw),
        "hasValueLevelMetadata": "ValueListDef" in raw,
        "sapReferences": [], "datasets": datasets,
    }


def harvest_spec_xlsx(path: Path, root: Path) -> dict:
    """Read a metacore/P21-style spec workbook into the same shape as harvest_define()."""
    x = pd.ExcelFile(path)
    sheet = lambda n: x.parse(n) if n in x.sheet_names else pd.DataFrame()  # noqa: E731
    attrs = dict(sheet("Define").values.tolist()) if "Define" in x.sheet_names else {}
    methods = {r.ID: " ".join(str(r.Description).split()) for r in sheet("Methods").itertuples()}
    comments = {r.ID: " ".join(str(r.Description).split()) for r in sheet("Comments").itertuples()}
    cl = sheet("Codelists")
    cl_values = cl.groupby("ID")["Term"].apply(lambda s: [str(v) for v in s]).to_dict() if len(cl) else {}
    nn = lambda v: None if pd.isna(v) else str(v).strip()  # noqa: E731
    datasets = {}
    for r in sheet("Datasets").to_dict("records"):
        keys = nn(r.get("Key Variables"))
        datasets[r["Dataset"]] = {"itemGroupOID": f"IG.{r['Dataset']}", "leaf": None, "variables": {},
                                  "keys": [k.strip() for k in keys.split(",")] if keys else []}
    for r in sheet("Variables").to_dict("records"):
        ds, var, meth, cid = r["Dataset"], r["Variable"], nn(r.get("Method")), nn(r.get("Codelist"))
        datasets.setdefault(ds, {"itemGroupOID": f"IG.{ds}", "leaf": None, "variables": {}})
        datasets[ds]["variables"][var] = {
            "itemOID": f"IT.{ds}.{var}", "label": nn(r.get("Label")), "origin": nn(r.get("Origin")),
            "methodOID": meth, "methodText": methods.get(meth) if meth else None,
            "codelistOID": cid, "codelistValues": cl_values.get(cid) if cid else None,
            "predecessor": nn(r.get("Predecessor")),
        }
    sap = [{"id": k, "text": v} for k, v in {**methods, **comments}.items() if re.search(r"\bSAP\b", v)]
    return {
        "source": "spec-xlsx", "path": rel(path, root), "oidsDeclared": False,
        "studyOID": None, "metaDataVersionOID": None,
        "studyName": attrs.get("StudyName"),
        "hasAnalysisResultsMetadata": len(sheet("Analysis Displays")) + len(sheet("Analysis Results")) > 0,
        "hasValueLevelMetadata": len(sheet("ValueLevel")) > 0,
        "sapReferences": sap, "datasets": datasets,
    }


# ----------------------------------------------------------------- code
def parse_functions(text: str) -> dict:
    """Top-level `name <- function` definitions in R source text."""
    defs = list(re.finditer(r"^(\w+)\s*<-\s*function", text, re.M))
    out = {}
    for k, d in enumerate(defs):
        end = defs[k + 1].start() if k + 1 < len(defs) else len(text)
        body = text[d.start(): end]
        out[d.group(1)] = {"upperTokens": sorted(upper_tokens(strip_r_comments(body))),
                           "namespaceCalls": sorted(set(re.findall(r"\b(\w+)::\w+", body)))}
    return out


def metadata_refs(lines: list[str], file: str) -> list[dict]:
    return [{"file": file, "line": n, "text": ln.strip().lstrip("#'").strip()}
            for n, ln in enumerate(lines, 1)
            if re.search(r"analysis results metadata|analysis define", ln, re.I)]


def harvest_pkglite(path: Path, root: Path) -> dict:
    blocks, cur = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Package: "):
            cur = {"package": line[9:].strip(), "file": None, "lines": []}
            blocks.append(cur)
        elif cur is not None and line.startswith("File: "):
            cur["file"] = line[6:].strip()
        elif cur is not None and (line.startswith("  ") or not line.strip()):
            cur["lines"].append(line[2:])
    pkg = {"name": None, "version": None, "path": rel(path, root), "imports": [], "exports": [],
           "functions": {}, "metadataReferences": []}
    for b in blocks:
        text = "\n".join(b["lines"])
        pkg["name"] = b["package"]
        if b["file"] == "DESCRIPTION":
            m = re.search(r"^Version:\s*(\S+)", text, re.M)
            pkg["version"] = m.group(1) if m else None
            m = re.search(r"^Imports:\s*(.*?)(?:^\S|\Z)", text, re.M | re.S)
            if m:
                pkg["imports"] = [s.strip().split(" ")[0] for s in m.group(1).split(",") if s.strip()]
        elif b["file"] == "NAMESPACE":
            pkg["exports"] = re.findall(r"^export\((\w+)\)", text, re.M)
        elif b["file"] and b["file"].startswith("R/"):
            pkg["functions"].update({k: {**v, "file": b["file"]} for k, v in parse_functions(text).items()})
            pkg["metadataReferences"] += metadata_refs(b["lines"], b["file"])
    return pkg


def harvest_helper_r(path: Path, root: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fns = parse_functions(text)
    return {"name": path.stem, "version": None, "path": rel(path, root), "imports": [],
            "exports": sorted(fns), "functions": {k: {**v, "file": path.name} for k, v in fns.items()},
            "metadataReferences": metadata_refs(text.splitlines(), path.name)}


def harvest_r_program(path: Path, root: Path, helper: dict) -> dict:
    code = path.read_text(encoding="utf-8")
    nc = strip_r_comments(code)
    lines = nc.splitlines()
    reads = re.findall(r"file\.path\(\s*path\$\w+\s*,\s*[\"']([^\"']+\.(?:json|xpt))[\"']", nc)
    created = set(re.findall(r"^\s*(\w+)\s*(?:<-|=)(?!=)", nc, re.M))
    via_list2env: set[str] = set()
    # dynamic list: c("dm", ...) mapped through paste0(.x, ".json")
    m = re.search(r"file\.path\(\s*path\$\w+\s*,\s*paste0\(\s*\.x\s*,\s*[\"']\.(json|xpt)[\"']\s*\)\s*\)", nc)
    if m:
        var = re.search(r"\bmap\(\s*(\w+)", nc)
        vec = re.search(rf"\b{var.group(1)}\s*<-\s*c\(([^)]*)\)", nc) if var else None
        if vec:
            names = re.findall(r"[\"'](\w+)[\"']", vec.group(1))
            reads += [f"{n}.{m.group(1)}" for n in names]
            if "list2env(" in nc:
                via_list2env |= set(names)
    if "list2env(" in nc:
        via_list2env |= set(re.findall(r"\b(\w+)\s*=\s*file\.path\(", nc))
    created |= via_list2env
    writes, dataset_writes = [], []
    for fn in WRITE_CALLS:
        for body, _ in call_bodies(nc, fn):
            writes += [Path(w).name for w in re.findall(r"file\.path\(\s*path\$output\s*,\s*[\"']([^\"']+)[\"']", body)]
    for fn in DATASET_WRITERS:
        for body, line in call_bodies(nc, fn):
            obj = body.split(",")[0].strip() or None
            name = next(iter(string_literals(body)), None)
            assigned_before = bool(obj) and any(
                re.match(rf"^\s*{re.escape(obj)}\s*(?:<-|=)(?!=)", ln) for ln in lines[: line - 1])
            dataset_writes.append({
                "function": fn, "line": line, "object": obj,
                "file": f"{name}.json" if name and fn.startswith("write_dataset_json") else name,
                "objectDefinedInProgram": assigned_before or obj in via_list2env,
                "objectUsedOnLines": [n for n, ln in enumerate(lines, 1) if obj and re.search(rf"\b{re.escape(obj)}\b", ln)],
            })
    titles = []
    for fn in TITLE_CALLS:
        for body, _ in call_bodies(nc, fn):
            titles += [s for s in string_literals(body)
                       if len(s) > 3 and not re.match(r"^(left|right|center|split|sans|bold|plain)$", s)]
    literals = string_literals(nc)
    filters = [{"variable": v, "op": "==", "value": val}
               for v, val in re.findall(r"\b([A-Z][A-Z0-9]{1,7})\s*==\s*[\"']([^\"']+)[\"']", nc)]
    filters += [{"variable": v, "op": "==", "value": float(val)}
                for v, val in re.findall(r"\b([A-Z][A-Z0-9]{1,7})\s*==\s*(-?\d+(?:\.\d+)?)\b", nc)]
    assignments = [{"variable": v, "expression": e.strip(), "line": nc.count("\n", 0, mm.start()) + 1}
                   for mm in re.finditer(r"(?<![=!<>])\b([A-Z][A-Z0-9]{1,7})\s*=\s*([A-Za-z_][\w.]*)\s*(?=[,)\n])", nc)
                   for v, e in [mm.groups()]]
    called = [f for f in helper["exports"] if re.search(rf"\b{f}\s*\(", nc)]
    return {
        "path": rel(path, root), "sha256": sha256(path),
        "kind": "adam" if dataset_writes else "tlf",
        "reads": sorted(set(reads)), "writes": sorted(set(writes)), "datasetWrites": dataset_writes,
        "objectsCreated": sorted(created),
        "libraries": sorted(set(re.findall(r"\blibrary\((\w+)\)", nc))),
        "namespaceCalls": sorted(set(re.findall(r"\b(\w+)::\w+", nc))),
        "helperFunctionsCalled": called,
        "titles": titles,
        "displayIdsInOutput": sorted(set(re.findall(r"\b(?:Table|Figure|Listing)\s+\d+-\d+(?:\.\d+)?", " ".join(literals)))),
        "selfReportedProgramName": sorted(set(n for s in literals for n in re.findall(r"Program:\s*([\w.\-]+)", s))),
        "filters": filters, "assignments": assignments,
        "upperTokens": sorted(upper_tokens(nc)),
    }


def harvest_lockfile(path: Path, root: Path) -> dict:
    lock = json.loads(path.read_text(encoding="utf-8"))
    return {"path": rel(path, root), "sha256": sha256(path), "r": lock.get("R", {}).get("Version"),
            "packages": {k: v.get("Version") for k, v in lock.get("Packages", {}).items()}}


def harvest_pdf(path: Path, root: Path) -> dict:
    pages = int(re.search(r"Pages:\s+(\d+)", run(["pdfinfo", str(path)])).group(1))
    images = run(["pdfimages", "-list", str(path)]).splitlines()[2:]
    per_page = []
    for p in range(1, pages + 1):
        text = run(["pdftotext", "-layout", "-f", str(p), "-l", str(p), str(path), "-"])
        per_page.append({"page": p, "textChars": len(text.strip()), "text": text,
                         "images": sum(1 for ln in images if ln.split() and ln.split()[0] == str(p))})
    return {"path": rel(path, root), "sha256": sha256(path), "pages": per_page}


# ----------------------------------------------------------------- results extraction
def extract_t1401(text: str) -> dict:
    """Pull Table 14-3.01 cells out of a PDF text layer (layout specific to this display)."""
    groups = ["Placebo", "Xanomeline Low Dose", "Xanomeline High Dose"]
    sec_map = {"Baseline": (0, "AVAL"), "Week 24": (24, "AVAL"), "Change from Baseline": (24, "CHG")}
    rows, cur, pairwise, dose, block = {}, None, [], None, None
    msd = r"-?\d+\.\d+ \(\s*-?\d+\.\d+\)"
    mrg = r"-?\d+\.\d+ \(\s*-?\d+;\s*-?\d+\)"
    for line in text.splitlines():
        s = line.strip()
        if s in sec_map:
            cur = sec_map[s]
            continue
        if cur and re.match(r"^n\s+\d", s):
            for g, v in zip(groups, re.findall(r"\d+", s)):
                rows.setdefault((cur, g), {})["n"] = v
        elif cur and s.startswith("Mean (SD)"):
            for g, v in zip(groups, re.findall(msd, s)):
                rows.setdefault((cur, g), {})["mean_sd"] = v
        elif cur and s.startswith("Median (Range)"):
            for g, v in zip(groups, re.findall(mrg, s)):
                rows.setdefault((cur, g), {})["median_range"] = v
        elif s.startswith("p-value(Dose Response)"):
            dose = re.findall(r"\d\.\d{3}", s)[-1]
            cur = None
        elif s.startswith("p-value(Xan - Placebo)"):
            ps = re.findall(r"\d\.\d{3}", s)
            block = [{"contrast": ["Xanomeline Low Dose", "Placebo"], "p": ps[0]},
                     {"contrast": ["Xanomeline High Dose", "Placebo"], "p": ps[1]}]
            pairwise += block
        elif s.startswith("p-value(Xan High - Xan Low)"):
            block = [{"contrast": ["Xanomeline High Dose", "Xanomeline Low Dose"], "p": re.findall(r"\d\.\d{3}", s)[-1]}]
            pairwise += block
        elif block and s.startswith("Diff of LS Means (SE)"):
            for b, v in zip(block, re.findall(r"-?\d+\.\d+ \(\d+\.\d+\)", s)):
                b["diff_se"] = v
        elif block and s.startswith("95% CI"):
            for b, v in zip(block, re.findall(r"\(-?\d+\.\d+;\s*-?\d+\.\d+\)", s)):
                b["ci"] = v
    desc = [{"visit": k[0][0], "variable": k[0][1], "group": k[1], **v} for k, v in rows.items()]
    return {"descriptive": desc, "doseResponse": dose, "pairwise": pairwise}


# ----------------------------------------------------------------- assembly
def build(root: Path, decl: dict, schema: dict | None) -> dict:
    files = []
    for p in sorted(root.rglob("*")):
        if p.is_file() and ".git" not in p.parts:
            files.append({"path": rel(p, root), "bytes": p.stat().st_size, "sha256": sha256(p),
                          "inEctdPackage": p.name not in NOT_IN_ECTD})
    paths = [root / f["path"] for f in files]

    define = next((p for p in paths if p.name == "define.xml"), None)
    spec = next((p for p in paths if p.suffix == ".xlsx"), None)
    metadata = harvest_define(define, root) if define else (harvest_spec_xlsx(spec, root) if spec else None)

    datasets = {}
    for p in paths:
        if p.suffix.lower() in (".xpt", ".json") and ("datasets" in p.parts):
            datasets[p.stem.upper()] = harvest_dataset(p, root, schema)

    pkglite = next((p for p in paths if p.name == "r0pkg.txt"), None)
    helper_r = next((p for p in paths if re.search(r"helper", p.name) and p.suffix.lower() == ".r"), None)
    helper = harvest_pkglite(pkglite, root) if pkglite else (harvest_helper_r(helper_r, root) if helper_r else
                                                             {"name": None, "version": None, "path": "", "imports": [],
                                                              "exports": [], "functions": {}, "metadataReferences": []})
    programs = {}
    for p in paths:
        if p.suffix.lower() == ".r" and p != helper_r:
            programs[p.name] = harvest_r_program(p, root, helper)
    for prog in programs.values():
        tokens = set(prog["upperTokens"])
        for fn in prog["helperFunctionsCalled"]:
            tokens |= set(helper["functions"].get(fn, {}).get("upperTokens", []))
        prog["variablesUsed"] = {Path(f).stem.upper(): sorted(tokens & set(datasets.get(Path(f).stem.upper(), {}).get("columns", [])))
                                 for f in prog["reads"]}

    lock = next((p for p in paths if p.name in ("renv.lock", "renv-lock.txt")), None)
    lockfile = harvest_lockfile(lock, root) if lock else None
    pdfs = {p.name: harvest_pdf(p, root) for p in paths if p.suffix.lower() == ".pdf"}

    # Reported values: transcribed (declared) or extracted from a text layer (harvested).
    rv = decl.get("reportedValues", {})
    if rv.get("source", {}).get("method") == "text-layer":
        doc = next(d for d in decl["documents"] if d["id"] == rv["source"]["doc"])
        page = pdfs[Path(doc["path"]).name]["pages"][rv["source"]["page"] - 1]["text"]
        ex = extract_t1401(page)
        rv["descriptive"]["rows"] = ex["descriptive"]
        rv["doseResponse"]["p"] = ex["doseResponse"]
        rv["pairwise"]["rows"] = ex["pairwise"]
        rv["source"]["extracted"] = True

    nodes, edges = [], []

    def node(id_, type_, basis, **kw):
        nodes.append({"id": id_, "type": type_, "basis": basis, **kw})

    def edge(src, typ, dst, basis, **kw):
        edges.append({"from": src, "type": typ, "to": dst, "basis": basis, **kw})

    sid = decl["study"]["id"]
    node(f"STUDY.{sid}", "Study", "declared", aliases=decl["study"].get("aliases", []))
    fidx = {f["path"]: f for f in files}
    for d in decl["documents"]:
        f = fidx.get(d.get("path") or "")
        node(d["id"], "Document", "declared", role=d["role"], path=d.get("path"),
             sha256=f["sha256"] if f else None, inPackage=bool(f), note=d.get("note"))
    for e in decl["endpoints"]:
        node(e["id"], "Endpoint", "declared", **{k: v for k, v in e.items() if k != "id"})
        edge(f"STUDY.{sid}", "hasEndpoint", e["id"], "declared")
    for e in decl["estimands"]:
        node(e["id"], "Estimand", "declared", **{k: v for k, v in e.items() if k != "id"})
        edge(e["endpoint"], "hasEstimand", e["id"], "declared")

    meta_doc = "DOC.METADATA"
    if metadata:
        node(meta_doc, "Document", "harvested", role=metadata["source"], path=metadata["path"],
             sha256=fidx[metadata["path"]]["sha256"], inPackage=True)
    for ds, h in datasets.items():
        node(f"DS.{ds}", "Dataset", "harvested", path=h["path"], format=h["format"], role=h["role"],
             sha256=fidx[h["path"]]["sha256"], records=h["records"],
             itemGroupOID=(h.get("header") or {}).get("itemGroupOID"))
        if metadata and ds in metadata["datasets"]:
            edge(f"DS.{ds}", "describedBy", meta_doc, "harvested", ref=metadata["datasets"][ds]["itemGroupOID"])

    seen_vars = set()

    def var_node(ds, var):
        vid = f"VAR.{ds}.{var}"
        if vid in seen_vars:
            return vid
        seen_vars.add(vid)
        if ds not in datasets and f"DS.{ds}" not in seen_vars:
            seen_vars.add(f"DS.{ds}")
            node(f"DS.{ds}", "Dataset", "declared", resolved=False,
                 note="Cited in documentation, but no dataset with this name is in the package.")
        meta = (metadata or {}).get("datasets", {}).get(ds, {}).get("variables", {}).get(var)
        node(vid, "Variable", "harvested", inMetadata=bool(meta),
             inData=var in datasets.get(ds, {}).get("columns", []),
             itemOID=meta["itemOID"] if meta else None, origin=meta["origin"] if meta else None,
             methodText=meta["methodText"] if meta else None)
        edge(vid, "partOf", f"DS.{ds}", "harvested")
        return vid

    if metadata:
        for ds, m in metadata["datasets"].items():
            for var, meta in m["variables"].items():
                if meta.get("predecessor") and "." in meta["predecessor"]:
                    pds, pvar = meta["predecessor"].split(".", 1)
                    edge(var_node(ds, var), "derivedFrom", var_node(pds.upper(), pvar), "harvested",
                         source=metadata["path"])

    if helper["name"]:
        node(f"PKG.{helper['name']}", "Package", "harvested", version=helper["version"], path=helper["path"])
        for fn in helper["exports"]:
            node(f"FN.{helper['name']}::{fn}", "Function", "harvested")
            edge(f"FN.{helper['name']}::{fn}", "definedIn", f"PKG.{helper['name']}", "harvested")

    for name, prog in programs.items():
        pid = f"PGM.{name}"
        node(pid, "Program", "harvested", path=prog["path"], sha256=prog["sha256"], kind=prog["kind"])
        for f in prog["reads"]:
            ds = Path(f).stem.upper()
            edge(pid, "reads", f"DS.{ds}", "harvested")
            for v in prog["variablesUsed"].get(ds, []):
                edge(pid, "usesVariable", var_node(ds, v), "harvested")
        for fn in prog["helperFunctionsCalled"]:
            edge(pid, "calls", f"FN.{helper['name']}::{fn}", "harvested")
        for w in prog["writes"]:
            node(f"FILE.{w}", "OutputFile", "harvested", name=w, inPackage=any(Path(f["path"]).name == w for f in files))
            edge(pid, "writes", f"FILE.{w}", "harvested")
        for w in prog["datasetWrites"]:
            if w["file"]:
                edge(pid, "writesDataset", f"DS.{Path(w['file']).stem.upper()}", "harvested",
                     object=w["object"], objectDefinedInProgram=w["objectDefinedInProgram"])

    for name, claim in decl.get("claimedInputs", {}).get("programs", {}).items():
        for qv in claim.get("variables", []) + claim.get("selectionVariables", []):
            ds, v = qv.split(".")
            edge(f"PGM.{name}", "claimsVariable", var_node(ds, v), "declared", source=decl["claimedInputs"]["source"])

    for a in decl["analyses"]:
        node(a["id"], "Analysis", "declared", **{k: v for k, v in a.items() if k != "id"})
        edge(a["estimand"], "analyzedBy", a["id"], "declared")
        edge(a["id"], "usesDataset", f"DS.{a['dataset']}", "declared")
        for v in list(a.get("analysisSet", {})) + list(a.get("dataSubset", {})):
            edge(a["id"], "selectsOn", var_node(a["dataset"], v), "declared")
        edge(a["id"], "implementedIn", f"PGM.{a['program']}", "declared")
        if a.get("implementation"):
            edge(a["id"], "implementedBy", f"FN.{a['implementation']}", "declared")
        edge(a["id"], "reportedIn", a["output"], "declared")
    for o in decl["outputs"]:
        node(o["id"], "Output", "declared", **{k: v for k, v in o.items() if k != "id"})
        edge(o["id"], "producedBy", f"PGM.{o['program']}", "declared")
        edge(o["id"], "renderedIn", o["renderedIn"]["doc"], "declared", page=o["renderedIn"]["page"])

    if rv:
        basis = "harvested" if rv["source"].get("extracted") else "declared"
        for r in rv["descriptive"]["rows"]:
            rid = f"RES.{rv['output']}.{r['variable']}.V{r['visit']}.{r['group'].replace(' ', '_')}"
            node(rid, "Result", basis, analysis=rv["descriptive"]["analysis"], **r)
            edge(rid, "fromAnalysis", rv["descriptive"]["analysis"], "declared")
            edge(rid, "displayedIn", rv["output"], basis, source=rv["source"])
        node(f"RES.{rv['output']}.DOSE", "Result", basis, analysis=rv["doseResponse"]["analysis"], p=rv["doseResponse"]["p"])
        edge(f"RES.{rv['output']}.DOSE", "fromAnalysis", rv["doseResponse"]["analysis"], "declared")
        for r in rv["pairwise"]["rows"]:
            rid = f"RES.{rv['output']}.PW." + "_vs_".join(x.replace(" ", "_") for x in r["contrast"])
            node(rid, "Result", basis, analysis=rv["pairwise"]["analysis"], **r)
            edge(rid, "fromAnalysis", rv["pairwise"]["analysis"], "declared")
            edge(rid, "displayedIn", rv["output"], basis, source=rv["source"])

    for p in pdfs.values():          # keep the manifest small: page text only for the TLF report
        tlf = next((d for d in decl["documents"] if d["id"] == "DOC.TLFREPORT"), {})
        if p["path"] != tlf.get("path"):
            for pg in p["pages"]:
                pg.pop("text", None)

    return {
        "lineageManifest": {"version": decl["manifestVersion"], "studyId": sid, "generator": "build_manifest.py",
                            "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")},
        "nodes": nodes, "edges": edges,
        "harvest": {"files": files, "metadata": metadata, "datasets": datasets, "programs": programs,
                    "helper": helper, "lockfile": lockfile, "pdfs": pdfs},
        "declarations": decl,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("package_root", type=Path)
    ap.add_argument("declarations", type=Path)
    ap.add_argument("-o", "--out", type=Path, default=Path("lineage-manifest.json"))
    ap.add_argument("--dsjson-schema", type=Path, help="CDISC Dataset-JSON schema (dataset.schema.json)")
    args = ap.parse_args()
    decl = yaml.safe_load(args.declarations.read_text(encoding="utf-8"))
    schema = json.loads(args.dsjson_schema.read_text(encoding="utf-8")) if args.dsjson_schema else None
    manifest = build(args.package_root.resolve(), decl, schema)
    args.out.write_text(json.dumps(manifest, indent=1, default=str), encoding="utf-8")
    print(f"Wrote {args.out} ({len(manifest['nodes'])} nodes, {len(manifest['edges'])} edges)")


if __name__ == "__main__":
    main()
