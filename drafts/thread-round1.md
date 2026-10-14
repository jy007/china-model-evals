1/
I ran 4 Chinese LLMs on Microsoft's FY2025 10-K: 18 figures, 3 runs each, checked against the SEC's XBRL data. All via OpenRouter.
216 extractions. 0 errors. Not one prior-year figure mixed in.
The difference wasn't accuracy. It was cost.

2/
Median cost per call, full ~50K-token 10-K, no prompt cache:
GLM-5.3: $0.010
DeepSeek V4.1 Flash: $0.010
Kimi K3: $0.045
Qwen3.8-Max: $0.115
Median latency: 10s, 7s, 8s, 20s.

3/
The surprise: same model, same prompt, different bill.
OpenRouter picked a different host on each call. DeepSeek ranged $0.0015–0.015 (10x), GLM 6x, Kimi 4x. Only Qwen, served by Alibaba alone, was stable.
Choose the host, not just the model.

4/
Watch the cache too. Our first draft compared cached and uncached calls and claimed a 260x gap. Rerun without cache: ~12x.
Caveat: one clean large-cap 10-K. 0 errors on 18 figures means "none here", not "never" (95% upper bound ~15%).

5/
Next round is harder: footnotes, segment data, derived metrics, PDFs, small caps, mixed Chinese/English filings.
Script, prompt, raw responses and ground truth: https://github.com/jy007/china-model-evals
