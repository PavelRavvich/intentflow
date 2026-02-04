# IntentFlow Specification v0.1

## Abstract

IntentFlow is a Markdown-based specification for defining workflows that can be executed by Large Language Models (LLMs). It bridges the gap between rigid scripted automation and fully autonomous AI agents by providing structured intent with controlled flexibility.

## Design Principles

1. **Human-first** — A workflow should be readable by someone with no programming experience
2. **Executable** — Structure must be consistent enough for LLM parsing
3. **Flexible** — Explicitly define where deviation is allowed
4. **Portable** — Plain Markdown, no proprietary formats
5. **Composable** — Steps communicate through files, enabling loose coupling

## Document Structure

```
# Workflow: {Title}

## Meta
{metadata key-value pairs}

## Context
{background information for the executor}

---

## Step {N}: {Step Title}
{step content}

---

## Finalization
{cleanup and output instructions}
```

## Meta Section

Optional metadata about the workflow.

```markdown
## Meta
version: 1.0
author: John Doe
requires: Claude with computer use
estimated_time: 30 minutes
tags: data, analysis, reporting
```

### Reserved Keys

| Key | Description |
|-----|-------------|
| `version` | Workflow version (semver recommended) |
| `author` | Creator of the workflow |
| `requires` | Runtime requirements |
| `estimated_time` | Expected execution time |
| `tags` | Comma-separated categorization |

## Context Section

Optional background information that helps the executor understand the purpose and constraints.

```markdown
## Context
This workflow processes customer feedback data to identify trends.
The data comes from our CRM system and may contain PII.
Final report goes to the marketing team weekly.
```

## Step Structure

Each step MUST contain a `Task` section. All other sections are optional.

### Required Sections

#### Task

The core instruction. Describes WHAT to accomplish, not HOW.

```markdown
### Task
Fetch all customer reviews from the past 30 days.
Extract the review text, rating, and timestamp.
Handle pagination if the API returns partial results.
```

**Guidelines:**
- Use imperative mood ("Fetch", "Calculate", "Generate")
- Focus on outcomes, not implementation
- Be specific about data requirements
- One logical unit of work per step

### Optional Sections

#### Dependencies

Tools, packages, or services required for this step.

```markdown
### Dependencies
```bash
pip install pandas numpy --break-system-packages
npm install -g @anthropic/mcp-server-postgres
```
```

**Guidelines:**
- Use standard package managers
- Include version constraints for reproducibility
- List MCP servers or external tools if needed

#### Configuration

Setup instructions or environment details.

```markdown
### Configuration
- Database host: Use `DB_HOST` environment variable
- API endpoint: https://api.example.com/v2
- Create temp directory at `/tmp/workflow/` if not exists
```

#### Save As

Output file path. Creates a contract for subsequent steps.

```markdown
### Save as
`/tmp/workflow/reviews.parquet`
```

**Guidelines:**
- Use absolute paths for clarity
- Prefer structured formats (JSON, Parquet) over plain text
- One primary output per step (additional files can be noted in Task)

#### Success Criteria

Verifiable conditions that indicate step completion.

```markdown
### Success criteria
- Output file exists and is valid JSON
- Contains at least 100 records
- No null values in required fields: `id`, `timestamp`, `amount`
- All timestamps are within the specified date range
```

**Guidelines:**
- Must be programmatically verifiable
- Include both existence and validity checks
- Specify reasonable bounds for numeric values

#### Flexibility

Explicit permission to deviate from instructions.

```markdown
### Flexibility
If the primary API is unavailable, you may use the backup endpoint.
Additional data enrichment is welcome if it improves the analysis.
```

