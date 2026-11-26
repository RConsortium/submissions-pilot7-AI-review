"""ADRG-JSON core profile (v0.2).

The core keeps only what JSON does better than prose:
  - stable IDs and the links between them (cell -> analysis -> parameter -> variable -> SDTM -> code line)
  - a compute spec per cell, the shown value, the recomputed value and a status
  - notes and findings attached to IDs
  - hashes of every source read, so a stale file is detected

Everything else a PDF ADRG needs (study context, protocol and estimand text, standards, conformance
explanations, environment, run instructions, dataset descriptions) is written later as narrative and
merged only when the PDF is rendered.

to_core(full)          -> (core, narrative)   split an existing full ADRG-JSON
from_core(core, narr)  -> full-shaped dict     what trace, render and the review board work on
"""
from __future__ import annotations

import re

CORE_VERSION = "0.2.0"
NARRATIVE_KEYS = ("study", "documents", "standards", "protocol", "estimands", "analysisConsiderations",
                  "conformance", "environment", "runInstructions")


def _short(ref: str | None) -> str:
    return (ref or "").split(":", 1)[-1]


def _cells(displays):
    return [c for d in displays for s in d["sections"] for r in s["rows"] for c in r["cells"]]


def program_kind(pid: str) -> str:
    n = _short(pid).lower()
    return "tlf" if n.startswith("tlf") else "helper" if "helper" in n or "fcns" in n else "adam"


