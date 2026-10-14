# Run 2026-10-14 (uncached) · Microsoft FY2025 10-K · 18 figures × 4 models × 3 runs

Same document, prompt, ground truth and scoring as `../2026-10-14-msft-fy2025/`, but every prompt starts with a unique `Request id` line (`--bust-cache`), so no call hits a prompt cache (`cached_tokens` = 0 for all 12 calls). Use this run for cost comparisons.

| Model | Correct | Billed cost per call (min / median / max) | Latency (min–max) | Hosts OpenRouter routed to |
|---|---|---|---|---|
| z-ai/glm-5.3 | 54/54 | $0.0083 / $0.0096 / $0.0486 | 4.0–13.2 s | Wafer, InferenceNet, DigitalOcean |
| deepseek/deepseek-v4.1-flash | 54/54 | $0.0015 / $0.0104 / $0.0150 | 5.0–8.2 s | Crusoe, Relace, CoreWeave |
| moonshotai/kimi-k3 | 54/54 | $0.0366 / $0.0451 / $0.1624 | 7.6–9.7 s | InferenceNet, Relace, Parasail |
| qwen/qwen3.8-max-0902 | 54/54 | $0.1150 / $0.1151 / $0.1153 | 19.2–21.2 s | Alibaba |

Total spend for this run: $0.68.

## Reading
- Accuracy: 216/216 again.
- By median uncached cost, GLM-5.3 and DeepSeek V4.1 Flash are about the same; Kimi K3 is ~4.7× and Qwen3.8-Max ~12× more.
- For the same model and prompt, the bill varied with the host OpenRouter picked: ~10× for DeepSeek, ~6× for GLM, ~4× for Kimi. Only Qwen (single host, Alibaba) was stable.
- The first run (`../2026-10-14-msft-fy2025/`) mixed cached and uncached calls; its cost ratios (up to ~260×) mostly reflect cache hits and should not be quoted.
