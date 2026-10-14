# china-model-evals

Reproducible tests of Chinese LLMs on real tasks, scored against official data. Every number we post comes from a run in `runs/`, with the exact prompt, the raw model responses and the ground truth.

## Round 1: Microsoft FY2025 10-K, 18 figures

- **Task**: read Microsoft's full FY2025 annual report (~50K tokens) and return 18 figures from the income statement, balance sheet and cash flow statement.
- **Ground truth**: SEC XBRL company facts for CIK 0000789019, filing 0000950170-25-100235 (`data/msft-fy2025/truth.json`).
- **Models** (via OpenRouter, temperature 0): DeepSeek V4.1 Flash, Qwen3.8-Max, Kimi K3, GLM-5.3. 3 runs each.
- **Result**: 216/216 correct. Costs and hosts: [`runs/2026-10-14-msft-fy2025-uncached/summary.md`](runs/2026-10-14-msft-fy2025-uncached/summary.md).

## Reproduce

```bash
uv sync
uv run pytest
export OPENROUTER_API_KEY=...   # your own key
uv run python -m cme.run --data data/msft-fy2025 --out runs/my-run --repeats 3 --bust-cache
```

## Layout

- `src/cme/truth.py`: picks the annual values from the XBRL company-facts file.
- `src/cme/document.py`: annual-report HTML to text (table rows stay on one line).
- `src/cme/score.py`: classifies each answer as correct, unit error, wrong period, sign error, missing or wrong value.
- `src/cme/run.py`: calls the models and saves prompt, raw responses, usage and scores.
- `data/msft-fy2025/`: source HTML (microsoft.com/investor/reports/ar25), extracted text, XBRL company facts, ground truth.
- `runs/`: one folder per run.

## Limits

One clean large-cap filing and 18 headline figures. Zero errors here does not mean zero errors on notes, segments, derived metrics, PDFs or messier filers; that is the next round.