# ---------------------------------------------------------------------------- full -> core
def to_core(a: dict) -> tuple[dict, dict]:
    docs = {d["id"]: d for d in a.get("documents", [])}
    meta = a.get("metadata", {})
    produced = {d["id"]: d.get("producedBy") for d in a.get("datasets", [])}

    sources = {}
    if meta.get("sha256") and meta.get("source") in docs:
        sources[meta["source"]] = {"path": docs[meta["source"]]["path"], "sha256": meta["sha256"], "role": "metadata"}
    for d in a.get("datasets", []):
        if (d.get("file") or {}).get("sha256"):
            sources[d["id"]] = {"path": d["file"]["path"], "sha256": d["file"]["sha256"]}
    for p in a.get("programs", []):
        if p.get("sha256"):
            sources[p["id"]] = {"path": p["path"], "sha256": p["sha256"]}

    analyses = []
    for an in a.get("analyses", []):
        m = an.get("method", {})
        x = {"id": an["id"], "purpose": an.get("purpose"), "estimand": an.get("estimand"), "dataset": an["dataset"],
             "population": an.get("analysisSet") or None, "subset": an.get("dataSubset") or None, "by": an.get("groupBy"),
             "parameters": an.get("parameters") or None, "method": m.get("description"), "model": m.get("model"),
             "implementation": m.get("implementation"), "program": an.get("program")}
        analyses.append({k: v for k, v in x.items() if v not in (None, [], {})})

    displays = []
    for d in a.get("displays", []):
        secs = []
        for s in d["sections"]:
            rows = []
            for r in s["rows"]:
                cells = []
                for c in r["cells"]:
                    res = c.get("result") or {}
                    cell = {"id": c["id"], "analysis": c["analysis"], "compute": c["compute"], "format": c["format"],
                            "value": res.get("value"), "recomputed": res.get("recomputed"), "status": res.get("status", "planned")}
                    cells.append({k: v for k, v in cell.items() if v is not None})
                rows.append({"id": r["id"], "label": r["label"], "cells": cells})
            sec = {"id": s["id"], "label": s.get("label"), "rows": rows}
            if s.get("columns"):
                sec["columns"] = s["columns"]
            secs.append({k: v for k, v in sec.items() if v is not None})
        x = {"id": d["id"], "title": d["title"], "renderedIn": d.get("renderedIn"), "columns": d.get("columns"), "sections": secs}
        displays.append({k: v for k, v in x.items() if v is not None})

    variables = []
    for v in a.get("variables", []):
        x = {"id": v["id"], "derivation": (v.get("derivation") or {}).get("text"), "predecessors": v.get("predecessors") or None,
             "codeAnchors": [{"program": k["program"], "line": k["line"], "role": k["role"], "excerpt": k["excerpt"]}
                             for k in v.get("codeAnchors", [])] or None}
        variables.append({k: val for k, val in x.items() if val is not None})

    parameters = []
    for p in a.get("parameters", []):
        der = p.get("derivation") or {}
        x = {"id": p["id"], "where": der.get("whereClause"), "derivation": der.get("text")}
        parameters.append({k: v for k, v in x.items() if v is not None})

    programs = []
    for p in a.get("programs", []):
        writes = [ds for ds, by in produced.items() if by == p["id"]] or p.get("writes", [])
        run = p.get("run") or {}
        x = {"id": p["id"], "reads": p.get("reads") or None, "writes": writes or None,
             "run": {"mode": run["mode"], "evidence": run.get("evidence")} if run.get("mode") not in (None, "unknown") else None}
        programs.append({k: v for k, v in x.items() if v is not None})

    notes = [{k: n[k] for k in ("id", "about", "title", "text", "status", "section") if n.get(k) is not None}
             for n in a.get("notes", [])]
    findings = [{k: f[k] for k in ("id", "severity", "about", "text", "check") if f.get(k) is not None}
                for f in a.get("findings", [])]

    history = a.get("lifecycle", {}).get("history", [])
    core = {"adrgCore": CORE_VERSION, "study": a["study"]["studyId"], "stage": a["lifecycle"]["stage"],
            "generated": history[-1]["date"] if history else None, "sources": sources,
            "analyses": analyses, "displays": displays, "variables": variables, "parameters": parameters,
            "programs": programs, "notes": notes, "findings": findings}

    # narrative: what a writer adds later, plus descriptive fields the core leaves to define.xml or prose
    narr = {k: a[k] for k in NARRATIVE_KEYS if k in a}
    narr["datasets"] = [{k: d[k] for k in ("id", "label", "class", "structure", "purposes", "description") if d.get(k)}
                        | ({"file": {k: d["file"][k] for k in ("records", "createdAt", "sourceSystem") if d["file"].get(k) is not None}}
                           if d.get("file") else {})
                        for d in a.get("datasets", [])]
    narr["displays"] = [{k: d[k] for k in ("id", "displayId", "type", "population", "footnotes", "outputFile") if d.get(k)}
                        for d in a.get("displays", [])]
    narr["variables"] = [{k: v[k] for k in ("id", "label", "origin") if v.get(k)} for v in a.get("variables", [])
                         if v.get("label") or v.get("origin")]
    narr["parameters"] = [{"id": p["id"], "param": p["param"]} for p in a.get("parameters", []) if p.get("param")]
    narr["metadataKind"] = meta.get("kind")
    return core, narr


# ---------------------------------------------------------------------------- core -> full shape
def _display_id(did: str) -> tuple[str, str]:
    s = _short(did)
    return ("Figure " + s[1:], "figure") if s.startswith("F") else ("Listing " + s[1:], "listing") if s.startswith("L") else ("Table " + s[1:], "table")


def open_items(full: dict) -> list[str]:
    cells = _cells(full.get("displays", []))
    out = []
    nv = sum(c["result"]["status"] != "verified" for c in cells)
    if nv:
        out.append(f"{nv} of {len(cells)} cells not verified")
    errs = sum(f["severity"] == "error" for f in full.get("findings", []))
    if errs:
        out.append(f"{errs} error findings")
    drafts = sum(n.get("status") == "draft" for n in full.get("notes", []))
    if drafts:
        out.append(f"{drafts} notes in draft")
    unexpl = sum(not i.get("explanation") for i in full.get("conformance", {}).get("issues", []))
    if unexpl:
        out.append(f"{unexpl} conformance issues unexplained")
    return out


