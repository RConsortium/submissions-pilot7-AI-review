"""Cell engine for ADRG-JSON: select the records a cell describes, recompute its statistic,
and match shell formats against rendered output.

A cell's compute spec says what produces it, e.g.
    {"op": "mean_sd", "variable": "CHG", "where": {"AVISITN": 24}, "group": "Placebo"}
and the cell's analysis supplies the dataset, analysis set, data subset, grouping
variable and (for model-based ops) the model.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from lineage_harvest import read_dataset

NUM_TOKEN = re.compile(r"x+(?:\.x+)?")


# ----------------------------------------------------------------- formats
def format_to_regex(fmt: str) -> str:
    """'xx.x (xx.xx)' -> regex matching e.g. '2.5 ( 5.80)'. Decimal places are enforced."""
    out, pos = [], 0
    for m in NUM_TOKEN.finditer(fmt):
        lit = fmt[pos:m.start()]
        out.append("".join(r"\s*" if ch == " " else re.escape(ch) for ch in lit))
        tok = m.group(0)
        d = len(tok.split(".")[1]) if "." in tok else 0
        out.append(r"\s*-?\d+\.\d{%d}" % d if d else r"\s*-?\d+")   # R pads numbers with spaces
        pos = m.end()
    out.append("".join(r"\s*" if ch == " " else re.escape(ch) for ch in fmt[pos:]))
    return "".join(out)


def format_values(fmt: str, values: list[float]) -> str:
    it = iter(values)

    def sub(m):
        tok = m.group(0)
        d = len(tok.split(".")[1]) if "." in tok else 0
        try:
            v = next(it)
        except StopIteration:
            return tok
        return f"{v:.{d}f}" if d else f"{int(round(v))}"
    return NUM_TOKEN.sub(sub, fmt)


def numbers(s: str) -> list[float]:
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", s or "")]


def decimals(s: str) -> list[int]:
    return [len(x.split(".")[1]) if "." in x else 0 for x in re.findall(r"-?\d+(?:\.\d+)?", s or "")]


def matches(values: list[float], shown: str) -> bool:
    sv, dv = numbers(shown), decimals(shown)
    return len(sv) == len(values) and all(abs(v - s) <= 0.5 * 10 ** (-d) + 1e-9 for v, s, d in zip(values, sv, dv))


# ----------------------------------------------------------------- data
class Data:
    """Loads datasets by name from the package, once."""

    def __init__(self, root: Path, datasets: list[dict]):
        self.root = root
        self.paths = {d["name"]: d["file"]["path"] for d in datasets if d.get("file")}
        self._cache: dict[str, pd.DataFrame] = {}

    def get(self, name: str) -> pd.DataFrame:
        if name not in self._cache:
            self._cache[name] = read_dataset(self.root / self.paths[name])[0]
        return self._cache[name]


def _apply(df: pd.DataFrame, cond: dict) -> pd.DataFrame:
    for k, v in (cond or {}).items():
        if isinstance(v, dict) and "in" in v:
            df = df[df[k].isin(v["in"])]
        elif isinstance(v, dict) and v.get("notnull"):
            df = df[df[k].notna()]
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            df = df[np.isclose(pd.to_numeric(df[k], errors="coerce"), v)]
        else:
            df = df[df[k] == v]
    return df


def _with_adsl(df: pd.DataFrame, needed: set[str], data: Data) -> pd.DataFrame:
    missing = [c for c in needed if c not in df.columns]
    if not missing or "ADSL" not in data.paths:
        return df
    adsl = data.get("ADSL")
    cols = ["USUBJID"] + [c for c in missing if c in adsl.columns]
    return df.merge(adsl[cols], on="USUBJID", how="left")


def analysis_records(an: dict, data: Data, where: dict | None = None) -> pd.DataFrame:
    ds = an["dataset"].split(":", 1)[1]
    df = data.get(ds)
    needed = set(an.get("analysisSet", {})) | set(an.get("dataSubset", {})) | set((where or {})) | {an.get("groupBy") or ""}
    model = an.get("method", {}).get("model") or {}
    needed |= {model.get(k) for k in ("response", "treatment", "numericTreatment") if model.get(k)}
    needed |= set(model.get("factors", [])) | set(model.get("covariates", []))
    df = _with_adsl(df, {n for n in needed if n}, data)
    df = _apply(df, an.get("analysisSet", {}))
    df = _apply(df, an.get("dataSubset", {}))
    return _apply(df, where or {})


# ----------------------------------------------------------------- models
def _design(df: pd.DataFrame, model: dict, levels: list[str] | None):
    parts = [pd.Series(1.0, index=df.index, name="(Intercept)")]
    trt_cols = {}
    if model.get("numericTreatment"):
        parts.append(df[model["numericTreatment"]].astype(float).rename(model["numericTreatment"]))
    if model.get("treatment"):
        for lv in levels[1:]:
            col = (df[model["treatment"]] == lv).astype(float).rename(f"trt[{lv}]")
            trt_cols[lv] = col.name
            parts.append(col)
    fac_levels = {}
    for f in model.get("factors", []):
        lv = sorted(df[f].dropna().unique().tolist())
        fac_levels[f] = lv
        for l in lv[1:]:
            parts.append((df[f] == l).astype(float).rename(f"{f}[{l}]"))
    for c in model.get("covariates", []):
        parts.append(df[c].astype(float).rename(c))
    X = pd.concat(parts, axis=1)
    return X, trt_cols, fac_levels


def fit(df: pd.DataFrame, model: dict, levels: list[str] | None = None) -> dict:
    terms = [model["response"]] + [model[k] for k in ("treatment", "numericTreatment") if model.get(k)] \
        + model.get("factors", []) + model.get("covariates", [])
    d = df.dropna(subset=terms)
    if model.get("treatment") and levels is None:
        levels = sorted(d[model["treatment"]].unique().tolist())
    X, trt_cols, fac_levels = _design(d, model, levels)
    y = d[model["response"]].to_numpy(float)
    A = X.to_numpy(float)
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ beta
    dof = len(y) - A.shape[1]
    s2 = (resid ** 2).sum() / dof
    return {"beta": beta, "V": s2 * np.linalg.inv(A.T @ A), "dof": dof, "cols": list(X.columns),
            "resid": resid, "data": d, "levels": levels, "trt_cols": trt_cols, "fac_levels": fac_levels, "model": model}


def _contrast_vec(f: dict, g1: str, g2: str) -> np.ndarray:
    c = np.zeros(len(f["cols"]))
    for g, s in ((g1, 1), (g2, -1)):
        col = f["trt_cols"].get(g)
        if col:
            c[f["cols"].index(col)] += s
    return c


def _lsmean_vec(f: dict, g: str) -> np.ndarray:
    """emmeans-style reference grid: covariates at their mean, factors averaged with equal weights."""
    c = np.zeros(len(f["cols"]))
    c[0] = 1.0
    if f["trt_cols"].get(g):
        c[f["cols"].index(f["trt_cols"][g])] = 1.0
    for fac, lv in f["fac_levels"].items():
        for l in lv[1:]:
            c[f["cols"].index(f"{fac}[{l}]")] = 1.0 / len(lv)
    for cov in f["model"].get("covariates", []):
        c[f["cols"].index(cov)] = f["data"][cov].astype(float).mean()
    return c


# ----------------------------------------------------------------- compute
def compute(cell: dict, an: dict, data: Data) -> list[float]:
    cp = cell["compute"]
    op = cp["op"]
    group, gv = cp.get("group"), an.get("groupBy")
    if op == "bign" and cp.get("populationDataset"):
        pop = data.get(cp["populationDataset"])
        pop = _apply(pop, {k: v for k, v in an.get("analysisSet", {}).items() if k in pop.columns})
        return [float(pop[pop[cp["groupVariable"]] == group]["USUBJID"].nunique())]
    if op in ("ancova_dose_p", "pairwise_p", "pairwise_diff_se", "pairwise_ci", "lsmean_ci",
              "diff_ci_normal", "diff_p", "rmse_n"):
        f = fit(analysis_records(an, data, cp.get("where")), an["method"]["model"])
        if op == "rmse_n":
            return [float(np.sqrt(np.mean(f["resid"] ** 2)))]
        if op == "ancova_dose_p":
            i = f["cols"].index(an["method"]["model"]["numericTreatment"])
            t = f["beta"][i] / np.sqrt(f["V"][i, i])
            return [float(2 * stats.t.sf(abs(t), f["dof"]))]
        if op == "lsmean_ci":
            c = _lsmean_vec(f, group)
            est, se = c @ f["beta"], np.sqrt(c @ f["V"] @ c)
            q = stats.t.ppf(0.975, f["dof"])
            return [float(est), float(est - q * se), float(est + q * se)]
        g1, g2 = cp["contrast"]
        c = _contrast_vec(f, g1, g2)
        est, se = c @ f["beta"], np.sqrt(c @ f["V"] @ c)
        p = 2 * stats.t.sf(abs(est / se), f["dof"])
        if op in ("pairwise_p", "diff_p"):
            return [float(p)]
        if op == "pairwise_diff_se":
            return [float(est), float(se)]
        if op == "pairwise_ci":
            q = stats.t.ppf(0.975, f["dof"])
            return [float(est - q * se), float(est + q * se)]
        if op == "diff_ci_normal":
            return [float(est), float(est - 1.96 * se), float(est + 1.96 * se)]
    df = analysis_records(an, data, cp.get("where"))
    if group is not None and gv:
        df = df[df[gv] == group]
    if op == "bign":
        return [float(df["USUBJID"].nunique())]
    if op == "count":
        return [float((df[cp["variable"]] == cp["value"]).sum())]
    if op == "at_risk":
        return [float((pd.to_numeric(df[cp["variable"]], errors="coerce") >= cp["time"]).sum())]
    s = pd.to_numeric(df[cp["variable"]], errors="coerce").dropna()
    if op == "n":
        return [float(len(s))]
    if op == "mean_sd":
        return [float(s.mean()), float(s.std(ddof=1))]
    if op == "median":
        return [float(s.median())]
    if op == "min_max":
        return [float(s.min()), float(s.max())]
    if op == "median_range":
        return [float(s.median()), float(s.min()), float(s.max())]
    raise ValueError(f"unknown op {op}")


def variables_of(cell: dict, an: dict) -> list[str]:
    """Dataset variables a cell depends on (for tracing)."""
    cp = cell["compute"]
    out = []
    model = an.get("method", {}).get("model") or {}
    if cp["op"] in ("ancova_dose_p", "pairwise_p", "pairwise_diff_se", "pairwise_ci", "lsmean_ci",
                    "diff_ci_normal", "diff_p", "rmse_n"):
        out += [model.get("response"), model.get("treatment"), model.get("numericTreatment")]
        out += model.get("factors", []) + model.get("covariates", [])
    else:
        out.append(cp.get("variable"))
        if cp["op"] == "bign":
            out += ["USUBJID", cp.get("groupVariable")]
    out.append(an.get("groupBy"))
    out += list(an.get("analysisSet", {})) + list(an.get("dataSubset", {})) + list(cp.get("where", {}))
    seen, res = set(), []
    for v in out:
        if v and v not in seen:
            seen.add(v)
            res.append(v)
    return res


def extract_values(display: dict, page_text: str) -> dict[str, str]:
    """Pick each cell's rendered value out of a PDF text layer using row text/anchor and cell formats."""
    lines = [ln.strip() for ln in page_text.splitlines()]
    found = {}
    for sec in display.get("sections", []):
        for row in sec["rows"]:
            anchor = row.get("anchor") or sec.get("anchor")
            start = 0
            if anchor:
                start = next((i for i, ln in enumerate(lines) if re.search(anchor, ln)), None)
            elif sec["label"]:
                start = next((i for i, ln in enumerate(lines) if ln == sec["label"]), None)
            if start is None:
                continue
            label_rx = row.get("text")
            if label_rx is None:
                label_rx = re.escape(row["label"]) if row["label"] else ""
            cells_rx = r"\s*".join(f"({format_to_regex(c['format'])})" for c in row["cells"])
            rx = re.compile(r"^" + label_rx + (r"\s*" if label_rx else "") + cells_rx)
            for ln in lines[start:]:
                m = rx.search(ln)
                if m:
                    for c, val in zip(row["cells"], m.groups()):
                        found[c["id"]] = val
                    break
    return found
