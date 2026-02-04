<!--
Domain: Trading / Finance
Complexity: Complex
Tested with: Claude Sonnet 4
Author: IntentFlow Examples
-->

# Workflow: Quarterly Trading Strategy Analysis

## Meta
version: 0.1
author: IntentFlow Team
requires: Claude with computer use, MCP support
estimated_time: 30 minutes
tags: trading, analysis, reporting, finance

## Context
This workflow analyzes the performance of a systematic trading strategy over the last quarter.
The output is an investor-ready report that includes performance metrics, risk analysis,
and comparison with market benchmarks. The strategy being analyzed uses a Dual Momentum
Stochastic (DMS) indicator system with three-phase market regime detection.

---

## Step 1: Trade Data Collection

### Dependencies
```bash
pip install pandas pyarrow mt5-python --break-system-packages
```

### Configuration
Set up MT5 connection:
- Server: Use environment variable MT5_SERVER
- Login: Use environment variable MT5_LOGIN  
- Password: Use environment variable MT5_PASSWORD

### Task
Connect to the MT5 trading platform and extract all closed trades from the last quarter
that have the tag "DMS-v2" in their comments. For each trade, collect:
- Entry and exit timestamps
- Symbol traded
- Position size (volume)
- Entry and exit prices
- Realized P&L
- Trade duration
- Closing reason (TP, SL, manual, or signal)

### Save as
`/tmp/workflow/step1_trades.parquet`

### Success criteria
- Minimum 500 trades in the dataset
- All required fields present with no null values
- Trade dates fall within the Q4 date range
- P&L values are in account currency (USD)

### If something goes wrong
- Connection timeout → wait 30 seconds, retry up to 3 times
- Authentication failed → check credentials, abort with clear error message
- Less than 500 trades → expand to last 6 months, note this in metadata
- Missing fields → log which fields are missing, continue with available data

---

## Step 2: Performance Metrics Calculation

### Dependencies
```bash
pip install quantstats numpy scipy --break-system-packages
```

### Task
Using the trade data from Step 1, calculate comprehensive performance metrics:

**Required metrics:**
- Total return (%)
- Sharpe ratio (annualized, risk-free rate = 5%)
- Sortino ratio
- Maximum drawdown (% and duration)
- Win rate (%)
- Profit factor
- Average trade duration
- Average winner vs average loser

**Regime-specific analysis:**
- Break down win rate and profit factor by market regime if regime data is available
- Calculate performance during trending vs ranging markets

### Flexibility
If you identify additional metrics that would provide valuable insight into
the strategy's behavior, include them. Consider metrics that reveal:
- Strategy consistency
- Risk-adjusted performance
- Execution quality

### Save as
- `/tmp/workflow/step2_metrics.json` — all calculated metrics
- `/tmp/workflow/step2_equity_curve.csv` — daily equity curve data

### Success criteria
- All required metrics calculated
- Sharpe ratio is a reasonable value (between -5 and 5)
- Maximum drawdown is between 0% and 100%
- Equity curve has no gaps in trading days

### If something goes wrong
- Division by zero → use fallback value, note in output
- Insufficient data for regime analysis → skip regime breakdown, note limitation
- Numerical instability → use robust calculation methods (median instead of mean where appropriate)

---

## Step 3: Benchmark Comparison

### Dependencies
```bash
pip install yfinance --break-system-packages
```

### Task
Fetch benchmark data for the same period and compare strategy performance:

**Benchmarks to fetch:**
- S&P 500 (SPY)
- NASDAQ 100 (QQQ)
- 60/40 Portfolio proxy (calculate from SPY + TLT)

**Comparisons to make:**
- Overlay equity curves
- Compare risk-adjusted returns
- Calculate correlation with each benchmark
- Compute beta and alpha relative to SPY

### Flexibility
- If Yahoo Finance is unavailable, use any reliable alternative data source
- If additional benchmarks would be more relevant to the strategy's asset class, substitute appropriately
- Visualization style is at your discretion — prioritize clarity

