# IntentFlow

**MCP & Skills orchestration in plain Markdown**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Spec Version](https://img.shields.io/badge/spec-v0.1-blue.svg)](SPEC.md)
[![GitHub](https://img.shields.io/github/stars/PavelRavvich/intentflow?style=social)](https://github.com/PavelRavvich/intentflow)
[![Docs](https://img.shields.io/badge/docs-website-blue)](https://pavelravvich.github.io/intentflow/)

📖 **Documentation:** [pavelravvich.github.io/intentflow](https://pavelravvich.github.io/intentflow/)

---

## What is IntentFlow?

IntentFlow is a specification for writing workflows that are:
- **Readable by humans** — plain Markdown, no code required
- **Executable by LLMs** — structured enough for AI agents to follow
- **Flexible by design** — explicitly define where AI can improvise

```markdown
## Step 1: Fetch Data

### Task
Download all transactions from the payment API for last month.
Handle pagination automatically.

### Flexibility
If the API is slow, you may batch requests or add delays as needed.

### Save as
`/tmp/workflow/transactions.json`

### Success criteria
- File exists and is valid JSON
- Contains at least 100 records
- All records have `id`, `amount`, `timestamp` fields
```

## The Problem

| Approach | Issue |
|----------|-------|
| Traditional scripts | Brittle, no adaptability |
| LangChain/DSPy | Requires Python expertise |
| AutoGPT-style | Too autonomous, unpredictable |
| Plain prompts | No structure, not reusable |

**IntentFlow sits in the sweet spot:**

```
Rigid Scripts ←————— IntentFlow ——————→ Full Autonomy
(Airflow)           structured          (AutoGPT)
                    flexibility
```

## MCP & Skills Orchestration

IntentFlow can orchestrate AI tooling — install MCP servers, load Skills, and chain them in workflows:

```markdown
## Step 1: Setup Database
### Dependencies
```bash
npm install -g @anthropic/mcp-server-postgres
```

## Step 2: Query Data
### Task
Using the Postgres MCP, fetch all orders from last month...

## Step 3: Generate Report  
### Dependencies
Read skill at `/mnt/skills/public/docx/SKILL.md`

### Task
Following the docx skill, create a Word report...
```

See [MCP Orchestration Guide](docs/mcp-orchestration.md) for details.

## Key Concepts

### 1. Intent over Implementation

You describe **what** you want, not **how** to do it:

```markdown
### Task
Analyze sentiment of customer reviews and categorize them.
```

The LLM chooses the implementation — API calls, local models, heuristics.

### 2. Graduated Flexibility

Explicitly mark where AI can deviate:

```markdown
### Flexibility [autonomous]
Choose any visualization library. 
Add extra charts if they help tell the story.
```

Flexibility levels:
- `[strict]` — follow exactly as written
- `[guided]` — work within defined boundaries (default)
- `[autonomous]` — only the goal matters, means are up to you

### 3. Contract-Based Steps

Steps communicate through files, not code:

```
Step 1: Save as → /tmp/data.json
Step 2: (implicitly reads /tmp/data.json)
```

### 4. Failure Strategies in Natural Language

```markdown
### If something goes wrong
- API returns 429 → wait 60 seconds and retry
- No data found → expand date range to 3 months, note in report
- Unknown error → stop and ask for guidance
```

## Quick Start

### 1. Write a workflow

Create `my-workflow.md`:

```markdown
# Workflow: Daily Report

## Meta
version: 1.0
estimated_time: 10 minutes

## Step 1: Gather metrics

### Task
Query the database for yesterday's sales metrics.
Calculate total revenue, order count, and average order value.

### Save as
`/tmp/workflow/metrics.json`

### Success criteria
- All three metrics are present
- Revenue is a positive number

## Step 2: Generate report

### Dependencies
```bash
pip install matplotlib
```

### Task
Create a one-page PDF report with the metrics.
Include a simple bar chart comparing to last week.

### Save as
`/tmp/workflow/daily-report.pdf`
```

### 2. Validate (optional)

```bash
python tools/validator/validate.py my-workflow.md
```

### 3. Execute with your LLM

Feed the workflow to Claude, GPT-4, or any capable LLM with tool access.

## Examples

- [Trading Strategy Analysis](examples/trading-analysis.md) — financial data pipeline
- [Data Processing Pipeline](examples/data-pipeline.md) — ETL with flexibility
- [Content Generation](examples/content-generation.md) — multi-step content creation

## Specification

See [SPEC.md](SPEC.md) for the complete specification.

## Tools

- **[Validator](tools/validator/)** — CLI tool to validate workflow syntax
- **VSCode Extension** — syntax highlighting (coming soon)
- **Converters** — export to LangChain, Prefect (coming soon)

## Philosophy

> "The best workflow is one that a junior can read and an AI can execute."

IntentFlow is not about replacing programmers. It's about:
- Documenting processes in executable form
- Giving non-developers a way to automate complex tasks
- Providing guardrails for AI agents without micromanaging

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas where help is needed:
- More examples from different domains
- Runner implementations for various LLMs
- IDE integrations
- Translations of documentation

## License

MIT License — see [LICENSE](LICENSE) for details.

## Acknowledgments

Inspired by the gap between "write code for everything" and "let AI figure it out".
Built for the era of capable AI agents that need structure, not micromanagement.

---

**Star this repo** if you believe workflows should be human-first! ⭐
