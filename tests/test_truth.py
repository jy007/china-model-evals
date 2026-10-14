from cme.truth import pick_fact

ACCN = "0000950170-25-100235"


def fact(val, end, start=None, accn=ACCN, form="10-K"):
    x = {"val": val, "end": end, "accn": accn, "form": form, "fy": 2025, "fp": "FY"}
    if start:
        x["start"] = start
    return x


def test_picks_annual_duration_not_quarter():
    facts = [
        fact(70, "2025-06-30", start="2025-04-01"),
        fact(281, "2025-06-30", start="2024-07-01"),
    ]
    assert pick_fact(facts, ACCN, "2025-06-30") == 281


def test_picks_instant_value_for_balance_sheet_items():
    assert pick_fact([fact(619, "2025-06-30")], ACCN, "2025-06-30") == 619


def test_ignores_other_filings():
    facts = [fact(1, "2025-06-30", accn="other"), fact(2, "2025-06-30")]
    assert pick_fact(facts, ACCN, "2025-06-30") == 2


def test_returns_none_when_missing():
    assert pick_fact([fact(1, "2024-06-30")], ACCN, "2025-06-30") is None