### Constraints
- All data must be from the exact same date range as the strategy
- Use adjusted close prices for benchmarks

### Save as
- `/tmp/workflow/step3_comparison.json` — comparison metrics
- `/tmp/workflow/step3_equity_comparison.png` — overlay chart

### Success criteria
- All three benchmarks successfully fetched
- Date alignment verified (same start/end dates)
- Chart is readable with clear legend
- Alpha and beta values are reasonable

### If something goes wrong
- Yahoo Finance rate limited → add delays between requests, retry
- Benchmark data missing days → forward-fill gaps (max 3 days)
- One benchmark unavailable → proceed with remaining benchmarks, note in report

---

## Step 4: Risk Analysis

### Task
Perform detailed risk analysis of the strategy:

**Analysis components:**
- Value at Risk (VaR) at 95% and 99% confidence levels
- Conditional VaR (Expected Shortfall)
- Drawdown analysis: all drawdowns > 5%, recovery times
- Worst day, worst week, worst month
- Consecutive losing trades analysis
- Position sizing consistency

**Stress scenarios:**
- Estimate performance during 2008-like conditions (scale by historical volatility)
- Estimate performance during 2020 March-like conditions

### Flexibility [guided]
The specific statistical methods for VaR calculation are at your discretion.
Choose between historical, parametric, or Monte Carlo based on data availability.

### Constraints
- Do not overstate confidence in stress test results — they are estimates
- Include appropriate caveats about historical analysis limitations

### Save as
- `/tmp/workflow/step4_risk_analysis.json` — all risk metrics
- `/tmp/workflow/step4_drawdown_chart.png` — drawdown visualization

### Success criteria
- VaR values are negative (representing potential losses)
- All drawdowns identified and documented
- Stress scenarios clearly labeled as estimates

---

## Step 5: Report Generation

### Dependencies
```bash
pip install reportlab matplotlib seaborn --break-system-packages
```

### Task
Create a professional, investor-ready PDF report that synthesizes all previous analysis.

**Report structure:**
1. Executive Summary (1 paragraph, key takeaways)
2. Performance Overview (metrics table + equity curve)
3. Benchmark Comparison (relative performance)
4. Risk Profile (VaR, drawdowns, stress tests)
5. Appendix (methodology notes, data sources)

**Design requirements:**
- Clean, professional aesthetic
- Consistent color scheme throughout
- All charts must have clear labels and legends
- Include MBM Systems branding if assets are available

### Flexibility [autonomous]
The exact layout, chart styles, and narrative voice are at your discretion.
The goal is a report that instills confidence in sophisticated investors
while being accessible to those less familiar with quantitative metrics.

### Constraints
- Maximum 6 pages (excluding appendix)
- No jargon without explanation
- All numbers must trace back to previous steps
- Include disclaimer about past performance

### Save as
`/tmp/workflow/step5_investor_report.pdf`

### Success criteria
- PDF renders correctly and is not corrupted
- All required sections present
- Page count within limit
- A non-technical reader can understand the executive summary

### If something goes wrong
- PDF generation fails → fall back to HTML report
- Charts not rendering → embed as separate PNG files
- Branding assets missing → use clean minimal design

---

## Finalization

### After completion
1. Copy all artifacts to `/home/user/reports/q4_analysis/`
2. Create `manifest.json` listing all files with timestamps and checksums
3. Create `run_log.md` documenting any deviations from the workflow
4. Clean up `/tmp/workflow/` directory

### Verification
Verify the final report:
- Open the PDF and confirm all pages render
- Check that all charts are present and readable
- Verify the executive summary numbers match the detailed sections

### Notification
Provide a summary including:
- Key performance metrics (return, Sharpe, max drawdown)
- How strategy compared to S&P 500
- Any issues encountered and how they were resolved
- Location of all output files
