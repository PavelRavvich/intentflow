# Workflow: Automated Code Review

## Meta
version: 1.0
author: Engineering Team
requires: Claude with computer use, Git access
estimated_time: 15 minutes
tags: code, review, quality, automation

## Context
Perform automated code review on a pull request. This workflow analyzes code 
changes for quality, security, and best practices. It supplements (not replaces) 
human review by catching common issues early.

The output is a structured review report that can be posted as a PR comment.

---

## Step 1: Fetch PR Changes

### Dependencies
```bash
pip install PyGithub gitpython --break-system-packages
```

### Configuration
- Repository: Use `GITHUB_REPO` environment variable (format: owner/repo)
- PR Number: Use `PR_NUMBER` environment variable
- Token: Use `GITHUB_TOKEN` for API access

### Task
Fetch the pull request details and changed files:

1. Get PR metadata (title, description, author, base branch)
2. List all changed files with their diff status (added/modified/deleted)
3. Download the full content of modified and added files
4. Get the diff for each file

### Save as
`/tmp/workflow/step1_pr_data.json`

Structure:
```json
{
  "pr": {
    "number": 123,
    "title": "...",
    "description": "...",
    "author": "...",
    "base_branch": "main"
  },
  "files": [
    {
      "path": "src/utils.py",
      "status": "modified",
      "additions": 45,
      "deletions": 12,
      "content": "...",
      "diff": "..."
    }
  ]
}
```

### Success criteria
- PR metadata is complete
- All changed files are fetched
- File content is available for analysis
- Total diff size < 10MB (reasonable PR size)

### If something goes wrong
- PR not found → verify PR number, check if private repo needs auth
- Rate limited → wait 60 seconds, retry
- Large PR (>50 files) → focus on non-test files, note in report

---

## Step 2: Static Analysis

### Task
Perform static code analysis on changed files:

**For each file, check:**

1. **Code Style**
   - Consistent indentation
   - Line length (warn if >120 chars)
   - Naming conventions (snake_case for Python, camelCase for JS)

2. **Complexity**
   - Functions longer than 50 lines
   - Cyclomatic complexity > 10
   - Deeply nested code (>4 levels)

3. **Common Issues**
   - Unused imports
   - Unused variables
   - Hardcoded credentials or secrets
   - TODO/FIXME comments
   - Print/console.log statements (debug code)

4. **Documentation**
   - Public functions without docstrings
   - Complex logic without comments

### Flexibility [guided]
Adapt analysis rules based on file type:
- Python: Follow PEP 8 conventions
- JavaScript/TypeScript: Follow Airbnb or Standard style
- Other languages: Use common conventions

### Save as
`/tmp/workflow/step2_static_analysis.json`

### Success criteria
- All changed files analyzed
- Issues categorized by severity (error, warning, info)
- Line numbers provided for each issue

---

## Step 3: Security Scan

### Task
Scan for potential security issues:

1. **Secrets Detection**
   - API keys, tokens, passwords in code
   - AWS credentials
   - Private keys
   - Connection strings with credentials

2. **Common Vulnerabilities**
   - SQL injection patterns (string concatenation in queries)
   - XSS vulnerabilities (unescaped user input in HTML)
   - Path traversal (user input in file paths)
   - Command injection (user input in shell commands)

3. **Dependency Issues**
   - Check if any new dependencies were added
   - Flag if package.json or requirements.txt changed
   - Note: actual CVE checking requires separate tools

4. **Configuration**
   - Debug mode enabled
   - CORS wildcards
   - Disabled security features

### Flexibility [guided]
Focus depth based on file sensitivity:
- Auth-related files: thorough scan
- Test files: lighter scan
- Config files: check for exposed secrets

### Save as
`/tmp/workflow/step3_security.json`

### Success criteria
- All files scanned
- No false positives on test fixtures or examples
- Severity levels assigned (critical, high, medium, low)

### Constraints
- Never output actual secrets in the report (redact them)
- Flag uncertainty: "potential issue" vs "confirmed issue"

---

## Step 4: Logic Review

### Task
Review the code changes for logical issues:

1. **Change Analysis**
   - What is the intent of this PR (infer from title, description, changes)?
   - Do the changes align with the stated intent?
   - Are there any incomplete implementations?

2. **Edge Cases**
   - Null/undefined handling
   - Empty collections
   - Boundary conditions
   - Error handling coverage

3. **Best Practices**
   - DRY violations (copy-pasted code)
   - SOLID principles violations (where obvious)
   - Appropriate use of design patterns

4. **Testing**
   - Are there corresponding test changes?
   - Do tests cover the new code paths?
   - Are edge cases tested?

### Flexibility [autonomous]
Use your judgment to identify issues that automated tools miss.
Focus on issues that would matter in a real code review.

### Save as
`/tmp/workflow/step4_logic_review.json`

### Success criteria
- Clear summary of what the PR does
- Actionable feedback (not vague observations)
- Severity and confidence level for each issue

---

## Step 5: Generate Review Report

### Task
Compile all findings into a GitHub-compatible review report:

**Report Structure:**

```markdown
## 🤖 Automated Code Review

### Summary
[One paragraph: what this PR does, overall quality assessment]

### 📊 Statistics
- Files changed: X
- Lines added: X
- Lines removed: X
- Issues found: X critical, X warnings, X suggestions

### 🔴 Critical Issues
[Must be fixed before merge]

### 🟡 Warnings  
[Should be addressed]

### 💡 Suggestions
[Nice to have improvements]

### ✅ What's Good
[Positive observations to balance the review]

### 📝 Notes
[Any caveats about this automated review]
```

**Formatting rules:**
- Use GitHub-flavored markdown
- Include file paths and line numbers as links
- Code snippets for context
- Keep total length reasonable (<500 lines)

### Flexibility [guided]
Adjust tone based on issue count:
- Few issues: encouraging, brief
- Many issues: structured, prioritized
- Critical issues: clear, actionable

### Save as
`/tmp/workflow/step5_review_report.md`

### Success criteria
- Valid GitHub markdown
- All sections present
- Issues are actionable (not just "this is bad")
- Includes positive feedback
- Line numbers are accurate

### Constraints
- No snark or condescension
- Focus on code, not the author
- Acknowledge when uncertain

---

## Finalization

### After completion
1. Copy review report to `/home/user/reviews/`
2. Name file: `pr_{number}_review.md`
3. Create summary JSON with statistics

### Notification
Provide:
- PR number and title
- Issue summary (X critical, Y warnings, Z suggestions)
- Location of full report
- Recommendation: approve / request changes / comment

### If any step failed
- Generate partial report with available data
- Clearly mark which analysis was skipped
- Never block a PR based on incomplete analysis
