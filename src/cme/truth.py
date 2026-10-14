"""Ground truth from SEC XBRL companyfacts (a locally downloaded JSON file)."""

import json
from datetime import date
from pathlib import Path

# (field, us-gaap tag, unit) — the 18 numbers we ask models to extract.
FIELDS = [
    ("revenue", "RevenueFromContractWithCustomerExcludingAssessedTax", "usd_millions"),
    ("gross_margin", "GrossProfit", "usd_millions"),
    ("research_and_development", "ResearchAndDevelopmentExpense", "usd_millions"),
    ("sales_and_marketing", "SellingAndMarketingExpense", "usd_millions"),
    ("general_and_administrative", "GeneralAndAdministrativeExpense", "usd_millions"),
    ("operating_income", "OperatingIncomeLoss", "usd_millions"),
    ("income_before_income_taxes", "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", "usd_millions"),
    ("provision_for_income_taxes", "IncomeTaxExpenseBenefit", "usd_millions"),
    ("net_income", "NetIncomeLoss", "usd_millions"),
    ("diluted_eps", "EarningsPerShareDiluted", "usd_per_share"),
    ("total_assets", "Assets", "usd_millions"),
    ("total_liabilities", "Liabilities", "usd_millions"),
    ("total_stockholders_equity", "StockholdersEquity", "usd_millions"),
    ("cash_and_cash_equivalents", "CashAndCashEquivalentsAtCarryingValue", "usd_millions"),
    ("short_term_investments", "ShortTermInvestments", "usd_millions"),
    ("property_and_equipment_net", "PropertyPlantAndEquipmentNet", "usd_millions"),
    ("goodwill", "Goodwill", "usd_millions"),
    ("net_cash_from_operations", "NetCashProvidedByUsedInOperatingActivities", "usd_millions"),
]

ANNUAL_MIN_DAYS = 300


def pick_fact(facts: list[dict], accn: str, end: str) -> float | None:
    """Value reported in filing `accn` for the period ending `end`.

    Duration facts must span roughly a year, so quarterly values in the same
    filing are skipped. Instant facts (balance sheet) have no start date.
    """
    for x in facts:
        if x["accn"] != accn or x["end"] != end or x.get("form") != "10-K":
            continue
        start = x.get("start")
        if start and (date.fromisoformat(end) - date.fromisoformat(start)).days < ANNUAL_MIN_DAYS:
            continue
        return x["val"]
    return None


def build_truth(companyfacts: Path, accn: str, end: str, prior_end: str) -> dict:
    """18 fields with the current-year value and the prior-year comparative from the same filing."""
    gaap = json.loads(companyfacts.read_text())["facts"]["us-gaap"]
    out = {}
    for field, tag, unit in FIELDS:
        facts = next(iter(gaap[tag]["units"].values()))
        value = pick_fact(facts, accn, end)
        if value is None:
            raise ValueError(f"{tag} has no annual value ending {end} in filing {accn}")
        scale = 1e6 if unit == "usd_millions" else 1
        prior = pick_fact(facts, accn, prior_end)
        out[field] = {
            "tag": tag,
            "unit": unit,
            "value": value / scale,
            "prior": None if prior is None else prior / scale,
        }
    return out
