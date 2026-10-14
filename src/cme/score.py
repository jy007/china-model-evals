"""Classify one extracted number against the XBRL ground truth."""

TOLERANCE = {"usd_millions": 0.5, "usd_per_share": 0.005}


def _close(a: float, b: float, unit: str) -> bool:
    return abs(a - b) <= TOLERANCE[unit]


def classify(answer: float | None, truth: dict) -> str:
    """One of: correct, unit_error, wrong_period, sign_error, missing, wrong_value."""
    if answer is None:
        return "missing"
    unit, value, prior = truth["unit"], truth["value"], truth.get("prior")
    if _close(answer, value, unit):
        return "correct"
    if value and any(_close(answer / f, value, unit) for f in (1e3, 1e6, 1e-3)):
        return "unit_error"
    if prior is not None and _close(answer, prior, unit):
        return "wrong_period"
    if _close(-answer, value, unit):
        return "sign_error"
    return "wrong_value"


def to_number(raw) -> float | None:
    """Accept numbers or strings like "1,234", "(56)", "$7.8"; anything else is missing."""
    if raw is None or isinstance(raw, bool):
        return None
    if isinstance(raw, (int, float)):
        return float(raw)
    s = str(raw).strip().replace(",", "").replace("$", "")
    negative = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    try:
        n = float(s)
    except ValueError:
        return None
    return -n if negative else n
