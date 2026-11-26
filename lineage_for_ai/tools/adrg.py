#!/usr/bin/env python3
"""adrg - create, sync, validate, trace and render an ADRG-JSON file (prototype v0.1).

    adrg init     plan.yaml -o adrg.json                 # day one: SAP + shells, no data
    adrg sync     adrg.json PACKAGE_ROOT -o adrg.json    # fill from metadata, data, programs, outputs
    adrg validate adrg.json [--package PACKAGE_ROOT]     # schema, references, readiness, staleness
    adrg trace    adrg.json CELL:T14-3.01.CHG.MEAN_SD.PBO
    adrg render   adrg.json -o adrg.pdf [--final]        # PHUSE-structured PDF; --final refuses open items
    adrg viewer   adrg.json -o adrg-viewer.html          # standalone trace explorer

Requires Python 3.10+, pandas, numpy, scipy, openpyxl, PyYAML, jsonschema, reportlab,
and poppler-utils (pdftotext etc.) for reading rendered outputs.
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

HERE = Path(__file__).resolve().parent
SCHEMA_DIR = HERE.parent / "schema" if (HERE.parent / "schema").is_dir() else HERE
sys.path.insert(0, str(HERE))
import adrg_core  # noqa: E402
import adrg_engine as eng  # noqa: E402
import lineage_harvest as hv  # noqa: E402

VERSION = "0.1.0"
STAGES = ["planned", "specified", "programmed", "executed", "final"]


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def gen(*src: str) -> dict:
    return {"kind": "generated", "from": [s for s in src if s], "by": "adrg sync", "date": now()}


def authored(by: str = "study team") -> dict:
    return {"kind": "authored", "by": by}


def merge(*dicts) -> dict:
    out: dict = {}
    for d in dicts:
        for k, v in (d or {}).items():
            if k == "where":
                out["where"] = {**out.get("where", {}), **v}
            else:
                out[k] = copy.deepcopy(v)
    return out


def ds_of(ref: str) -> str:
    return ref.split(":", 1)[1]


# =================================================================== init
def expand_display(d: dict) -> dict:
    short = ds_of(d["id"])
    cols = d.get("columns", [])
    out = {k: copy.deepcopy(d[k]) for k in ("id", "displayId", "type", "title", "subtitle", "population",
                                            "renderedIn", "footnotes") if k in d}
    out["columns"] = [{"id": c["id"], "label": c["label"]} for c in cols]
    out["sections"], used = [], []
    for sec in d.get("sections", []):
        scols = sec.get("columns") or cols
        so = {"id": sec["id"], "label": sec["label"], "rows": []}
        if sec.get("anchor"):
            so["anchor"] = sec["anchor"]
        if sec.get("columns"):
            so["columns"] = [{"id": c["id"], "label": c["label"]} for c in scols]
        for row in sec["rows"]:
            rcols = [c for c in scols if c["id"] in row["columns"]] if row.get("columns") else scols
            cells = []
            for c in rcols:
                comp = merge(sec.get("compute"), c.get("compute"), row.get("compute"))
                if "contrast" in comp:
                    comp["contrast"] = [comp.get("group") if x == "{group}" else x for x in comp["contrast"]]
                an = row.get("analysis") or c.get("analysis") or sec.get("analysis") or d.get("analysis")
                used.append(an)
                cells.append({"id": f"CELL:{short}.{sec['id']}.{row['id']}.{c['id']}", "column": c["id"],
                              "analysis": an, "compute": comp,
                              "format": row.get("format") or c.get("format") or sec.get("format"),
                              "result": {"value": None, "status": "planned", "source": None, "recomputed": None}})
            ro = {"id": row["id"], "label": row["label"], "cells": cells}
            for k in ("text", "anchor"):
                if k in row:
                    ro[k] = row[k]
            so["rows"].append(ro)
        out["sections"].append(so)
    out["analyses"] = sorted(set(used))
    out["status"] = "planned"
    return out


def program_kind(name: str) -> str:
    return "helper" if "helper" in name else ("tlf" if name.startswith("tlf") else "adam")


def cmd_init(plan: dict) -> dict:
    a = {"adrgJSONVersion": VERSION, "study": plan["study"],
         "lifecycle": {"stage": "planned", "history": [{"stage": "planned", "date": now(), "by": "adrg init",
                                                       "note": "Expanded from plan.yaml (SAP and table shells)."}]}}
    a["documents"] = plan.get("documents", [])
    a["standards"] = [{**s, "provenance": authored()} for s in plan.get("standards", [])]
    if "protocol" in plan:
        a["protocol"] = {**plan["protocol"], "provenance": authored()}
    a["estimands"] = plan.get("estimands", [])
    ac = plan.get("analysisConsiderations", {})
    a["analysisConsiderations"] = {"coreVariables": ac.get("coreVariables", []),
                                   "qa": [{**q, "provenance": authored()} for q in ac.get("qa", [])]}
    a["metadata"] = {"kind": "none", "sha256": None}
    a["datasets"] = [{"id": f"DS:{d['name']}", "role": "analysis", "status": "planned", "file": None,
                      "provenance": authored(), **d} for d in plan.get("datasets", [])]
    a["displays"] = [expand_display(d) for d in plan.get("displays", [])]
    anmap = {x["id"]: x for x in plan.get("analyses", [])}
    a["analyses"] = []
    for an in plan.get("analyses", []):
        cells = [c for d in a["displays"] for s in d["sections"] for r in s["rows"] for c in r["cells"] if c["analysis"] == an["id"]]
        vars_ = []
        for c in cells:
            vars_ += eng.variables_of(c, an)
        dsn = ds_of(an["dataset"])
        a["analyses"].append({**an, "status": "planned",
                              "variables": sorted({f"VAR:{dsn}.{v}" for v in vars_})})
    for d in a["displays"]:
        first = anmap.get(d["analyses"][0]) if d["analyses"] else None
        d["program"] = first.get("program") if first else None
    refs = {v for an in a["analyses"] for v in an["variables"]}
    refs |= {r for n in plan.get("notes", []) for r in n["about"] if r.startswith("VAR:")}
    refs |= {r for q in ac.get("qa", []) for r in q.get("about", []) if r.startswith("VAR:")}
    refs |= set(ac.get("coreVariables", []))
    a["variables"] = [{"id": r, "dataset": f"DS:{ds_of(r).split('.')[0]}", "name": ds_of(r).split(".")[1], "status": "planned"}
                      for r in sorted(refs)]
    a["parameters"] = [{"id": p, "dataset": f"DS:{ds_of(p).split('.')[0]}", "paramcd": ds_of(p).split(".")[1], "status": "planned"}
                       for p in sorted({p for an in a["analyses"] for p in an.get("parameters", [])})]
    progs = list(dict.fromkeys(plan.get("runInstructions", {}).get("order", []) +
                               [an["program"] for an in a["analyses"] if an.get("program")]))
    a["programs"] = [{"id": p, "path": ds_of(p), "kind": program_kind(ds_of(p)), "status": "planned"} for p in progs]
    a["environment"] = {"platform": {"claimed": plan.get("runInstructions", {}).get("platform", ""), "observed": []}}
    ri = plan.get("runInstructions", {})
    a["runInstructions"] = {"order": ri.get("order", []), "steps": ri.get("steps", []), "script": None,
                            "provenance": authored()}
    conf = plan.get("conformance")
    if conf:
        a["conformance"] = {**conf, "provenance": authored()}
    a["notes"] = [{**n, "provenance": authored()} for n in plan.get("notes", [])]
    a["findings"] = []
    return a


# =================================================================== sync helpers
def comment_stripped_lines(path: Path) -> tuple[list[str], list[str]]:
    raw = path.read_text(encoding="utf-8").splitlines()
    return raw, hv.strip_r_comments("\n".join(raw)).splitlines()


def anchors_in(path: Path, prog_id: str, var: str, limit: int = 3, lines_range: tuple[int, int] | None = None) -> list[dict]:
    raw, nc = comment_stripped_lines(path)
    hits = []
    for i, ln in enumerate(nc):
        if lines_range and not (lines_range[0] <= i + 1 <= lines_range[1]):
            continue
        if not re.search(rf"(?<![\w.$]){re.escape(var)}\b", ln):
            continue
        if re.search(rf"\b{re.escape(var)}\s*(=|<-)(?!=)", ln):
            role = "derives"
        elif re.search(rf"\b{re.escape(var)}\s*(==|!=|%in%|>=|<=)|filter|subset|is\.na\(\s*{re.escape(var)}", ln):
            role = "selects"
        else:
            role = "uses"
        hits.append({"program": prog_id, "line": i + 1, "excerpt": raw[i].strip()[:160], "role": role})
    order = {"derives": 0, "selects": 1, "uses": 2}
    return sorted(hits, key=lambda h: (order[h["role"]], h["line"]))[:limit]


def function_range(path: Path, fn: str) -> tuple[int, int] | None:
    text = path.read_text(encoding="utf-8").splitlines()
    starts = [i + 1 for i, ln in enumerate(text) if re.match(r"^\w+\s*<-\s*function", ln)]
    me = next((i + 1 for i, ln in enumerate(text) if re.match(rf"^{re.escape(fn)}\s*<-\s*function", ln)), None)
    if not me:
        return None
    nxt = next((s for s in starts if s > me), len(text) + 1)
    return me, nxt - 1


def claim_rate(T: pd.DataFrame, var: str, S: pd.DataFrame, sds: str, svar: str):
    seq = f"{sds}SEQ"
    keys = ["USUBJID", seq] if seq in T and seq in S else (["USUBJID"] if S["USUBJID"].is_unique else None)
    if not keys or var not in T or svar not in S:
        return None
    src = S[keys].copy()
    src["_S"] = S[svar]
    tgt = T[keys].copy()
    tgt["_T"] = T[var]
    mm = tgt.dropna(subset=["_T"]).merge(src, on=keys, how="inner")
    if not len(mm):
        return None
    if pd.api.types.is_numeric_dtype(mm["_T"]):
        eq = np.isclose(mm["_T"].astype(float), pd.to_numeric(mm["_S"], errors="coerce").astype(float))
    else:
        eq = mm["_T"].astype(str).str.strip() == mm["_S"].astype(str).str.strip()
    return int(eq.sum()), len(mm)


def read_value_level(spec: Path) -> list[dict]:
    x = pd.ExcelFile(spec)
    if "ValueLevel" not in x.sheet_names:
        return []
    methods = {r["ID"]: " ".join(str(r["Description"]).split()) for r in x.parse("Methods").to_dict("records")}
    out = []
    for r in x.parse("ValueLevel").to_dict("records"):
        m = re.match(r"(\w+)\s+EQ\s+(\S+)", str(r.get("Where Clause", "")))
        if m:
            meth = None if pd.isna(r.get("Method")) else str(r["Method"])
            out.append({"dataset": r["Dataset"], "variable": r["Variable"], "whereVar": m.group(1), "whereVal": m.group(2),
                        "label": None if pd.isna(r.get("Label")) else str(r["Label"]), "methodOID": meth,
                        "methodText": methods.get(meth) if meth else None,
                        "whereClause": str(r["Where Clause"]),
                        "predecessor": None if pd.isna(r.get("Predecessor")) else str(r["Predecessor"])})
    return out


# =================================================================== sync
def cmd_sync(a: dict, root: Path, dsjson_schema: dict | None) -> dict:
    a = copy.deepcopy(a)
    files = [p for p in sorted(root.rglob("*")) if p.is_file() and ".git" not in p.parts]
    rel = lambda p: p.relative_to(root).as_posix()  # noqa: E731
    by_rel = {rel(p): p for p in files}
    findings: list[dict] = []

    def finding(fid, severity, about, text, check=None):
        findings.append({"id": f"FND:{fid}", "severity": severity, "about": about, "text": text,
                         "check": check or fid.split(".")[0], "resolution": None})

    # ---- documents
    for d in a.get("documents", []):
        p = by_rel.get(d.get("path") or "")
        if p:
            d["sha256"], d["status"] = sha256(p), "present"
        elif d.get("status") != "external":
            d["status"] = "missing"
            if d["role"] in ("statistical-analysis-plan", "define-xml"):
                finding(f"DOC.{ds_of(d['id'])}", "warning", [d["id"]], f"{d['role']} is referenced but not in the package.")

    # ---- metadata
    define = next((p for p in files if p.name == "define.xml"), None)
    spec = next((p for p in files if p.suffix == ".xlsx"), None)
    md = hv.harvest_define(define, root) if define else (hv.harvest_spec_xlsx(spec, root) if spec else None)
    vlm = read_value_level(spec) if (spec and not define) else []
    if md:
        src = define or spec
        doc_id = next((d["id"] for d in a["documents"] if d.get("path") == rel(src)), None)
        a["metadata"] = {"source": doc_id, "kind": "define-xml" if define else "spec-xlsx", "sha256": sha256(src),
                         "snapshotTakenAt": now()}
    mds = (md or {}).get("datasets", {})

    # ---- datasets
    harvested = {}
    for p in files:
        if p.suffix.lower() in (".json", ".xpt") and "datasets" in p.parts:
            harvested[p.stem.upper()] = hv.harvest_dataset(p, root, dsjson_schema)
    plan_ds = {d["name"]: d for d in a.get("datasets", [])}
    helper_p = next((p for p in files if "helper" in p.name and p.suffix.lower() == ".r"), None)
    helper = hv.harvest_helper_r(helper_p, root) if helper_p else {"name": None, "exports": [], "functions": {}, "path": ""}
    progs_h = {p.name: hv.harvest_r_program(p, root, helper) for p in files if p.suffix.lower() == ".r" and p != helper_p}
    for prog in progs_h.values():
        tokens = set(prog["upperTokens"])
        for fn in prog["helperFunctionsCalled"]:
            tokens |= set(helper["functions"].get(fn, {}).get("upperTokens", []))
        prog["variablesUsed"] = {Path(f).stem.upper(): sorted(tokens & set(harvested.get(Path(f).stem.upper(), {}).get("columns", [])))
                                 for f in prog["reads"]}
    producer = {Path(w["file"]).stem.upper(): name for name, p in progs_h.items() for w in p["datasetWrites"] if w["file"]}
    new_ds = []
    for name, h in sorted(harvested.items(), key=lambda kv: (kv[1]["role"] != "analysis", kv[0])):
        base = plan_ds.get(name, {"id": f"DS:{name}", "name": name, "provenance": gen(h["path"])})
        hdr = h.get("header") or {}
        lab = hdr.get("label")
        ss = hdr.get("sourceSystem") or {}
        prod = producer.get(name)
        deps = sorted({f"DS:{Path(f).stem.upper()}" for f in progs_h[prod]["reads"]} - {f"DS:{name}"}) if prod else []
        new_ds.append({**base, "role": h["role"], "label": lab if isinstance(lab, str) else base.get("label"),
                       "file": {"path": h["path"], "format": h["format"], "sha256": sha256(root / h["path"]),
                                "records": h["records"], "createdAt": hdr.get("datasetJSONCreationDateTime"),
                                "sourceSystem": f"{ss.get('name')} {ss.get('version')}".strip() if ss else None},
                       "metadataRef": mds.get(name, {}).get("itemGroupOID"),
                       "dependsOn": deps, "producedBy": f"PGM:{prod}" if prod else None,
                       "status": "produced"})
        conf = h.get("conformance") or {}
        miss = {c: v["missing-as-string"]["count"] for c, v in conf.get("valueIssues", {}).items() if "missing-as-string" in v}
        if miss:
            top = ", ".join(f"{c} ({n})" for c, n in sorted(miss.items(), key=lambda kv: -kv[1])[:3])
            finding(f"DSJSON.NA.{name}", "error", [f"DS:{name}"],
                    f"{sum(miss.values()):,} missing values written as the string 'NA' instead of null: {top}.", "L18")
        if conf.get("schemaErrors"):
            finding(f"DSJSON.SCHEMA.{name}", "error", [f"DS:{name}"],
                    "Fails the CDISC Dataset-JSON v1.1 schema: " + "; ".join(e[:90] for e in conf["schemaErrors"][:2]), "L18")
    missing_planned = [d for n, d in plan_ds.items() if n not in harvested]
    a["datasets"] = new_ds + missing_planned
    refs = [d for d in new_ds if (harvested[d["name"]].get("header") or {})]
    unresolved = [d["id"] for d in refs if not by_rel.get((harvested[d["name"]]["header"].get("metaDataRef") or "").lstrip("./"))
                  and not any(rel(p).endswith("/" + Path(harvested[d["name"]]["header"].get("metaDataRef") or "?").name) for p in files)]
    if unresolved:
        finding("DSJSON.METADATAREF", "error", unresolved,
                f"{len(unresolved)} Dataset-JSON files have a metaDataRef that does not resolve to a file in the package.", "L17")

    # ---- programs
    tlf_pages = {}
    rep = next((d for d in a["documents"] if d["role"] == "tlf-report" and d["status"] == "present"), None)
    report_pdf = hv.harvest_pdf(by_rel[rep["path"]], root) if rep else None
    for disp in a["displays"]:
        if report_pdf and disp.get("renderedIn"):
            tlf_pages[disp["id"]] = report_pdf["pages"][disp["renderedIn"]["page"] - 1]["text"]
    prog_paths = {p.name: p for p in files if p.suffix.lower() == ".r"}
    plan_pg = {p["id"]: p for p in a.get("programs", [])}
    new_pg = []
    for name, p in sorted(prog_paths.items()):
        pid = f"PGM:{name}"
        h = progs_h.get(name)
        kind = "helper" if p == helper_p else (h["kind"] if h else "other")
        run = {"receipt": None, "mode": "unknown", "evidence": "No build receipt in the package."}
        if h and kind == "tlf":
            disp_ids = [d["id"] for d in a["displays"] if d.get("program") == pid]
            pages = [tlf_pages.get(i, "") for i in disp_ids]
            if any("<run interactively>" in t for t in pages):
                run = {"receipt": None, "mode": "interactive",
                       "evidence": "Rendered output says 'Source: <run interactively>'."}
                finding(f"RUN.{name}", "warning", [pid] + disp_ids,
                        f"{', '.join(d.split(':')[1] for d in disp_ids)} was produced in an interactive session, not by a scripted run of {name}.", "L10")
        writes = (h["writes"] if h else []) + [w["file"] for w in (h["datasetWrites"] if h else []) if w["file"]]
        new_pg.append({**plan_pg.get(pid, {}), "id": pid, "path": rel(p), "kind": kind, "sha256": sha256(p),
                       "reads": [f"DS:{Path(f).stem.upper()}" for f in (h["reads"] if h else [])],
                       "writes": sorted(set(writes)),
                       "calls": [f"FN:{Path(helper['path']).stem}.{fn}" for fn in (h["helperFunctionsCalled"] if h else [])],
                       "run": run, "status": "programmed", "provenance": gen(rel(p))})
        for w in (h["datasetWrites"] if h else []):
            if not w["objectDefinedInProgram"]:
                others = [n for n, q in progs_h.items() if n != name and w["object"] in q["objectsCreated"]]
                finding(f"WRITE.{name}", "error", [pid, f"DS:{Path(w['file']).stem.upper()}"],
                        f"{name} line {w['line']} writes `{w['object']}`, which it never creates (the dataset it builds is "
                        f"`{Path(w['file']).stem}`); only {', '.join(others) or 'no program'} creates `{w['object']}`. "
                        f"The submitted {w['file']} cannot be shown to come from this program.", "L20")
    a["programs"] = new_pg + [p for pid, p in plan_pg.items() if pid not in {x["id"] for x in new_pg}]
    finding("RECEIPTS", "warning", [p["id"] for p in new_pg if p["kind"] in ("adam", "tlf")],
            "No program has a build receipt (inputs, hashes, commit, session), so which run produced each file cannot be shown.", "L19")

    # ---- environment
    lock_p = next((p for p in files if p.name in ("renv.lock", "renv-lock.txt")), None)
    env = a.get("environment", {})
    observed = sorted({d["file"]["sourceSystem"] for d in new_ds if d["file"] and d["file"].get("sourceSystem")})
    env["platform"] = {"claimed": env.get("platform", {}).get("claimed", ""), "observed": observed}
    if lock_p:
        lock = hv.harvest_lockfile(lock_p, root)
        env["r"] = lock["r"]
        env["lockfile"] = {"path": rel(lock_p), "sha256": lock["sha256"]}
        used: dict[str, set] = {}
        for name, h in progs_h.items():
            for pk in set(h["libraries"]) | set(h["namespaceCalls"]):
                used.setdefault(pk, set()).add(f"PGM:{name}")
        for fn in helper["functions"].values():
            for pk in fn["namespaceCalls"]:
                used.setdefault(pk, set()).add(f"PGM:{helper_p.name}")
        env["packages"] = [{"name": k, "version": lock["packages"][k], "usedBy": sorted(v)}
                           for k, v in sorted(used.items(), key=lambda kv: kv[0].lower()) if k in lock["packages"]]
        env["provenance"] = gen(rel(lock_p))
    claimed = env["platform"]["claimed"]
    off = [d["id"] for d in new_ds if d["file"].get("sourceSystem") and claimed and claimed.lower() not in d["file"]["sourceSystem"].lower()]
    if off:
        finding("ENV.PLATFORM", "warning", off,
                f"Run instructions state {claimed}, but {len(off)} datasets declare another platform: "
                + "; ".join(sorted(set(d['file']['sourceSystem'] for d in new_ds if d['id'] in off))) + ".", "L19")
    a["environment"] = env

    # ---- parameters
    data = eng.Data(root, a["datasets"])
    for prm in a.get("parameters", []):
        dsn = ds_of(prm["dataset"])
        df = data.get(dsn)
        sub = df[df["PARAMCD"] == prm["paramcd"]] if "PARAMCD" in df else df.iloc[0:0]
        prm["param"] = str(sub["PARAM"].iloc[0]) if "PARAM" in sub and len(sub) else None
        v = next((x for x in vlm if x["dataset"] == dsn and x["whereVal"] == prm["paramcd"]), None)
        prm["derivation"] = ({"text": v["methodText"] or "", "methodOID": v["methodOID"], "whereClause": v["whereClause"]}
                             if v else None)
        prm["status"] = "produced" if len(sub) else "missing"
        prm["provenance"] = gen(a.get("metadata", {}).get("source") or "", ds_of(prm["dataset"]))
        if not v:
            finding(f"PARAM.NOVLM.{dsn}.{prm['paramcd']}", "info", [prm["id"]],
                    f"No value-level derivation for {dsn} {prm['paramcd']} in the metadata.", "L07")

    # ---- variables (traced set + predecessors, recursively)
    def resolve(dsn: str, name: str) -> str:
        """A variable named in an analysis lives in its dataset, or in ADSL when merged in for population/grouping."""
        if name in harvested.get(dsn, {}).get("columns", []):
            return f"VAR:{dsn}.{name}"
        if name in harvested.get("ADSL", {}).get("columns", []):
            return f"VAR:ADSL.{name}"
        return f"VAR:{dsn}.{name}"

    for an in a["analyses"]:
        dsn = ds_of(an["dataset"])
        cells = [c for d in a["displays"] for s in d["sections"] for r in s["rows"] for c in r["cells"] if c["analysis"] == an["id"]]
        names = []
        for c in cells:
            for v in eng.variables_of(c, an):
                pd_ = c["compute"].get("populationDataset")
                names.append(f"VAR:{pd_}.{v}" if pd_ and v == c["compute"].get("groupVariable") else resolve(dsn, v))
        an["variables"] = sorted(set(names))
    want = {v for an in a["analyses"] for v in an["variables"]}
    want |= {r for n in a.get("notes", []) for r in n["about"] if r.startswith("VAR:")}
    want |= {r for q in a.get("analysisConsiderations", {}).get("qa", []) for r in q.get("about", []) if r.startswith("VAR:")}
    want |= set(a.get("analysisConsiderations", {}).get("coreVariables", []))
    cited_by: dict[str, str] = {}
    for an in a["analyses"]:
        pg = progs_h.get(ds_of(an["program"])) if an.get("program") else None
        if pg:
            want |= {f"VAR:{ds_of(an['dataset'])}.{v}" for v in pg["variablesUsed"].get(ds_of(an["dataset"]), [])}
    for prm in a.get("parameters", []):
        want |= {f"VAR:{ds_of(prm['dataset'])}.PARAMCD", f"VAR:{ds_of(prm['dataset'])}.AVAL"}
    built: dict[str, dict] = {}
    queue = sorted(want)
    while queue:
        vid = queue.pop(0)
        if vid in built:
            continue
        dsn, var = ds_of(vid).split(".", 1)
        h = harvested.get(dsn)
        meta = mds.get(dsn, {}).get("variables", {}).get(var)
        col_label = next((c.get("label") for c in (h or {}).get("columnMeta", []) if c["name"] == var), None)
        preds = []
        if meta and meta.get("predecessor") and "." in meta["predecessor"]:
            pds, pv = meta["predecessor"].split(".", 1)
            preds.append(f"VAR:{pds.upper()}.{pv}")
        elif meta and meta.get("methodText") and re.match(r"^[A-Z][A-Z0-9]*\.[A-Z][A-Z0-9]*$", meta["methodText"]):
            pds, pv = meta["methodText"].split(".")
            if pds.upper() != dsn:
                preds.append(f"VAR:{pds.upper()}.{pv}")
        text = (meta or {}).get("methodText") or ""
        if not preds and text and not re.match(r"^[A-Z][A-Z0-9]*\.[A-Z][A-Z0-9]*$", text):
            # prose derivation: pick out DS.VAR references and same-dataset columns it names
            for sds, sv in re.findall(r"\b([A-Z][A-Z0-9]{1,7})\.([A-Z][A-Z0-9]{1,7})\b", text):
                if sv in harvested.get(sds, {}).get("columns", []):
                    preds.append(f"VAR:{sds}.{sv}")
            if not preds:
                cols = set((h or {}).get("columns", []))
                preds += [f"VAR:{dsn}.{t}" for t in re.findall(r"\b[A-Z][A-Z0-9]{1,7}\b", text) if t in cols and t != var]
        prod = producer.get(dsn)
        if not preds and prod:                                   # fall back to the code: VAR = SOURCECOL
            for asg in progs_h[prod]["assignments"]:
                if asg["variable"] == var:
                    for f in progs_h[prod]["reads"]:
                        src = Path(f).stem.upper()
                        if asg["expression"] in harvested.get(src, {}).get("columns", []) and src != dsn:
                            preds.append(f"VAR:{src}.{asg['expression']}")
                            break
                    if preds:
                        break
        preds = [p for p in dict.fromkeys(preds) if ds_of(p).split(".")[0] in harvested]
        anchors = []
        if prod:
            anchors += anchors_in(prog_paths[prod], f"PGM:{prod}", var)
        if h and h["role"] == "tabulation":
            for name, pg in progs_h.items():
                if pg["kind"] == "adam" and f"{dsn.lower()}.json" in pg["reads"]:
                    anchors += anchors_in(prog_paths[name], f"PGM:{name}", var, limit=2)
        for an in a["analyses"]:
            if an.get("program") and vid in an.get("variables", []):
                pn = ds_of(an["program"])
                if pn in prog_paths:
                    anchors += anchors_in(prog_paths[pn], an["program"], var, limit=2)
                impl = an.get("method", {}).get("implementation")
                if impl and helper_p:
                    rng = function_range(helper_p, impl.split(".")[-1])
                    anchors += anchors_in(helper_p, f"PGM:{helper_p.name}", var, limit=2, lines_range=rng)
        seen_a, uniq = set(), []
        for x in anchors:
            k = (x["program"], x["line"])
            if k not in seen_a:
                seen_a.add(k)
                uniq.append(x)
        built[vid] = {"id": vid, "dataset": f"DS:{dsn}", "name": var,
                      "label": (meta or {}).get("label") or (col_label if isinstance(col_label, str) else None),
                      "origin": (meta or {}).get("origin"),
                      "derivation": {"text": meta.get("methodText"), "methodOID": meta.get("methodOID")} if meta and meta.get("methodOID") else None,
                      "predecessors": preds, "codeAnchors": uniq[:6],
                      "inData": bool(h and var in h["columns"]), "inMetadata": bool(meta),
                      "status": "produced" if h and var in h["columns"] else "missing",
                      "provenance": gen(a.get("metadata", {}).get("source") or "", f"DS:{dsn}")}
        for p in preds:
            cited_by.setdefault(p, vid)
        queue += [p for p in preds if p not in built]
        # derivation claim vs data
        if meta and meta.get("methodText") and re.match(r"^[A-Z][A-Z0-9]*\.[A-Z][A-Z0-9]*$", meta["methodText"]):
            sds, sv = meta["methodText"].split(".")
            if sv != var and sds.upper() in harvested and dsn in harvested:
                r = claim_rate(data.get(dsn), var, data.get(sds.upper()), sds.upper(), sv)
                if r and r[1] and r[0] / r[1] < 0.99:
                    finding(f"DERIV.{dsn}.{var}", "error", [vid],
                            f"Metadata says {dsn}.{var} is derived from {meta['methodText']}, but the data agree in only "
                            f"{r[0]:,} of {r[1]:,} records.", "L06")
    a["variables"] = sorted(built.values(), key=lambda v: (v["dataset"], v["name"]))
    for v in a["variables"]:
        if not v["inData"]:
            src = cited_by.get(v["id"])
            text = (f"{ds_of(src)} cites {ds_of(v['id'])} as its predecessor, but there is no such variable in the data."
                    if src else f"{ds_of(v['id'])} is referenced but not in the data.")
            finding(f"VAR.MISSING.{ds_of(v['id'])}", "error" if src else "warning", [v["id"]] + ([src] if src else []), text, "L22")

    # ---- analyses, displays, cells
    an_by = {x["id"]: x for x in a["analyses"]}
    n_mismatch = 0
    for disp in a["displays"]:
        got = eng.extract_values(disp, tlf_pages.get(disp["id"], "")) if disp["id"] in tlf_pages else {}
        pg = next((p for p in a["programs"] if p["id"] == disp.get("program")), None)
        if pg:
            outs = [w for w in pg["writes"] if not w.endswith(".json")]
            disp["outputFile"] = outs[0] if outs else None
        statuses = []
        for sec in disp["sections"]:
            for row in sec["rows"]:
                for c in row["cells"]:
                    an = an_by[c["analysis"]]
                    val = got.get(c["id"])
                    try:
                        rv = eng.compute(c, an, data)
                        rec = eng.format_values(c["format"], rv)
                    except Exception as e:  # noqa: BLE001
                        rv, rec = None, f"error: {e}"
                    if val is None:
                        status = "missing"
                    elif rv is not None and eng.matches(rv, val):
                        status = "verified"
                    else:
                        status = "mismatch"
                        n_mismatch += 1
                        finding(f"CELL.{ds_of(c['id'])}", "error", [c["id"]],
                                f"Displayed '{val}' does not match recomputation '{rec}'.", "L13")
                    c["result"] = {"value": val, "status": status,
                                   "source": f"{rep['id']} page {disp['renderedIn']['page']} (text layer)" if val else None,
                                   "recomputed": rec}
                    statuses.append(status)
        disp["status"] = ("verified" if statuses and all(s == "verified" for s in statuses)
                          else "mismatch" if "mismatch" in statuses else "produced" if any(s != "missing" for s in statuses) else "programmed")
        miss = sum(s == "missing" for s in statuses)
        if miss:
            finding(f"CELL.MISSING.{ds_of(disp['id'])}", "warning", [disp["id"]], f"{miss} cells have no value in the rendered output.")
    for an in a["analyses"]:
        cells = [c for d in a["displays"] for s in d["sections"] for r in s["rows"] for c in r["cells"] if c["analysis"] == an["id"]]
        an["status"] = "verified" if cells and all(c["result"]["status"] == "verified" for c in cells) else "produced"

    # ---- conformance explanations
    unexpl = [i for i in a.get("conformance", {}).get("issues", []) if not i.get("explanation")]
    if unexpl:
        finding("CONF.UNEXPLAINED", "warning", sorted({i["dataset"] for i in unexpl}),
                f"{len(unexpl)} conformance issues have no explanation.", "L16")

    # ---- run order and data dependencies
    order = [r for r in a.get("runInstructions", {}).get("order", [])]
    pos = {r: i for i, r in enumerate(order)}
    for d in a["datasets"]:
        if d.get("producedBy") in pos:
            for dep in d.get("dependsOn", []):
                up = next((x.get("producedBy") for x in a["datasets"] if x["id"] == dep), None)
                if up in pos and pos[up] > pos[d["producedBy"]]:
                    finding(f"ORDER.{d['name']}", "error", [d["producedBy"], up],
                            f"{ds_of(d['producedBy'])} reads {ds_of(dep)} but runs before {ds_of(up)}, which creates it.")

    # ---- notes about refs, lifecycle
    a["findings"] = findings
    ids = all_ids(a)
    for n in a.get("notes", []):
        bad = [r for r in n["about"] if r not in ids]
        if bad:
            finding(f"NOTE.REF.{ds_of(n['id'])}", "warning", [n["id"]], f"Note refers to unknown entities: {', '.join(bad)}.")
    a["findings"] = findings
    set_lifecycle(a, "adrg sync", f"Synced from {root.name}")
    return a


def all_ids(a: dict) -> set[str]:
    ids = set()
    for key in ("documents", "estimands", "datasets", "variables", "parameters", "programs", "analyses", "displays",
                "notes", "findings"):
        ids |= {x["id"] for x in a.get(key, [])}
    ids |= {q["id"] for q in a.get("analysisConsiderations", {}).get("qa", [])}
    ids |= {c["id"] for d in a.get("displays", []) for s in d["sections"] for r in s["rows"] for c in r["cells"]}
    return ids


def set_lifecycle(a: dict, by: str, note: str):
    cells = [c for d in a.get("displays", []) for s in d["sections"] for r in s["rows"] for c in r["cells"]]
    errors = [f for f in a.get("findings", []) if f["severity"] == "error"]
    drafts = [n for n in a.get("notes", []) if n["status"] == "draft"]
    open_items = []
    if any(c["result"]["status"] != "verified" for c in cells):
        open_items.append(f"{sum(c['result']['status'] != 'verified' for c in cells)} of {len(cells)} cells not verified")
    if errors:
        open_items.append(f"{len(errors)} error findings")
    if drafts:
        open_items.append(f"{len(drafts)} notes in draft")
    unexpl = [i for i in a.get("conformance", {}).get("issues", []) if not i.get("explanation")]
    if unexpl:
        open_items.append(f"{len(unexpl)} conformance issues unexplained")
    if any(c["result"]["value"] for c in cells):
        stage = "executed"
    elif any(p.get("status") == "programmed" for p in a.get("programs", [])):
        stage = "programmed"
    elif a.get("metadata", {}).get("kind") not in (None, "none"):
        stage = "specified"
    else:
        stage = "planned"
    if stage == "executed" and not open_items:
        stage = "final"
    a["lifecycle"]["stage"] = stage
    a["lifecycle"]["openItems"] = open_items
    a["lifecycle"]["history"].append({"stage": stage, "date": now(), "by": by, "note": note})


# =================================================================== validate
REF_FIELDS = [
    ("analyses", ["dataset", "program", "estimand"], ["variables", "parameters"]),
    ("datasets", ["producedBy"], ["dependsOn"]),
    ("variables", ["dataset"], ["predecessors"]),
    ("parameters", ["dataset"], ["sources"]),
    ("programs", [], ["reads"]),
    ("notes", [], ["about"]),
    ("findings", [], ["about"]),
    ("displays", ["program"], ["analyses"]),
]


def cmd_validate(a: dict, schema: dict, root: Path | None) -> tuple[list[str], list[str], dict]:
    import jsonschema
    errors = [f"schema: {'/'.join(map(str, e.absolute_path)) or '(root)'}: {e.message[:160]}"
              for e in jsonschema.Draft202012Validator(schema).iter_errors(a)]
    ids = all_ids(a)
    warnings = []
    for key, single, multi in REF_FIELDS:
        for x in a.get(key, []):
            for f in single:
                r = x.get(f)
                if r and not r.startswith("FN:") and r not in ids:
                    errors.append(f"reference: {x['id']}.{f} -> {r} does not resolve")
            for f in multi:
                for r in x.get(f, []) or []:
                    if not r.startswith("FN:") and r not in ids:
                        (warnings if key in ("notes", "findings") else errors).append(f"reference: {x['id']}.{f} -> {r} does not resolve")
    for d in a.get("displays", []):
        for s in d["sections"]:
            for r in s["rows"]:
                for c in r["cells"]:
                    if c["analysis"] not in ids:
                        errors.append(f"reference: {c['id']}.analysis -> {c['analysis']} does not resolve")
    stale = []
    if root:
        for d in a.get("datasets", []):
            if d.get("file") and (root / d["file"]["path"]).exists() and sha256(root / d["file"]["path"]) != d["file"]["sha256"]:
                stale.append(d["id"])
        for p in a.get("programs", []):
            if p.get("sha256") and (root / p["path"]).exists() and sha256(root / p["path"]) != p["sha256"]:
                stale.append(p["id"])
        if a.get("metadata", {}).get("sha256"):
            src = next((x for x in a["documents"] if x["id"] == a["metadata"].get("source")), None)
            if src and (root / src["path"]).exists() and sha256(root / src["path"]) != a["metadata"]["sha256"]:
                stale.append(a["metadata"]["source"] + " (metadata snapshot is stale)")
        if stale:
            errors += [f"stale: {s} changed since the last sync" for s in stale]
    cells = [c for d in a.get("displays", []) for s in d["sections"] for r in s["rows"] for c in r["cells"]]
    summary = {"stage": a["lifecycle"]["stage"], "cells": len(cells),
               "cellStatus": {s: sum(c["result"]["status"] == s for c in cells) for s in sorted({c["result"]["status"] for c in cells})},
               "findings": {s: sum(f["severity"] == s for f in a.get("findings", [])) for s in ("error", "warning", "info")},
               "openItems": a["lifecycle"].get("openItems", [])}
    return errors, warnings, summary


# =================================================================== trace
def trace_cell(a: dict, cell_id: str) -> list[str]:
    idx = {}
    for key in ("variables", "datasets", "parameters", "programs", "analyses"):
        idx.update({x["id"]: x for x in a.get(key, [])})
    cell = disp = None
    for d in a["displays"]:
        for s in d["sections"]:
            for r in s["rows"]:
                for c in r["cells"]:
                    if c["id"] == cell_id:
                        cell, disp, row = c, d, r
    if not cell:
        return [f"{cell_id}: not found"]
    an = idx[cell["analysis"]]
    res = cell["result"]
    out = [f"{cell_id}", f"  {disp['displayId']} | row '{row['label']}' | column {cell['column']}",
           f"  value {res['value']!r} [{res['status']}]  recomputed {res['recomputed']!r}" + (f"  ({res['source']})" if res.get('source') else ""),
           f"  compute {json.dumps(cell['compute'])}  format '{cell['format']}'",
           f"ANALYSIS {an['id']}: {an['method']['description']}",
           f"  dataset {an['dataset']}  set {json.dumps(an.get('analysisSet', {}))}  subset {json.dumps(an.get('dataSubset', {}))}  by {an.get('groupBy')}"]
    for p in an.get("parameters", []):
        prm = idx.get(p, {})
        der = (prm.get("derivation") or {}).get("text")
        out.append(f"PARAMETER {p}:" + (f" {prm['param']}" if prm.get('param') else "") + f"  derivation: {der or '(none in metadata)'}")
    for n in a.get("notes", []):
        if cell["id"] in n["about"] or an["id"] in n["about"] or any(p in n["about"] for p in an.get("parameters", [])):
            out.append(f"  NOTE {n['id']} [{n['status']}]: {n['text'][:150]}")
    dsn = ds_of(an["dataset"])
    vars_ = [f"VAR:{dsn}.{v}" for v in eng.variables_of(cell, an)]

    def walk(vid, depth, seen):
        v = idx.get(vid)
        if not v or vid in seen:
            return
        seen.add(vid)
        der = (v.get("derivation") or {}).get("text")
        out.append("  " * depth + f"VAR {vid}" + (f" [{v['origin']}]" if v.get('origin') else "") + (f" {v['label']}" if v.get('label') else "") + (f" | derivation: {der[:90]}" if der else ""))
        for k in v.get("codeAnchors", [])[:3]:
            out.append("  " * depth + f"   {k['role']:7} {ds_of(k['program'])}:{k['line']}  {k['excerpt'][:100]}")
        for f in a.get("findings", []):
            if vid in f["about"]:
                out.append("  " * depth + f"   ! {f['severity']}: {f['text'][:140]}")
        for p in v.get("predecessors", []):
            walk(p, depth + 1, seen)
    out.append("LINEAGE (ADaM -> SDTM)")
    seen: set = set()
    for vid in vars_:
        walk(vid, 1, seen)
    ds = idx.get(an["dataset"], {})
    out.append(f"DATASET {an['dataset']} {ds.get('file', {}).get('path')} sha256 {str(ds.get('file', {}).get('sha256'))[:12]}… built by {ds.get('producedBy')} from {', '.join(ds.get('dependsOn', []))}")
    for pid in [an.get("program"), ds.get("producedBy")]:
        p = idx.get(pid)
        if p:
            out.append(f"PROGRAM {pid} sha256 {str(p.get('sha256'))[:12]}… run: {p['run']['mode']} | {p['run']['evidence']}")
            for f in a.get("findings", []):
                if pid in f["about"] and f["severity"] == "error":
                    out.append(f"   ! {f['severity']}: {f['text'][:160]}")
    return out


# =================================================================== core profile
def load_adrg(path: Path, narrative: Path | None = None) -> tuple[dict, dict | None]:
    """Return (full-shaped dict for the tools, the core dict or None)."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if "adrgCore" not in raw:
        return raw, None
    narr = yaml.safe_load(narrative.read_text(encoding="utf-8")) if narrative else None  # YAML or JSON
    return adrg_core.from_core(raw, narr), raw


