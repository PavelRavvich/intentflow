# Flexibility Patterns

This guide covers patterns for effectively using flexibility in IntentFlow workflows. The key insight: flexibility isn't about being vague—it's about being intentional about where decisions should be made.

## The Flexibility Spectrum

```
[strict] ←————————————————————————→ [autonomous]
"Do exactly this"            "Achieve this goal"

More predictable              More adaptive
Less resilient               More resilient  
Easier to debug              Harder to debug
```

## Pattern 1: Bounded Autonomy

Give freedom within explicit limits.

### Example: Chart Design

```markdown
### Task
Create a visualization of monthly revenue trends.

### Flexibility [autonomous]
Design the chart for maximum clarity. You may choose:
- Chart type (line, bar, area)
- Color scheme
- Annotations and callouts

### Constraints
- Must include data labels
- Must be readable in grayscale (for printing)
- Maximum 2 y-axes
```

### When to Use
- Creative tasks (design, writing)
- Implementation choices that don't affect outcomes
- When you trust the executor's judgment

## Pattern 2: Fallback Chain

Define a sequence of alternatives.

### Example: Data Source Priority

```markdown
### Task
Fetch current stock prices for the watchlist.

### Flexibility [guided]
Use data sources in this priority order:
1. Bloomberg API (preferred, most accurate)
2. Yahoo Finance (good fallback)
3. Alpha Vantage (free tier, slower)

Move to next source only if current source fails.
Document which source was actually used.
```

### When to Use
- External dependencies that may fail
- Multiple valid approaches with different tradeoffs
- Graceful degradation scenarios

## Pattern 3: Quality Gates

Provide minimum requirements, allow exceeding them.

### Example: Content Generation

```markdown
### Task
Write an executive summary of the quarterly results.

### Flexibility [guided]
**Minimum requirements:**
- 150-200 words
- Cover: revenue, costs, net income
- Professional tone

**You may also include (if valuable):**
- YoY comparison
- Notable one-time items
- Forward guidance summary

Don't exceed 300 words total.
```

### When to Use
- When you have minimum viable output defined
- When additional work might add value
- When you want to encourage "going above and beyond"

## Pattern 4: Decision Points

Mark explicit choices for the executor.

### Example: Error Handling Strategy

```markdown
### Task
Process all records from the input file.

### Flexibility [guided]
**Decision point: How to handle invalid records?**

Option A: Skip invalid, continue processing (faster, loses data)
Option B: Stop on first error (safer, may not complete)
Option C: Quarantine invalid to separate file (balanced)

Choose based on data quality observed in first 100 records.
Document your choice and reasoning.
```

### When to Use
- When optimal choice depends on runtime conditions
- When you want to delegate judgment calls
- When documenting the decision matters

## Pattern 5: Scoped Creativity

Allow creativity in specific areas only.

### Example: Report Generation

```markdown
### Task
Generate the monthly performance report.

### Flexibility
**Fixed elements (do not change):**
- Section order (Executive Summary → Details → Appendix)
- Data sources (use only validated metrics from Step 2)
- Disclaimer text (use standard legal disclaimer)

**Creative freedom:**
- Visual design and layout
- Chart types and colors
- Section introductions and transitions
- Use of icons or visual elements

[strict] for content accuracy, [autonomous] for presentation.
```

### When to Use
- When some elements are non-negotiable (legal, compliance)
- When you want consistent structure with fresh presentation
- When separating "what" from "how it looks"

## Pattern 6: Progressive Disclosure

Start specific, allow expansion.

### Example: Data Analysis

```markdown
### Task
Analyze the sales data.

**Required analysis:**
1. Total revenue by region
2. Top 10 products by units sold
3. Month-over-month growth rate

### Flexibility [guided]
If you discover interesting patterns not covered above, you may:
- Add up to 3 additional analyses
- Include them in a "Additional Insights" section
- Each must include: finding, supporting data, potential action

Don't let additional analysis delay the required deliverables.
```

### When to Use
- When you expect the executor might find valuable insights
- When you want to encourage exploration without mandating it
- When core requirements must be met first

## Pattern 7: Conditional Flexibility

Flexibility that depends on conditions.

### Example: API Selection

```markdown
### Task
Translate the document from English to Spanish.

### Flexibility [guided]
**If document < 1000 words:**
Use any translation service. Speed over cost.

**If document 1000-10000 words:**
Use DeepL or Google Translate. Balance quality and cost.

**If document > 10000 words:**
Use the most cost-effective option. Consider chunking.
Provide cost estimate before proceeding.
```

### When to Use
- When optimal approach varies by input characteristics
- When different scenarios warrant different tradeoffs
- When you want to encode decision logic naturally

## Pattern 8: Documented Deviation

Allow deviation but require documentation.

### Example: ETL Pipeline

```markdown
### Task
Transform the data according to the schema mapping.

### Flexibility [guided]
You may deviate from the standard mapping if:
- Source data structure differs from documentation
- Data quality issues require additional cleaning
- Performance optimization requires different approach

**Required for any deviation:**
1. Document what was changed
2. Explain why standard approach didn't work
3. Note any implications for downstream processes

Save deviation log to `/tmp/workflow/deviations.md`
```

### When to Use
- When following spec exactly might not be possible
- When you need audit trail for changes
- When deviations have implications for other systems

## Anti-Patterns to Avoid

### Fake Flexibility

```markdown
# ❌ Flexibility that isn't really flexible
### Flexibility [autonomous]
Use your judgment, but make sure to:
- Use pandas (not polars or duckdb)
- Save as CSV (not parquet or JSON)
- Include exactly these 15 columns
- Format dates as YYYY-MM-DD
```

This is [strict] pretending to be [autonomous].

### Unbounded Autonomy

```markdown
# ❌ No guidance at all
### Flexibility [autonomous]
Do whatever you think is best.
```

Even autonomous tasks need success criteria or goals.

### Hidden Requirements

```markdown
# ❌ Requirements buried in flexibility
### Flexibility [guided]
Feel free to be creative with the analysis,
but by the way it absolutely must include 
correlation analysis and must use matplotlib.
```

Put requirements in Task or Constraints, not Flexibility.

## Choosing the Right Level

Ask yourself:

| Question | If Yes | If No |
|----------|--------|-------|
| Is there only one correct way? | [strict] | → |
| Does compliance/legal care? | [strict] | → |
| Are there multiple valid approaches? | [guided] | → |
| Does the outcome matter more than method? | [autonomous] | → |
| Do I need predictable results? | [strict] or [guided] | → |
| Is this creative work? | [autonomous] | → |

## Combining Levels in One Step

You can mix levels for different aspects:

```markdown
### Task
Generate quarterly investor presentation.

### Flexibility
**Data accuracy: [strict]**
Numbers must match audited financials exactly.
No rounding unless specified.

**Visual design: [autonomous]**
Create compelling, professional visuals.
Chart types and layouts at your discretion.

**Narrative: [guided]**
Cover required topics (revenue, expenses, outlook).
Additional context welcome if it aids understanding.
```

This gives tight control where it matters (data) and freedom where it adds value (design).
