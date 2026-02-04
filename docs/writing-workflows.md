# Writing Effective Workflows

This guide covers best practices for writing IntentFlow workflows that are reliable, maintainable, and get consistent results.

## The Anatomy of a Good Step

A well-written step balances clarity with flexibility:

```markdown
## Step N: Descriptive Title

### Dependencies (optional)
What to install before this step runs.

### Task
Clear description of what to accomplish.

### Save as
Output file path.

### Success criteria
How to verify the step completed correctly.

### Flexibility (optional)
Where the executor can make decisions.

### If something goes wrong (optional)
Fallback strategies for common failures.
```

## Writing Good Tasks

### Be Outcome-Oriented

Focus on results, not implementation:

```markdown
# ❌ Implementation-focused
### Task
Use pandas read_csv to load data.csv into a DataFrame.
Then use df.groupby('category').mean() to calculate averages.
Save using df.to_json().

# ✅ Outcome-focused
### Task
Load the sales data and calculate average revenue by category.
```

### Be Specific About Data

Ambiguity leads to inconsistent results:

```markdown
# ❌ Ambiguous
### Task
Get the important metrics from the data.

# ✅ Specific
### Task
Extract the following metrics:
- Total revenue (sum of 'amount' column)
- Order count (number of rows)
- Average order value (revenue / count)
- Top 5 products by revenue
```

### Use Imperative Mood

Write commands, not descriptions:

```markdown
# ❌ Descriptive
### Task
The system should fetch user data and transform it.

# ✅ Imperative
### Task
Fetch user data from the API.
Transform timestamps to ISO format.
Remove duplicate entries.
```

## Defining Success Criteria

Good success criteria are verifiable:

### Existence Checks

```markdown
### Success criteria
- Output file exists
- File is valid JSON/Parquet/CSV
- File size > 0 bytes
```

### Content Checks

```markdown
### Success criteria
- Contains minimum 100 records
- No null values in required columns: id, timestamp, amount
- All timestamps are valid ISO dates
```

### Validity Bounds

```markdown
### Success criteria
- Percentages are between 0 and 100
- Dates are within expected range (2024-01-01 to present)
- No negative amounts
```

### Relationship Checks

```markdown
### Success criteria
- Output row count matches input
- Sum of parts equals total
- No orphaned foreign keys
```

## Using Flexibility Effectively

### When to Use [strict]

Use for regulatory, security, or exact-format requirements:

```markdown
### Flexibility [strict]
Output must contain exactly these columns in this order:
id, timestamp, amount, currency, status
Do not add, remove, or rename columns.
```

### When to Use [guided] (default)

Use when the goal is clear but implementation can vary:

```markdown
### Flexibility [guided]
Use any charting library. Colors should be professional.
Include a legend if it improves readability.
```

### When to Use [autonomous]

Use when you trust the executor's judgment completely:

```markdown
### Flexibility [autonomous]
Create visualizations that best tell the story of this data.
Add context, annotations, or additional analysis as you see fit.
```

### Flexibility Anti-Patterns

```markdown
# ❌ Flexibility without bounds
### Flexibility [autonomous]
Do whatever you want.

# ✅ Flexibility with intent
### Flexibility [autonomous]
Design the report layout for maximum clarity.
Target audience: executives with 30 seconds to scan.
```

## Handling Failures

### Be Specific About Conditions

```markdown
# ❌ Vague
### If something goes wrong
Try again or skip.

# ✅ Specific
### If something goes wrong
- HTTP 429 (rate limit) → wait 60 seconds, retry up to 3 times
- HTTP 401 (auth error) → stop execution, report credentials issue
- Empty response → expand date range by 7 days, retry once
- Other errors → log error details, continue to next step
```

### Include a Catch-All

Always have a fallback for unexpected errors:

```markdown
### If something goes wrong
- Connection timeout → retry with exponential backoff
- Invalid data format → skip record, log issue
- Any other error → stop and report for human review
```

### Distinguish Recoverable vs Fatal

```markdown
### If something goes wrong
**Recoverable (retry):**
- Network timeouts
- Rate limiting
- Temporary service unavailability

**Fatal (stop execution):**
- Authentication failure
- Permission denied
- Data corruption detected
```

## Step Dependencies

### Implicit Dependencies (via Files)

Steps automatically depend on previous outputs:

```markdown
## Step 1: Extract
### Save as
`/tmp/data/raw.json`

## Step 2: Transform
### Task
Load the extracted data and normalize...
# ↑ Implicitly depends on Step 1's output
```

### Explicit References

For clarity, reference files directly:

```markdown
## Step 3: Analyze
### Task
Using the transformed data from Step 2 (`/tmp/data/clean.json`),
calculate the following metrics...
```

### Parallel-Safe Steps

Mark steps that don't depend on each other:

```markdown
## Step 2a: Fetch Stock Data
### Save as
`/tmp/data/stocks.json`

## Step 2b: Fetch Crypto Data  
### Save as
`/tmp/data/crypto.json`
# Note: Steps 2a and 2b can run in parallel

## Step 3: Combine Data
### Task
Merge data from both previous steps...
```

## Organizing Complex Workflows

### Use Clear Section Breaks

```markdown
---

## Step 3: Data Transformation

---
```

### Group Related Steps

```markdown
# --- DATA ACQUISITION ---

## Step 1: Fetch Source A
...

## Step 2: Fetch Source B
...

# --- PROCESSING ---

## Step 3: Merge Sources
...
```

### Keep Steps Focused

One logical unit of work per step:

```markdown
# ❌ Too much in one step
## Step 1: Get Data, Clean It, Transform It, and Generate Report

# ✅ Properly separated
## Step 1: Fetch Raw Data
## Step 2: Clean and Validate
## Step 3: Transform for Analysis
## Step 4: Generate Report
```

## Documentation Best Practices

### Context Section

Provide background that helps with decision-making:

```markdown
## Context
This workflow runs weekly as part of the finance reporting cycle.
Data comes from the ERP system and feeds into the CFO dashboard.
Historical quirk: The "pending" status actually means "approved" due to 
a legacy system migration in 2019.
```

### Inline Comments

Add context within tasks when helpful:

```markdown
### Task
Calculate customer lifetime value.
# Note: Use 12-month window, not all-time, per finance team request
Group by customer segment for the report.
```

### Meta Section

Document authorship and versioning:

```markdown
## Meta
version: 2.1
author: Data Engineering Team
last_updated: 2025-01-15
changelog: Added currency conversion step, fixed timezone handling
```

## Testing Workflows

### Start with Dry Runs

Ask the LLM to explain what it would do:

> "Review this workflow and explain what you would do at each step, without executing."

### Test Steps Individually

Run one step at a time to verify:

> "Execute only Step 1 of this workflow."

### Use Sample Data

For destructive operations, test with samples:

```markdown
### Configuration
# For testing: use sample database `test_db` instead of `production`
Database: Use DB_NAME environment variable (default: production)
```

### Validate Outputs

Always check outputs match expectations before proceeding:

```markdown
### Success criteria
- Compare row count with source: must match within 1%
- Verify no data loss: all source IDs present in output
```
