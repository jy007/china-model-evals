# Run 2026-10-14 · Microsoft FY2025 10-K · 18 figures × 4 models × 3 runs

> **Cost figures in this run are not comparable across models**: some calls hit a prompt cache (all three DeepSeek calls did, warmed by an earlier smoke test) and others did not. Use `../2026-10-14-msft-fy2025-uncached/summary.md` for costs. Accuracy results stand.

- Document: Microsoft 2025 Annual Report (Form 10-K) HTML from microsoft.com/investor/reports/ar25, converted to text (~230k chars, ~50k tokens). Full prompt: `prompt.txt`.
- Ground truth: SEC XBRL companyfacts for CIK 0000789019, filing 0000950170-25-100235, period ending 2025-06-30 (`data/msft-fy2025/truth.json`).
- Models via OpenRouter, temperature 0, single prompt, no tools, no retrieval.

| Model | Correct (3 runs) | Latency (3 runs) | Cost per run (USD) |
|---|---|---|---|
| deepseek/deepseek-v4.1-flash | 54/54 | 4.0–4.6 s | $0.0006–0.0007 |
| z-ai/glm-5.3 | 54/54 | 4.3–5.2 s | $0.004–0.005 |
| moonshotai/kimi-k3 | 54/54 | 6.5–10.4 s | $0.036–0.157 |
| qwen/qwen3.8-max-0902 | 54/54 | 24.6–26.7 s | $0.021–0.117 |

Total spend: $0.41. Cost varies between runs mostly because of prompt caching on repeat calls.

## Reading
- Headline statement figures from a clean, large-cap 10-K are a solved task for all four models: zero errors, including no prior-year confusions (FY2024 comparatives sit in the same rows).
- The difference is cost and latency, not accuracy: per call, DeepSeek V4.1 Flash was 6–8× cheaper than GLM-5.3, 31–192× cheaper than Qwen3.8-Max and 54–258× cheaper than Kimi K3 for identical results. The wide ranges come from prompt caching: the first call to a model costs the most.
- OpenRouter served DeepSeek, Kimi and GLM from third-party hosts (DigitalOcean, InferenceNet, Wafer) and Qwen from Alibaba. Data-residency questions depend on the provider route, not just the model.

## Limits
0 errors on 18 distinct figures gives a one-sided 95% upper bound of ~15% on the per-figure error rate; repeats at temperature 0 are not independent evidence.
One company, one filing, 18 headline figures, one prompt. This does not show the models are reliable on notes, segment data, derived metrics, PDFs, or messier filers.