def cmd_validate_core(core: dict, schema: dict, root: Path | None) -> tuple[list[str], list[str], dict]:
    import jsonschema
    errors = [f"schema: {'/'.join(map(str, e.absolute_path)) or '(root)'}: {e.message[:160]}"
              for e in jsonschema.Draft202012Validator(schema).iter_errors(core)]
    ids, warnings = adrg_core.core_ids(core), []
    for owner, field, target in adrg_core.core_refs(core):
        if target.startswith(adrg_core.EXTERNAL) or target in ids:
            continue
        (warnings if field == "about" else errors).append(f"reference: {owner}.{field} -> {target} does not resolve")
    if root:
        for sid, s in core.get("sources", {}).items():
            f = root / s["path"]
            if not f.exists():
                errors.append(f"stale: {sid} not found at {s['path']}")
            elif sha256(f) != s["sha256"]:
                errors.append(f"stale: {sid} changed since the last sync")
    full = adrg_core.from_core(core)
    cells = [c for d in full["displays"] for s in d["sections"] for r in s["rows"] for c in r["cells"]]
    summary = {"profile": "core " + core["adrgCore"], "stage": core["stage"], "cells": len(cells),
               "cellStatus": {s: sum(c["result"]["status"] == s for c in cells) for s in sorted({c["result"]["status"] for c in cells})},
               "findings": {s: sum(f["severity"] == s for f in core.get("findings", [])) for s in ("error", "warning", "info")},
               "links": len(adrg_core.core_refs(core)), "openItems": full["lifecycle"]["openItems"]}
    return errors, warnings, summary


