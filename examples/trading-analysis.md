# Workflow: Trading Strategy Analysis

## Meta
version: 1.0
author: MBM Systems
requires: Claude with computer use, MT5 access
estimated_time: 30 minutes
tags: trading, analysis, reporting, finance

## Context
Analyze the performance of the DMS (Dual Momentum Stochastic) trading strategy 
over the last quarter. Compare results against market benchmarks and prepare 
an investor-ready report.

This workflow is designed for quarterly performance reviews and due diligence 
documentation.

---

## Step 1: Fetch Trading Data

### Dependencies
```bash
pip install mt5-mcp-server pandas pyarrow --break-system-packages
```

### Configuration
- MT5 Server: Use `MT5_HOST` environment variable (default: mt5.example.com)
- Credentials: `MT5_LOGIN` and `MT5_PASSWORD` from environment
- If primary server unavailable, fallback to `MT5_BACKUP_HOST`

### Task
Connect to the MT5 trading platform and extract all closed trades for bots 
tagged with "DMS-v2" from the last quarter (Q4 2024: October 1 - December 31).

Required fields for each trade:
- Entry timestamp and exit timestamp
- Symbol (trading pair)
- Direction (buy/sell)
- Volume (lot size)
- Entry price and exit price
- Realized PnL
- Close reason (TP, SL, manual, signal)

### Save as
`/tmp/workflow/step1_trades.parquet`

### Success criteria
- File exists and is valid Parquet format
- Contains minimum 500 trades (strategy should be active)
- No null values in required fields
- All timestamps fall within Q4 2024
- PnL values sum to a non-zero amount

### If something goes wrong
- Connection timeout → check VPN status, retry with backup host
- Authentication failed → verify credentials, stop and report
- Fewer than 500 trades → expand to 6 months, document the change in report
- API rate limited → add 1-second delay between requests

---

## Step 2: Calculate Performance Metrics

### Dependencies
```bash
pip install quantstats numpy scipy --break-system-packages
```

### Task
Using the trade data from Step 1, calculate comprehensive performance metrics:

**Required metrics:**
- Total return (%)
- Sharpe ratio (annualized, risk-free rate = 4%)
- Sortino ratio
- Maximum drawdown (% and duration in days)
- Win rate (% of profitable trades)
- Profit factor (gross profit / gross loss)
- Average trade duration
- Best and worst trade

**Breakdown metrics:**
- Performance by market regime (trending vs ranging)
- Performance by symbol
- Performance by day of week
- Monthly returns

### Flexibility [guided]
If you identify additional metrics that would be valuable for investor 
reporting, include them. Standard quantitative finance metrics preferred.

### Save as
`/tmp/workflow/step2_metrics.json`

### Success criteria
- All required metrics are present
- Sharpe ratio is between -5 and 5 (sanity check)
- Maximum drawdown is between 0% and 100%
- Win rate is between 0% and 100%
- No NaN or infinite values

### Constraints
- Use standard financial formulas (no custom risk metrics)
- Annualize all ratios using 252 trading days

### If something goes wrong
- Division by zero (no losing trades) → set profit factor to infinity, note in output
- Insufficient data for regime analysis → skip that breakdown, document why

---

## Step 3: Benchmark Comparison

### Dependencies
```bash
pip install yfinance matplotlib --break-system-packages
```

### Task
Compare strategy performance against relevant benchmarks:

1. Download S&P 500 (^GSPC) data for the same period
2. Download relevant currency/commodity indices based on traded symbols
3. Calculate benchmark metrics: total return, Sharpe ratio, max drawdown
4. Create equity curve comparison chart

The chart should show:
- Strategy equity curve (normalized to 100 at start)
- S&P 500 equity curve (normalized)
- Drawdown subplot below

### Flexibility [guided]
You may add additional relevant benchmarks if the strategy trades specific 
asset classes. For forex-heavy strategies, consider DXY. For commodities, 
consider relevant commodity indices.

### Save as
- `/tmp/workflow/step3_comparison.json` (benchmark metrics)
- `/tmp/workflow/step3_equity_curve.png` (chart, 1200x800px minimum)

### Success criteria
- Both output files exist
- Comparison JSON contains benchmark metrics matching strategy period
- Chart is readable and properly labeled
- Legend clearly identifies each line

### If something goes wrong
- Yahoo Finance unavailable → use alternative data source (Alpha Vantage, FRED)
- Benchmark data missing dates → use nearest available dates, note in output
- Chart generation fails → save raw data, skip visualization

---

## Step 4: Risk Analysis

### Task
Perform detailed risk analysis:

1. **Value at Risk (VaR)** at 95% and 99% confidence levels
2. **Expected Shortfall (CVaR)** at same levels
3. **Correlation analysis** with benchmarks
4. **Drawdown analysis**: 
   - List all drawdowns > 5%
   - Average recovery time
   - Current drawdown status

5. **Concentration risk**:
   - Exposure by symbol
   - Exposure by direction (long/short bias)

### Save as
`/tmp/workflow/step4_risk.json`

### Success criteria
- VaR values are negative (representing potential loss)
- CVaR is more negative than VaR (by definition)
- All percentage values are between -100% and 100%

---

## Step 5: Generate Investor Report

### Dependencies
```bash
pip install weasyprint jinja2 --break-system-packages
```

### Task
Create a professional investor report (PDF) combining all previous analysis.

**Report structure:**
1. **Executive Summary** (1 paragraph)
   - Key performance number
   - Comparison to benchmark
   - One-sentence risk assessment

2. **Performance Overview** (1 page)
   - Key metrics table
   - Monthly returns heatmap or table
   - Equity curve chart

3. **Risk Analysis** (0.5 page)
   - VaR/CVaR summary
   - Maximum drawdown details
   - Concentration risks if any

4. **Benchmark Comparison** (0.5 page)
   - Side-by-side metrics table
   - Relative performance commentary

5. **Appendix** (optional)
   - Detailed trade statistics
   - Methodology notes

### Flexibility [autonomous]
Design and layout are entirely up to you. The report should be:
- Professional enough for institutional investors
- Clear enough for someone without deep finance background
- Visually appealing but not flashy

### Constraints
- Maximum 5 pages total
- No raw trade data (privacy)
- Include disclaimer: "Past performance does not guarantee future results"
- Include generation timestamp

### Save as
`/tmp/workflow/mbm_q4_2024_report.pdf`

### Success criteria
- PDF opens correctly in standard readers
- All sections from structure are present
- File size under 10MB
- No placeholder text or TODOs visible

---

## Finalization

### After completion
1. Copy all artifacts to `/home/user/outputs/trading-analysis/`
2. Create `manifest.json` with:
   - List of all generated files with sizes
   - Execution timestamp
   - Any deviations from the workflow
3. Archive raw data: `tar -czf raw_data.tar.gz step1_trades.parquet`

### Notification
Provide a summary including:
- Strategy performance (return, Sharpe)
- How it compared to S&P 500
- Location of the final report
- Any issues encountered during execution

### If any step failed
- Save partial results with `_partial` suffix
- Document which steps completed in `execution_log.md`
- Still generate report with available data, marking missing sections
