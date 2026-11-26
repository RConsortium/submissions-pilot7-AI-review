"""Render an ADRG-JSON file to a PDF in the PHUSE ADRG structure (reportlab).

Generated sections carry a 'Generated from …' tag and authored ones an 'Authored' tag,
so a reader can see what was checked by machine. Anything below stage 'final' is
watermarked DRAFT and opens with its open items.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
try:
    pdfmetrics.registerFont(TTFont("Body", str(FONT_DIR / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("Body-Bold", str(FONT_DIR / "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Body-Italic", str(FONT_DIR / "DejaVuSans-Oblique.ttf")))
    pdfmetrics.registerFont(TTFont("Mono", str(FONT_DIR / "DejaVuSansMono.ttf")))
    from reportlab.lib.fonts import addMapping
    addMapping("Body", 0, 0, "Body"); addMapping("Body", 1, 0, "Body-Bold"); addMapping("Body", 0, 1, "Body-Italic")
    BODY, BOLD, ITAL, MONO, ARROW = "Body", "Body-Bold", "Body-Italic", "Mono", "←"
except Exception:  # noqa: BLE001
    BODY, BOLD, ITAL, MONO, ARROW = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Courier", "<-"

INK = colors.HexColor("#1f2328")
MUTED = colors.HexColor("#6b7280")
RULE = colors.HexColor("#d0d7de")
HEAD_BG = colors.HexColor("#eef2f6")
OK = colors.HexColor("#1a7f37")
WARN = colors.HexColor("#9a6700")
BAD = colors.HexColor("#cf222e")

S = {
    "title": ParagraphStyle("title", fontName=BOLD, fontSize=22, leading=27, textColor=INK, spaceAfter=10),
    "subtitle": ParagraphStyle("subtitle", fontName=BODY, fontSize=12, leading=16, textColor=MUTED, spaceAfter=4),
    "h1": ParagraphStyle("h1", fontName=BOLD, fontSize=15, leading=19, textColor=INK, spaceBefore=14, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName=BOLD, fontSize=11.5, leading=15, textColor=INK, spaceBefore=10, spaceAfter=4),
    "body": ParagraphStyle("body", fontName=BODY, fontSize=10, leading=14, textColor=INK, spaceAfter=5, alignment=TA_LEFT),
    "tag": ParagraphStyle("tag", fontName=ITAL, fontSize=7.5, leading=10, textColor=MUTED, spaceAfter=5),
    "cell": ParagraphStyle("cell", fontName=BODY, fontSize=8, leading=10, textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName=BOLD, fontSize=8, leading=10, textColor=INK),
    "mono": ParagraphStyle("mono", fontName=MONO, fontSize=7.2, leading=9.2, textColor=INK),
    "toc1": ParagraphStyle("toc1", fontName=BODY, fontSize=10, leading=15, leftIndent=0),
    "toc2": ParagraphStyle("toc2", fontName=BODY, fontSize=9, leading=13, leftIndent=14, textColor=MUTED),
}


def esc(s) -> str:
    return (str(s) if s is not None else "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def short(ref: str | None) -> str:
    return (ref or "").split(":", 1)[-1]


class Doc(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in ("h1", "h2"):
            level = 0 if flowable.style.name == "h1" else 1
            text = flowable.getPlainText()
            key = f"h{id(flowable)}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=level > 0)
            self.notify("TOCEntry", (level, text, self.page, key))


def table(rows, widths, header=True, style_extra=None, font_size=8):
    data = [[c if not isinstance(c, str) else Paragraph(esc(c), S["cellb" if (header and i == 0) else "cell"])
             for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    st = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
          ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), HEAD_BG))
    t.setStyle(TableStyle(st + (style_extra or [])))
    return t


def status_par(status: str) -> Paragraph:
    col = {"verified": OK, "final": OK, "present": OK, "mismatch": BAD, "missing": BAD, "error": BAD,
           "interactive": WARN, "warning": WARN, "draft": WARN}.get(status, MUTED)
    return Paragraph(f'<font color="{col.hexval()}">{esc(status)}</font>', S["cell"])


def tag_generated(src: str, date: str | None = None) -> Paragraph:
    return Paragraph(f"Generated from {esc(src)}" + (f" · {esc(date)}" if date else ""), S["tag"])


def tag_authored(by: str = "study team", status: str = "final") -> Paragraph:
    s = "" if status == "final" else f' · <font color="{WARN.hexval()}">DRAFT</font>'
    return Paragraph(f"Authored · {esc(by)}{s}", S["tag"])


def notes_for(a, section=None, about=None):
    out = []
    for n in a.get("notes", []):
        if (section and n.get("section") == section) or (about and any(r in n["about"] for r in about)):
            out.append(n)
    return out


def note_flow(n) -> list:
    title = f"<b>{esc(n.get('title', ''))}.</b> " if n.get("title") else ""
    return [Paragraph(title + esc(n["text"]), S["body"]),
            tag_authored(n.get("provenance", {}).get("by", "study team"), n["status"])]


def build_story(a: dict, src_sha: str) -> list:
    st = a["study"]
    lc = a["lifecycle"]
    final = lc["stage"] == "final"
    meta = a.get("metadata", {})
    sync_date = next((h["date"][:10] for h in reversed(lc["history"]) if h["by"] == "adrg sync"), None)
    gen_src = f"{meta.get('kind', 'metadata')} (sha256 {str(meta.get('sha256'))[:12]}…) and the package"
    W = 7.0 * inch
    story = []

    # ---------------------------------------------------------------- cover
    story += [Spacer(1, 1.2 * inch), Paragraph("Analysis Data Reviewer's Guide", S["title"]),
              Paragraph(esc(st["title"]), S["subtitle"]),
              Paragraph(f"Study {esc(st['studyId'])} · Protocol {esc(st.get('protocolNumber', ''))}", S["subtitle"]),
              Spacer(1, 0.3 * inch)]
    cover = [["Rendered from", f"adrg.json (ADRG-JSON {a['adrgJSONVersion']}), sha256 {src_sha[:16]}…"],
             ["Lifecycle stage", lc["stage"] + ("" if final else "  (not final)")],
             ["Last synchronised", sync_date or "never"]]
    story.append(table(cover, [1.6 * inch, 5.4 * inch], header=False))
    if not final:
        story += [Spacer(1, 0.25 * inch), Paragraph("Open items before this guide can be final", S["h2"].clone("coverh"))]
        story += [Paragraph(f"• {esc(i)}", S["body"]) for i in lc.get("openItems", [])]
        errs = [f for f in a.get("findings", []) if f["severity"] == "error"]
        if errs:
            story.append(Paragraph(f"See section 6.3 for the {len(errs)} error findings.", S["body"]))
    story += [Spacer(1, 0.3 * inch), Paragraph(
        "How to read this guide: sections tagged <i>Generated</i> are built by <font face='%s'>adrg sync</font> "
        "from the metadata, datasets, programs and rendered outputs, and are re-checked whenever the package changes. "
        "Sections tagged <i>Authored</i> are the study team's explanations. Every display cell in Appendix A has a stable "
        "ID and was recomputed independently from the submitted data." % MONO, S["body"]), PageBreak()]

    toc = TableOfContents()
    toc.levelStyles = [S["toc1"], S["toc2"]]
    story += [Paragraph("Contents", S["h1"].clone("tocH", spaceBefore=0)), toc, PageBreak()]

    # ---------------------------------------------------------------- 1
    story.append(Paragraph("1 Introduction", S["h1"]))
    story.append(Paragraph("1.1 Purpose", S["h2"]))
    for n in notes_for(a, section="1.1"):
        story += note_flow(n)
    story.append(Paragraph("1.2 Study Data Standards and Dictionary Inventory", S["h2"]))
    story.append(table([["Standard or dictionary", "Version"]] + [[s["name"], s["version"]] for s in a.get("standards", [])],
                       [3.6 * inch, 3.4 * inch]))
    story.append(tag_authored())
    story.append(Paragraph("1.3 Source Data Used for Analysis Dataset Creation", S["h2"]))
    for n in notes_for(a, section="1.3"):
        story += note_flow(n)
    story.append(Paragraph("1.4 Documents in Scope", S["h2"]))
    rows = [["Document", "Role", "Location in package", "Status", "sha256"]]
    for d in a.get("documents", []):
        rows.append([short(d["id"]), d["role"], d.get("path") or "—", status_par(d["status"]),
                     (d.get("sha256") or "")[:12]])
    story.append(table(rows, [0.9 * inch, 1.4 * inch, 2.9 * inch, 0.7 * inch, 1.1 * inch]))
    story.append(tag_generated("the package file listing", sync_date))

    # ---------------------------------------------------------------- 2
    story.append(Paragraph("2 Protocol Description", S["h1"]))
    story.append(Paragraph("2.1 Protocol Number and Title", S["h2"]))
    story.append(Paragraph(f"Protocol number: {esc(st.get('protocolNumber'))}. Title: {esc(st['title'])}", S["body"]))
    p = a.get("protocol", {})
    story.append(Paragraph("2.2 Protocol Design in Relation to ADaM Concepts", S["h2"]))
    for label, key in (("Objectives", "objectives"), ("Design", "design"), ("Planned subjects", "plannedSubjects")):
        if p.get(key):
            story.append(Paragraph(f"<b>{label}.</b> {esc(p[key])}", S["body"]))
    story.append(tag_authored())
    story.append(Paragraph("2.3 Estimands", S["h2"]))
    rows = [["Endpoint", "Population", "Intercurrent events", "Summary measure", "Pre-specified"]]
    for e in a.get("estimands", []):
        ice = "; ".join(f"{i['event']}: {i['strategy']}" for i in e.get("intercurrentEvents", [])) or "—"
        rows.append([f"{e['endpoint']['label']} ({e['endpoint']['level']})", e["population"], ice, e["summaryMeasure"],
                     (e.get("prespecification") or {}).get("status", "—")])
    story.append(table(rows, [1.7 * inch, 1.2 * inch, 1.9 * inch, 1.4 * inch, 0.8 * inch]))
    story.append(tag_authored())

    # ---------------------------------------------------------------- 3
    vidx = {v["id"]: v for v in a.get("variables", [])}
    story.append(Paragraph("3 Analysis Considerations Related to Multiple Analysis Datasets", S["h1"]))
    story.append(Paragraph("3.1 Core Variables", S["h2"]))
    rows = [["Variable", "Label", "Origin"]]
    for r in a.get("analysisConsiderations", {}).get("coreVariables", []):
        v = vidx.get(r, {})
        rows.append([short(r), v.get("label") or "", v.get("origin") or ""])
    story.append(table(rows, [1.6 * inch, 3.9 * inch, 1.5 * inch]))
    story.append(tag_generated(gen_src, sync_date))
    qa = a.get("analysisConsiderations", {}).get("qa", [])
    for sec, title in (("3.2", "Treatment Variables"), ("3.3", "Use of Visit Windowing, Unscheduled Visits, and Record Selection"),
                       ("3.4", "Imputation/Derivation Methods")):
        story.append(Paragraph(f"{sec} {title}", S["h2"]))
        items = [q for q in qa if q["section"] == sec]
        for q in items:
            story.append(Paragraph(f"<b>{esc(q['question'])}</b> {esc(q['answer'])}", S["body"]))
        if items:
            story.append(tag_authored())
        for n in notes_for(a, section=sec):
            story += note_flow(n)

    # ---------------------------------------------------------------- 4
    ds = a.get("datasets", [])
    story.append(Paragraph("4 Analysis Data Creation and Processing Issues", S["h1"]))
    story.append(Paragraph("4.1 Split Datasets", S["h2"]))
    story.append(Paragraph("None. No dataset was split.", S["body"]))
    story.append(Paragraph("4.2 Data Dependencies", S["h2"]))
    rows = [["Analysis dataset", "Created by", "Reads"]]
    for d in ds:
        if d["role"] == "analysis":
            rows.append([d["name"], short(d.get("producedBy")) or "—", ", ".join(short(x) for x in d.get("dependsOn", [])) or "—"])
    story.append(table(rows, [1.4 * inch, 1.6 * inch, 4.0 * inch]))
    story.append(tag_generated("the programs' read and write calls", sync_date))
    story.append(Paragraph("4.3 Intermediate Datasets", S["h2"]))
    story.append(Paragraph("None. No intermediate datasets were created.", S["body"]))

    # ---------------------------------------------------------------- 5
    story.append(Paragraph("5 Analysis Dataset Descriptions", S["h1"]))
    story.append(Paragraph("5.1 Overview", S["h2"]))
    rows = [["Dataset", "Class", "Structure", "Purpose", "Records", "Built"]]
    for d in ds:
        if d["role"] == "analysis":
            f = d.get("file") or {}
            rows.append([f"{d['name']} – {d.get('label') or ''}", d.get("class") or "", d.get("structure") or "",
                         ", ".join(d.get("purposes", [])), f"{f['records']:,}" if f.get("records") is not None else "",
                         f"{(f.get('createdAt') or '')[:10]}\n{f.get('sourceSystem') or ''}"])
    story.append(table(rows, [1.5 * inch, 1.15 * inch, 1.6 * inch, 0.85 * inch, 0.6 * inch, 1.3 * inch]))
    story.append(tag_generated("Dataset-JSON headers and the specification", sync_date))
    story.append(Paragraph("5.2 Analysis Datasets", S["h2"]))
    params = a.get("parameters", [])
    for d in ds:
        if d["role"] != "analysis":
            continue
        block = [Paragraph(f"<b>{esc(d['name'])}</b> – {esc(d.get('label') or '')}", S["body"])]
        if d.get("description"):
            block += [Paragraph(esc(d["description"]), S["body"]), tag_authored()]
        ps = [p for p in params if p["dataset"] == d["id"]]
        if ps:
            rows = [["Parameter", "Label", "Derivation (value-level metadata)"]]
            for p in ps:
                rows.append([p["paramcd"], p.get("param") or "", (p.get("derivation") or {}).get("text") or "None in metadata"])
            block += [table(rows, [0.9 * inch, 1.9 * inch, 4.2 * inch]), tag_generated(gen_src, sync_date)]
        for n in notes_for(a, about=[d["id"]]):
            if n.get("section") not in ("1.3",):
                block += note_flow(n)
        story.append(KeepTogether(block))

    # ---------------------------------------------------------------- 6
    conf = a.get("conformance", {})
    story.append(Paragraph("6 Data Conformance Summary", S["h1"]))
    story.append(Paragraph("6.1 Conformance Inputs", S["h2"]))
    for q in conf.get("inputs", []):
        story.append(Paragraph(f"<b>{esc(q['question'])}</b> {esc(q['answer'])}", S["body"]))
    story.append(tag_authored())
    story.append(Paragraph("6.2 Issues Summary", S["h2"]))
    rows = [["Rule", "Message", "Dataset", "Count", "Explanation"]]
    for i in conf.get("issues", []):
        expl = Paragraph(esc(i["explanation"]), S["cell"]) if i.get("explanation") else \
            Paragraph(f'<font color="{BAD.hexval()}">Not explained</font>', S["cell"])
        rows.append([i["ruleId"], i["message"], short(i["dataset"]), str(i["count"]), expl])
    story.append(table(rows, [0.7 * inch, 2.6 * inch, 0.8 * inch, 0.55 * inch, 2.35 * inch]))
    story.append(tag_authored())
    story.append(Paragraph("6.3 Traceability Findings", S["h2"]))
    story.append(Paragraph("Checks run by <font face='%s'>adrg sync</font> against the package. Errors must be resolved "
                           "or explained before the guide is final." % MONO, S["body"]))
    order = {"error": 0, "warning": 1, "info": 2}
    rows = [["Severity", "Finding", "About"]]
    enc = [f for f in a.get("findings", []) if f["id"].startswith(("FND:DSJSON.NA.", "FND:DSJSON.SCHEMA."))]
    other = [f for f in a.get("findings", []) if f not in enc]
    ordered = sorted(other, key=lambda f: (order[f["severity"]], f["id"]))
    n_err = sum(f["severity"] == "error" for f in ordered)
    for i, f in enumerate(ordered):
        if i == n_err and enc:
            dsn = sorted({short(x) for g in enc for x in g["about"]})
            rows.append([status_par("error"), f"Dataset-JSON encoding: {len(enc)} findings across {len(dsn)} datasets "
                         "(missing values written as 'NA' strings, schema errors). Listed per dataset in Appendix B.",
                         ", ".join(dsn[:6]) + "…"])
        rows.append([status_par(f["severity"]), f["text"], ", ".join(short(x) for x in f["about"][:4]) + ("…" if len(f["about"]) > 4 else "")])
    story.append(table(rows, [0.7 * inch, 4.6 * inch, 1.7 * inch]))
    story.append(tag_generated("adrg sync checks", sync_date))

    # ---------------------------------------------------------------- 7
    env = a.get("environment", {})
    progs = a.get("programs", [])
    story.append(Paragraph("7 Submission of Programs", S["h1"]))
    story.append(Paragraph("7.1 Description", S["h2"]))
    plat = env.get("platform", {})
    story.append(Paragraph(
        f"R {esc(env.get('r', '?'))}; environment pinned by {esc((env.get('lockfile') or {}).get('path', 'no lockfile'))}. "
        f"Stated platform: {esc(plat.get('claimed') or 'not stated')}. Platforms recorded in the datasets: "
        f"{esc('; '.join(plat.get('observed', [])) or 'none recorded')}.", S["body"]))
    story.append(tag_generated("the lockfile and Dataset-JSON sourceSystem", sync_date))
    for kind, title in (("adam", "7.2 ADaM Programs"), ("tlf", "7.3 Analysis Output Programs")):
        story.append(Paragraph(title, S["h2"]))
        rows = [["Program", "Creates", "Reads", "Run", "sha256"]]
        for pg in progs:
            if pg["kind"] == kind:
                creates = ", ".join(pg.get("writes", [])) or "—"
                if kind == "tlf":
                    disp = [d["displayId"] for d in a["displays"] if d.get("program") == pg["id"]]
                    creates = "; ".join(disp) + (f" ({creates})" if creates != "—" else "")
                rows.append([short(pg["id"]), creates, ", ".join(short(r) for r in pg.get("reads", [])),
                             status_par(pg.get("run", {}).get("mode", "unknown")), (pg.get("sha256") or "")[:12]])
        story.append(table(rows, [1.2 * inch, 2.0 * inch, 2.0 * inch, 0.8 * inch, 1.0 * inch]))
        story.append(tag_generated("program code", sync_date))
    story.append(Paragraph("7.4 R Packages", S["h2"]))
    rows = [["Package", "Version", "Used by"]]
    for pk in env.get("packages", []):
        rows.append([pk["name"], pk["version"], ", ".join(short(u) for u in pk.get("usedBy", []))])
    story.append(table(rows, [1.4 * inch, 0.9 * inch, 4.7 * inch]))
    story.append(tag_generated("the renv lockfile and the packages the code loads", sync_date))

    # ---------------------------------------------------------------- 8
    ri = a.get("runInstructions", {})
    story.append(Paragraph("8 Running the Programs", S["h1"]))
    for i, sline in enumerate(ri.get("steps", []), 1):
        story.append(Paragraph(f"{i}. {esc(sline)}", S["body"]))
    story.append(Paragraph("Run order: " + (" → " if ARROW != "<-" else " -> ").join(short(r) for r in ri.get("order", [])), S["body"]))
    story.append(tag_authored())

    # ---------------------------------------------------------------- Appendix A
    story += [PageBreak(), Paragraph("Appendix A Display Traceability", S["h1"]),
              Paragraph("Each cell has a stable ID assigned at the shell stage. <i>Value</i> is what the rendered output "
                        "shows; <i>Recomputed</i> is an independent recomputation from the submitted data using the cell's "
                        "compute specification.", S["body"])]
    an_idx = {x["id"]: x for x in a.get("analyses", [])}
    for d in a.get("displays", []):
        cells = [(s, r, c) for s in d["sections"] for r in s["rows"] for c in r["cells"]]
        nver = sum(c["result"]["status"] == "verified" for _, _, c in cells)
        story.append(Paragraph(f"{esc(d['displayId'])}: {esc(d['title'])}", S["h2"]))
        story.append(Paragraph(
            f"Program {esc(short(d.get('program')))}; output {esc(d.get('outputFile') or '—')}; rendered in "
            f"{esc(short((d.get('renderedIn') or {}).get('doc')))} page {(d.get('renderedIn') or {}).get('page', '—')}. "
            f"{nver} of {len(cells)} cells verified.", S["body"]))
        for anid in d.get("analyses", []):
            an = an_idx.get(anid)
            if not an:
                continue
            sel = ", ".join(f"{k}={v}" for k, v in {**an.get("analysisSet", {}), **an.get("dataSubset", {})}.items())
            story.append(Paragraph(f"<b>{esc(short(anid))}</b> on {esc(short(an['dataset']))} [{esc(sel)}] by "
                                   f"{esc(an.get('groupBy'))}: {esc(an['method']['description'])}", S["body"]))
        rows = [["Row", "Column", "Value", "Recomputed", "Status", "Cell ID"]]
        for s, r, c in cells:
            label = (f"{s['label']}: " if s["label"] else "") + r["label"]
            rows.append([label, c["column"], c["result"]["value"] or "—", c["result"]["recomputed"] or "—",
                         status_par(c["result"]["status"]), Paragraph(esc(short(c["id"])), S["mono"])])
        story.append(table(rows, [1.6 * inch, 0.6 * inch, 1.05 * inch, 1.05 * inch, 0.6 * inch, 2.1 * inch]))
        story.append(tag_generated("the rendered output and Dataset-JSON data", sync_date))
        for n in notes_for(a, about=[d["id"]] + [c["id"] for _, _, c in cells]):
            story += note_flow(n)

    # ---------------------------------------------------------------- Appendix B
    story += [PageBreak(), Paragraph("Appendix B Variable Lineage", S["h1"]),
              Paragraph(f"Every variable used by an analysis, traced through its predecessors to SDTM. {ARROW} reads "
                        "'comes from'. Code references are program:line.", S["body"])]
    fidx = {}
    for f in a.get("findings", []):
        for r in f["about"]:
            fidx.setdefault(r, []).append(f)
    rows = [["Variable", "Origin and derivation", f"Comes from ({ARROW})", "Code"]]
    for v in a.get("variables", []):
        der = (v.get("derivation") or {}).get("text") or ""
        txt = f"{v.get('origin') or '—'}" + (f": {der}" if der else "")
        for f in fidx.get(v["id"], []):
            txt += f"  [{f['severity']}: {f['text']}]"
        code = "; ".join(f"{short(k['program'])}:{k['line']}" for k in v.get("codeAnchors", [])[:3])
        rows.append([short(v["id"]), Paragraph(esc(txt[:400]), S["cell"]),
                     ", ".join(short(p) for p in v.get("predecessors", [])) or "—", Paragraph(esc(code), S["mono"])])
    story.append(table(rows, [1.35 * inch, 3.15 * inch, 1.3 * inch, 1.2 * inch]))
    story.append(tag_generated(gen_src, sync_date))
    if enc:
        story.append(Paragraph("Dataset-JSON encoding findings", S["h2"]))
        rows = [["Dataset", "Finding"]] + [[", ".join(short(x) for x in f["about"]), f["text"]] for f in enc]
        story.append(table(rows, [1.2 * inch, 5.8 * inch]))
    return story


def render(a: dict, out: Path):
    raw = json.dumps(a, sort_keys=True).encode()
    src_sha = hashlib.sha256(raw).hexdigest()
    final = a["lifecycle"]["stage"] == "final"
    st = a["study"]

    def on_page(canv, doc):
        canv.saveState()
        if not final:
            canv.setFont(BOLD, 64)
            canv.setFillColor(colors.Color(0.85, 0.2, 0.2, alpha=0.08))
            canv.translate(letter[0] / 2, letter[1] / 2)
            canv.rotate(40)
            canv.drawCentredString(0, 0, "DRAFT")
            canv.rotate(-40)
            canv.translate(-letter[0] / 2, -letter[1] / 2)
        canv.setFont(BODY, 7.5)
        canv.setFillColor(MUTED)
        canv.drawString(0.75 * inch, 0.5 * inch,
                        f"ADRG · {st['studyId']} · rendered from adrg.json {src_sha[:12]} · stage {a['lifecycle']['stage']}")
        canv.drawRightString(letter[0] - 0.75 * inch, 0.5 * inch, f"Page {doc.page}")
        canv.restoreState()

    doc = Doc(str(out), pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch,
              topMargin=0.75 * inch, bottomMargin=0.8 * inch,
              title=f"Analysis Data Reviewer's Guide – {st['studyId']}", author="adrg render",
              subject=f"ADRG-JSON {a['adrgJSONVersion']} stage {a['lifecycle']['stage']}")
    doc.multiBuild(build_story(a, src_sha), onFirstPage=on_page, onLaterPages=on_page)
