# MCP & Skills Orchestration

IntentFlow was designed with AI tooling orchestration in mind. Workflows can install, configure, and use MCP servers and Skills as part of their execution.

## The Problem

Modern AI agents have access to powerful tools:
- **MCP (Model Context Protocol)** — External capabilities (databases, APIs, browsers)
- **Skills** — Knowledge files that guide how to use tools effectively

But there's no standard way to:
- Chain multiple tools in a controlled sequence
- Install tools on-demand as part of a workflow
- Document the orchestration in a human-readable format

## IntentFlow as Orchestrator

IntentFlow bridges this gap by providing a declarative way to orchestrate AI tooling.

### Installing MCP Servers

```markdown
## Step 1: Setup Database Access

### Dependencies
```bash
npm install -g @anthropic/mcp-server-postgres
```

### Configuration
Create MCP config at `~/.config/claude/`:
- Host: Use `DB_HOST` environment variable
- Credentials: `DB_USER` / `DB_PASSWORD`

### Task
Verify connection by listing available tables.
```

### Using MCP in Workflows

```markdown
## Step 2: Query Customer Data

### Task
Using the Postgres MCP connection from Step 1:
- Query all customers created in the last 30 days
- Include their order history
- Calculate lifetime value

### Save as
`/tmp/workflow/customers.json`
```

### Combining MCP with Skills

```markdown
## Step 3: Generate Report

### Dependencies
Read the skill at `/mnt/skills/public/docx/SKILL.md`

### Task
Following the docx skill instructions, create a professional
Word document with:
- Customer acquisition summary
- Revenue breakdown chart
- Recommendations section

### Save as
`/tmp/workflow/customer_report.docx`
```

## Multi-Tool Pipelines

A workflow can orchestrate multiple MCP servers:

```markdown
# Workflow: Competitive Analysis

## Step 1: Web Research

### Dependencies
```bash
npx @anthropic/mcp-server-puppeteer
```

### Task
Using the browser MCP, visit competitor websites and extract:
- Pricing information
- Feature lists
- Recent announcements

### Save as
`/tmp/workflow/competitor_data.json`

---

## Step 2: Enrich with News

### Dependencies
```bash
pip install news-api-mcp --break-system-packages
```

### Task
Search for recent news about each competitor.
Add sentiment analysis for each article.

### Save as
`/tmp/workflow/competitor_news.json`

---

## Step 3: Store in Database

### Dependencies
```bash
npm install -g @anthropic/mcp-server-postgres
```

### Task
Insert the collected data into the `competitive_intel` table.
Update existing records if competitor already exists.

---

## Step 4: Generate Insights

### Task
Analyze the collected data and generate:
- Market positioning map
- Threat assessment
- Opportunity recommendations

### Flexibility [autonomous]
Use any visualization approach that best communicates the insights.

### Save as
`/tmp/workflow/competitive_analysis.pdf`
```

## Why This Matters

### Traditional Approach

```python
# Hard-coded, brittle, requires programmer
from mcp_postgres import connect
from mcp_browser import Browser
from news_api import search

db = connect(...)
browser = Browser()
# ... 200 lines of orchestration code
```

### IntentFlow Approach

```markdown
## Step 1: Get data from database
### Task
Query the sales table...

## Step 2: Enrich with web data  
### Task
Search for additional context...

## Step 3: Generate report
### Task
Create a summary...
```

The workflow is:
- **Readable** by non-programmers
- **Flexible** — AI chooses implementation details
- **Self-documenting** — the workflow IS the documentation
- **Adaptable** — AI handles edge cases

## Limitations

### MCP Registration Timing

Most MCP servers need to be registered at client startup, not mid-session. IntentFlow handles this by:

1. **Installation step** — Install the MCP server package
2. **Configuration step** — Generate necessary config files
3. **Session restart** — User restarts client (if required)
4. **Usage steps** — Workflow continues with MCP available

For MCP servers that work as CLI tools or HTTP services, no restart is needed.

### Skill Loading

Skills are loaded via the `view` tool at runtime. The workflow should explicitly instruct the LLM to read the skill before using it:

```markdown
### Dependencies
First, read the skill at `/mnt/skills/public/xlsx/SKILL.md`
```

## Best Practices

1. **Group related MCP setup** — Install and configure in the same step
2. **Verify before proceeding** — Add success criteria to confirm tools work
3. **Document tool requirements** — Use the Meta section to list required MCP servers
4. **Provide fallbacks** — If an MCP fails, specify alternatives

```markdown
## Meta
requires: Claude with computer use
mcp_servers: postgres, puppeteer, news-api

## Step 1: Setup
### If something goes wrong
- MCP not available → install it in Dependencies
- Connection failed → check credentials, retry once
- Still failing → skip this step, note in final report
```

## Examples

See complete examples:
- [Trading Analysis](../examples/trading-analysis.md) — Uses MT5 MCP for market data
- [Data Pipeline](../examples/data-pipeline.md) — PostgreSQL + BigQuery MCPs
- [Code Review](../examples/code-review.md) — GitHub MCP integration
