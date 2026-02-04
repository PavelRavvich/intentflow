---
layout: default
title: Home
---

# IntentFlow

**Human-readable, LLM-executable workflow specification**

---

IntentFlow is a Markdown-based format for writing workflows that both humans can read and AI agents can execute.

```markdown
## Step 1: Fetch Data

### Task
Download sales data for the last quarter.

### Flexibility [guided]
Use any API or database. Caching is optional.

### Save as
`/tmp/sales.json`

### Success criteria
- File contains at least 100 records
- All required fields present
```

## Why IntentFlow?

| Traditional Scripts | IntentFlow | Full Autonomy (AutoGPT) |
|---------------------|------------|-------------------------|
| Brittle, breaks easily | Adapts to conditions | Unpredictable |
| Requires programmer | Plain English | Hard to control |
| No flexibility | Controlled flexibility | Too much freedom |

## Key Features

**🎯 Intent over Implementation** — Describe what you want, not how to do it

**📊 Graduated Flexibility** — Mark exactly where AI can improvise: `[strict]`, `[guided]`, `[autonomous]`

**📄 Contract-based Steps** — Steps communicate through files, not code

**🔄 Failure Strategies** — Natural language fallbacks: "If X fails → try Y"

## Get Started

1. [Read the Spec](SPEC.md) — Full specification
2. [Getting Started](docs/getting-started.md) — Write your first workflow
3. [Examples](https://github.com/PavelRavvich/intentflow/tree/master/examples) — Real-world workflows

## Quick Example

```markdown
# Workflow: Daily Report

## Step 1: Gather Data
### Task
Query yesterday's metrics from the database.

### Save as
`/tmp/metrics.json`

## Step 2: Generate Report  
### Task
Create a PDF summary with charts.

### Flexibility [autonomous]
Design and layout at your discretion.

### Save as
`/tmp/report.pdf`
```

Then tell your LLM: *"Execute this workflow"*

## Links

- [GitHub Repository](https://github.com/PavelRavvich/intentflow)
- [Full Specification](SPEC.md)
- [Contributing](CONTRIBUTING.md)

---

MIT License · Created by [Pavel Ravvich](https://github.com/PavelRavvich)