def from_core(core: dict, narr: dict | None = None) -> dict:
    narr = narr or {}
    nx = {k: {x["id"]: x for x in narr.get(k, [])} for k in ("datasets", "displays", "variables", "parameters")}
    src = core.get("sources", {})
    meta_id = next((k for k, v in src.items() if v.get("role") == "metadata"), None)

    a = {"adrgJSONVersion": "core " + core["adrgCore"],
         "study": narr.get("study") or {"studyId": core["study"], "title": core["study"]},
         "lifecycle": {"stage": core["stage"], "openItems": [],
                       "history": [{"stage": core["stage"], "date": core["generated"], "by": "adrg sync"}] if core.get("generated") else []}}
    for k in NARRATIVE_KEYS[1:]:
        if k in narr:
            a[k] = narr[k]
    a["metadata"] = ({"source": meta_id, "kind": narr.get("metadataKind") or "metadata", "sha256": src[meta_id]["sha256"],
                      "snapshotTakenAt": core.get("generated")} if meta_id else {"kind": "none"})
    if meta_id and not any(d["id"] == meta_id for d in a.get("documents", [])):
        a.setdefault("documents", []).append({"id": meta_id, "role": "metadata", "path": src[meta_id]["path"],
                                              "sha256": src[meta_id]["sha256"], "status": "present"})

    progs = []
    for p in core.get("programs", []):
        s = src.get(p["id"], {})
        progs.append({"id": p["id"], "path": s.get("path"), "sha256": s.get("sha256"), "kind": program_kind(p["id"]),
                      "status": "programmed", "reads": p.get("reads", []),
                      "writes": [_short(w) if w.startswith("DS:") else w for w in p.get("writes", [])],
                      "calls": [], "run": p.get("run") or {"mode": "unknown", "evidence": "No build receipt recorded."}})
    writer = {w: p["id"] for p in core.get("programs", []) for w in p.get("writes", []) if w.startswith("DS:")}
    reads = {p["id"]: [r for r in p.get("reads", []) if r.startswith("DS:")] for p in core.get("programs", [])}

    ds_ids = {k for k in src if k.startswith("DS:")}
    ds_ids |= {"DS:" + _short(v["id"]).split(".")[0] for v in core.get("variables", [])}
    ds_ids |= {an["dataset"] for an in core.get("analyses", [])}
    datasets = []
    for did in sorted(ds_ids, key=lambda x: (not _short(x).startswith("AD"), _short(x) != "ADSL", x)):
        name, s, extra = _short(did), src.get(did, {}), nx["datasets"].get(did, {})
        d = {"id": did, "name": name, "role": "analysis" if name.startswith("AD") else "tabulation",
             "label": extra.get("label"), "class": extra.get("class"), "structure": extra.get("structure"),
             "purposes": extra.get("purposes", []), "description": extra.get("description"),
             "producedBy": writer.get(did), "dependsOn": reads.get(writer.get(did), []),
             "file": ({"path": s["path"], "sha256": s["sha256"], **extra.get("file", {})} if s else None)}
        datasets.append(d)

    variables = []
    for v in core.get("variables", []):
        ds, name = _short(v["id"]).split(".", 1)
        extra = nx["variables"].get(v["id"], {})
        variables.append({"id": v["id"], "dataset": "DS:" + ds, "name": name, "label": extra.get("label"),
                          "origin": extra.get("origin"),
                          "derivation": {"text": v["derivation"]} if v.get("derivation") else None,
                          "predecessors": v.get("predecessors", []), "codeAnchors": v.get("codeAnchors", [])})

    parameters = []
    for p in core.get("parameters", []):
        ds, cd = _short(p["id"]).split(".", 1)
        parameters.append({"id": p["id"], "dataset": "DS:" + ds, "paramcd": cd, "param": nx["parameters"].get(p["id"], {}).get("param"),
                           "derivation": {"text": p.get("derivation"), "whereClause": p.get("where")}})

    var_by_ds = {}
    for v in variables:
        var_by_ds.setdefault(v["dataset"], []).append(v["id"])
    an_status = {}
    for c in _cells(core.get("displays", [])):
        an_status.setdefault(c["analysis"], set()).add(c.get("status", "planned"))
    analyses = []
    for an in core.get("analyses", []):
        st = an_status.get(an["id"], {"planned"})
        analyses.append({"id": an["id"], "purpose": an.get("purpose"), "estimand": an.get("estimand"), "dataset": an["dataset"],
                         "analysisSet": an.get("population", {}), "dataSubset": an.get("subset", {}), "groupBy": an.get("by"),
                         "parameters": an.get("parameters", []),
                         "method": {"description": an.get("method", ""), "model": an.get("model"), "implementation": an.get("implementation")},
                         "program": an.get("program"),
                         "status": "verified" if st == {"verified"} else next(iter(st - {"verified"}), "planned"),
                         "variables": var_by_ds.get(an["dataset"], []) + (var_by_ds.get("DS:ADSL", []) if an["dataset"] != "DS:ADSL" else [])})
    an_prog = {an["id"]: an.get("program") for an in core.get("analyses", [])}

    displays = []
    for d in core.get("displays", []):
        did, typ = _display_id(d["id"])
        extra = nx["displays"].get(d["id"], {})
        secs = []
        for s in d["sections"]:
            rows = [{"id": r["id"], "label": r["label"],
                     "cells": [{"id": c["id"], "column": c["id"].rsplit(".", 1)[-1], "analysis": c["analysis"], "compute": c["compute"],
                                "format": c["format"], "result": {"value": c.get("value"), "status": c.get("status", "planned"),
                                                                  "recomputed": c.get("recomputed"), "source": None}}
                               for c in r["cells"]]} for r in s["rows"]]
            secs.append({"id": s["id"], "label": s.get("label"), **({"columns": s["columns"]} if s.get("columns") else {}), "rows": rows})
        ans = list(dict.fromkeys(c["analysis"] for s in d["sections"] for r in s["rows"] for c in r["cells"]))
        displays.append({"id": d["id"], "displayId": extra.get("displayId", did), "type": extra.get("type", typ), "title": d["title"],
                         "population": extra.get("population"), "renderedIn": d.get("renderedIn"), "footnotes": extra.get("footnotes", []),
                         "columns": d.get("columns", []), "sections": secs, "analyses": ans,
                         "program": next((an_prog[x] for x in ans if an_prog.get(x)), None), "outputFile": extra.get("outputFile")})

    a.update({"datasets": datasets, "displays": displays, "analyses": analyses, "variables": variables, "parameters": parameters,
              "programs": progs,
              "notes": [{**n, "provenance": {"kind": "authored", "by": "study team"}} for n in core.get("notes", [])],
              "findings": [{**f, "resolution": None} for f in core.get("findings", [])]})
    a["lifecycle"]["openItems"] = open_items(a)
    return a