# =================================================================== viewer
def cmd_viewer(a: dict, out: Path):
    tpl = (HERE / "viewer.html").read_text(encoding="utf-8")
    payload = json.dumps(a, separators=(",", ":")).replace("</", "<\\/")
    head = ('<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n')
    out.write_text(head + tpl.replace("/*ADRG_JSON*/null", payload) + "\n</html>\n", encoding="utf-8")


# =================================================================== main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("init"); s.add_argument("plan", type=Path); s.add_argument("-o", "--out", type=Path, required=True)
    s = sub.add_parser("sync"); s.add_argument("adrg", type=Path); s.add_argument("package_root", type=Path)
    s.add_argument("-o", "--out", type=Path); s.add_argument("--dsjson-schema", type=Path, default=SCHEMA_DIR / "dataset.schema.json")
    s = sub.add_parser("validate"); s.add_argument("adrg", type=Path); s.add_argument("--package", type=Path)
    s.add_argument("--schema", type=Path)
    s = sub.add_parser("trace"); s.add_argument("adrg", type=Path); s.add_argument("cell")
    s = sub.add_parser("core", help="split a full ADRG-JSON into the core profile and a narrative file")
    s.add_argument("adrg", type=Path); s.add_argument("-o", "--out", type=Path, required=True)
    s.add_argument("--narrative", type=Path, help="where to write the narrative part (study context, conformance, ...)")
    s = sub.add_parser("render"); s.add_argument("adrg", type=Path); s.add_argument("-o", "--out", type=Path, required=True)
    s.add_argument("--narrative", type=Path, help="narrative written later; merged with a core file for the PDF")
    s.add_argument("--final", action="store_true", help="refuse to render if the file is not at stage 'final'")
    s = sub.add_parser("viewer"); s.add_argument("adrg", type=Path); s.add_argument("-o", "--out", type=Path, required=True)
    args = ap.parse_args()
    load = lambda p: json.loads(p.read_text(encoding="utf-8"))  # noqa: E731
    dump = lambda obj, p: p.write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=str), encoding="utf-8")  # noqa: E731

    if args.cmd == "init":
        dump(cmd_init(yaml.safe_load(args.plan.read_text(encoding="utf-8"))), args.out)
        print(f"Wrote {args.out} (stage: planned)")
    elif args.cmd == "sync":
        schema = load(args.dsjson_schema) if args.dsjson_schema and args.dsjson_schema.exists() else None
        a = cmd_sync(load(args.adrg), args.package_root.resolve(), schema)
        dump(a, args.out or args.adrg)
        f = a["findings"]
        print(f"Wrote {args.out or args.adrg} (stage: {a['lifecycle']['stage']}; "
              f"{sum(x['severity'] == 'error' for x in f)} errors, {sum(x['severity'] == 'warning' for x in f)} warnings)")
    elif args.cmd == "validate":
        a = load(args.adrg)
        root = args.package.resolve() if args.package else None
        if "adrgCore" in a:
            errors, warnings, summary = cmd_validate_core(a, load(args.schema or SCHEMA_DIR / "adrg-core.schema.json"), root)
        else:
            errors, warnings, summary = cmd_validate(a, load(args.schema or SCHEMA_DIR / "adrg.schema.json"), root)
        for e in errors:
            print("ERROR  ", e)
        for w in warnings:
            print("WARN   ", w)
        print(json.dumps(summary, indent=1))
        sys.exit(1 if errors else 0)
    elif args.cmd == "trace":
        print("\n".join(trace_cell(load_adrg(args.adrg)[0], args.cell)))
    elif args.cmd == "core":
        core, narr = adrg_core.to_core(load(args.adrg))
        args.out.write_text(json.dumps(core, indent=1, ensure_ascii=False), encoding="utf-8")
        if args.narrative:
            dump(narr, args.narrative)
        print(f"Wrote {args.out}" + (f" and {args.narrative}" if args.narrative else ""))
    elif args.cmd == "render":
        import adrg_render
        a, core = load_adrg(args.adrg, args.narrative)
        if core is not None and not args.narrative:
            print("Note: rendering a core file without --narrative; narrative sections will be empty.")
        if args.final and a["lifecycle"]["stage"] != "final":
            print("Refusing --final: open items:\n  " + "\n  ".join(a["lifecycle"].get("openItems", [])))
            sys.exit(1)
        adrg_render.render(a, args.out)
        print(f"Wrote {args.out}")
    elif args.cmd == "viewer":
        cmd_viewer(load(args.adrg), args.out)  # the review board reads full or core files itself
        print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