See [Flexibility Levels](#flexibility-levels) for detail.

#### Constraints

Hard limits that MUST NOT be violated.

```markdown
### Constraints
- Do not make more than 100 API calls per minute
- Output file must not exceed 50MB
- Do not include any PII in logs or error messages
```

#### If Something Goes Wrong

Fallback strategies for common failure modes.

```markdown
### If something goes wrong
- API returns 429 → wait 60 seconds, then retry up to 3 times
- No data in date range → expand to 90 days, document the change
- Invalid JSON response → log the raw response, skip to next page
- Unknown error → stop execution and report the issue
```

**Guidelines:**
- Use format: `condition → action`
- Cover likely failure modes
- Include a catch-all for unexpected errors

## Flexibility Levels

Flexibility can be specified with a level marker:

```markdown
### Flexibility [level]
```

### Levels

#### `[strict]`

No deviation allowed. Execute exactly as specified.

```markdown
### Flexibility [strict]
Use exactly the columns specified. Do not add or remove any fields.
```

#### `[guided]` (default)

Work within defined boundaries. The executor may choose implementation details but must achieve the stated goal.

```markdown
### Flexibility [guided]
You may use any HTTP library. Caching is optional but recommended.
```

#### `[autonomous]`

Only the goal matters. The executor has full discretion over approach.

```markdown
### Flexibility [autonomous]
Create visualizations that best represent the data.
Use any tools, libraries, or approaches you think are appropriate.
```

## Step Linking

Steps are connected through the file system.

```markdown
## Step 1: Extract
### Save as
`/tmp/workflow/raw_data.json`

---

## Step 2: Transform
### Task
Load the data from the previous step and normalize all timestamps to UTC.
```

The executor infers that Step 2 reads from `/tmp/workflow/raw_data.json`.

### Explicit References

For clarity, you may explicitly reference previous outputs:

```markdown
### Task
Using the metrics from Step 2 (`/tmp/workflow/metrics.json`),
generate a summary report.
```

## Finalization Section

Optional cleanup and output instructions.

```markdown
## Finalization

### After completion
1. Move all artifacts to `/home/user/outputs/`
2. Create `manifest.json` listing all generated files
3. Clean up temporary files in `/tmp/workflow/`

### Notification
Summarize what was accomplished and where outputs are located.

### If any step failed
Document which steps completed, which failed, and why.
Partial results should still be saved with clear naming: `*_partial.*`
```

## File Format

- **Extension**: `.md` or `.workflow.md`
- **Encoding**: UTF-8
- **Line endings**: LF (Unix-style)

## Validation Rules

A valid IntentFlow document MUST:

1. Have a level-1 heading as the title
2. Have at least one Step section
3. Each Step MUST have a `Task` subsection
4. Step numbers should be sequential (gaps allowed but not recommended)

A valid IntentFlow document SHOULD:

1. Include `Save as` for steps that produce output
2. Include `Success criteria` for verification
3. Use consistent heading levels

## Example

```markdown
# Workflow: Weekly Sales Report

## Meta
version: 1.0
author: Analytics Team
estimated_time: 15 minutes

## Context
Generate the weekly sales report for stakeholders.
Data comes from the sales database, report goes to #sales-reports Slack channel.

---

## Step 1: Query Sales Data

### Dependencies
```bash
pip install psycopg2-binary pandas --break-system-packages
```

### Task
Connect to the sales database and extract:
- Total revenue by product category
- Number of orders by region  
- Top 10 customers by spend

Date range: last 7 days (Monday to Sunday).

### Save as
`/tmp/workflow/sales_data.json`

### Success criteria
- File contains all three data sections
- Revenue values are positive numbers
- At least 1 order exists (otherwise report is empty)

### If something goes wrong
- Database connection fails → check VPN, retry in 30 seconds
- No orders in range → generate empty report with explanation

---

## Step 2: Generate Report

### Task
Create a professional PDF report including:
- Executive summary (3-4 sentences)
- Revenue breakdown chart (bar chart by category)
- Regional performance table
- Top customers list

### Flexibility [guided]
Chart styling and exact layout are up to you.
Additional insights are welcome if the data suggests them.

### Constraints
- Maximum 3 pages
- No customer PII (names okay, no emails/phones)

### Save as
`/tmp/workflow/weekly_sales_report.pdf`

### Success criteria
- PDF is valid and opens correctly
- All sections from Task are present
- File size under 5MB

---

## Finalization

### After completion
Copy the report to `/home/user/reports/weekly/`
with filename `sales_report_YYYY-MM-DD.pdf`

### Notification
Provide a brief summary of key metrics and confirm the report location.
```

## Versioning

This specification follows [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes to document structure
- MINOR: New optional features
- PATCH: Clarifications and typo fixes

## Changelog

### v0.1 (2025-02-04)
- Initial specification release
- Core sections: Task, Dependencies, Save as, Success criteria, Flexibility, Constraints, If something goes wrong
- Flexibility levels: strict, guided, autonomous
- File-based step linking