# ---------------------------------------------------------------------------- checks on the core itself
EXTERNAL = ("EST:", "DOC:", "FN:")


def core_ids(core: dict) -> set[str]:
    ids = set(core.get("sources", {}))
    for k in ("analyses", "displays", "variables", "parameters", "programs", "notes", "findings"):
        ids |= {x["id"] for x in core.get(k, [])}
    ids |= {c["id"] for c in _cells(core.get("displays", []))}
    ids |= {"DS:" + _short(v["id"]).split(".")[0] for v in core.get("variables", [])}
    return ids


def core_refs(core: dict) -> list[tuple[str, str, str]]:
    """(owner id, field, target id) for every link in the core."""
    out = []
    for an in core.get("analyses", []):
        out += [(an["id"], f, an[f]) for f in ("dataset", "program", "estimand") if an.get(f)]
        out += [(an["id"], "parameters", p) for p in an.get("parameters", [])]
    for c in _cells(core.get("displays", [])):
        out.append((c["id"], "analysis", c["analysis"]))
    for v in core.get("variables", []):
        out += [(v["id"], "predecessors", p) for p in v.get("predecessors", [])]
        out += [(v["id"], "codeAnchors", k["program"]) for k in v.get("codeAnchors", [])]
    for p in core.get("programs", []):
        out += [(p["id"], "reads", r) for r in p.get("reads", [])]
        out += [(p["id"], "writes", w) for w in p.get("writes", []) if re.match(r"^[A-Z]+:", w)]
    for k in ("notes", "findings"):
        for x in core.get(k, []):
            out += [(x["id"], "about", r) for r in x.get("about", [])]
    return out
