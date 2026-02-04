# Getting Started with IntentFlow

This guide will help you write your first IntentFlow workflow in 10 minutes.

## What You'll Need

- A text editor (VS Code, Sublime, or even Notepad)
- An LLM with tool access (Claude with computer use, GPT-4 with functions, etc.)
- Basic understanding of what you want to automate

## Your First Workflow

Let's create a simple workflow that downloads data, processes it, and generates a report.

### Step 1: Create the File

Create a new file called `my-first-workflow.md`:

```markdown
# Workflow: Daily Weather Report

## Meta
version: 1.0
estimated_time: 5 minutes

## Context
Fetch weather data and create a simple summary report.
```

### Step 2: Add Your First Step

```markdown
---

## Step 1: Fetch Weather Data

### Task
Get the current weather for San Francisco from any free weather API.
Save the temperature, conditions, and humidity.

### Save as
`/tmp/workflow/weather.json`

### Success criteria
- File contains temperature (in Fahrenheit)
- File contains current conditions (sunny, cloudy, etc.)
- File contains humidity percentage
```

Notice how we describe WHAT we want, not HOW to get it. The LLM will figure out which API to use.

### Step 3: Add Processing Step

```markdown
---

## Step 2: Generate Report

### Task
Create a simple text report with:
- Current temperature and conditions
- A recommendation (umbrella, sunscreen, jacket)
- Tomorrow's outlook if available

### Flexibility
Format the report however you think is most readable.

### Save as
`/tmp/workflow/weather_report.txt`

### Success criteria
- File exists and is readable
- Contains all requested information
```

### Step 4: Add Finalization

```markdown
---

## Finalization

### After completion
Display the contents of the report.

### If something goes wrong
Show what data was retrieved and where the error occurred.
```

### Complete Example

Here's the complete workflow:

```markdown
# Workflow: Daily Weather Report

## Meta
version: 1.0
estimated_time: 5 minutes

## Context
Fetch weather data and create a simple summary report.

---

## Step 1: Fetch Weather Data

### Task
Get the current weather for San Francisco from any free weather API.
Save the temperature, conditions, and humidity.

### Save as
`/tmp/workflow/weather.json`

### Success criteria
- File contains temperature (in Fahrenheit)
- File contains current conditions (sunny, cloudy, etc.)
- File contains humidity percentage

---

## Step 2: Generate Report

### Task
Create a simple text report with:
- Current temperature and conditions
- A recommendation (umbrella, sunscreen, jacket)
- Tomorrow's outlook if available

### Flexibility
Format the report however you think is most readable.

### Save as
`/tmp/workflow/weather_report.txt`

### Success criteria
- File exists and is readable
- Contains all requested information

---

## Finalization

### After completion
Display the contents of the report.

### If something goes wrong
Show what data was retrieved and where the error occurred.
```

## Running Your Workflow

Simply provide the workflow to your LLM:

> "Please execute this workflow: [paste workflow]"

Or if the LLM has file access:

> "Please execute the workflow in my-first-workflow.md"

The LLM will:
1. Read and understand the workflow
2. Execute each step in order
3. Verify success criteria
4. Handle any errors according to your instructions
5. Provide the finalization summary

## Key Concepts Recap

| Concept | Purpose |
|---------|---------|
| **Task** | What to accomplish (required) |
| **Save as** | Output file path (creates contract between steps) |
| **Success criteria** | How to verify completion |
| **Flexibility** | Where the LLM can improvise |
| **If something goes wrong** | Fallback strategies |

## Next Steps

- Read the [full specification](../SPEC.md) for all available sections
- Explore [examples](../examples/) for more complex workflows
- Learn about [flexibility patterns](flexibility-patterns.md)
- Set up [validation](../tools/validator/) for your workflows

## Tips for Writing Good Workflows

1. **Start simple** — Add complexity only when needed
2. **Be specific about outputs** — Vague success criteria lead to inconsistent results
3. **Use flexibility intentionally** — Don't make everything autonomous
4. **Test incrementally** — Run partial workflows to verify each step
5. **Document your intent** — Future you (or others) will thank you

## Common Mistakes

❌ **Too vague:**
```markdown
### Task
Do the data analysis.
```

✅ **Better:**
```markdown
### Task
Calculate the average, median, and standard deviation of the 'price' column.
Group results by 'category'.
```

❌ **Over-specified:**
```markdown
### Task
Use requests library to call api.weather.gov endpoint /points/37.7749,-122.4194
then parse the JSON response using json.loads() and extract the 'temperature' key...
```

✅ **Better:**
```markdown
### Task
Get current weather for San Francisco (37.7749, -122.4194).
Extract temperature and conditions.
```

The goal is to specify WHAT you need clearly, while leaving HOW to the LLM's judgment.
