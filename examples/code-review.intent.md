<!--
Domain: DevOps / Software Engineering
Complexity: Medium
Tested with: Claude Sonnet 4
Author: IntentFlow Examples
-->

# Workflow: Automated Pull Request Review

## Meta
version: 0.1
author: IntentFlow Team
requires: Claude with computer use, GitHub MCP
estimated_time: 10 minutes
tags: code-review, devops, automation, github

## Context
This workflow performs an automated code review on a pull request.
It analyzes code quality, security concerns, test coverage, and 
documentation completeness. The output is a structured review comment
that helps maintainers make informed decisions about merging.

This is not a replacement for human review — it's a first pass that
catches common issues and helps reviewers focus on architectural concerns.

---

## Step 1: Fetch PR Information

### Dependencies
```bash
pip install PyGithub gitpython --break-system-packages
```

### Configuration
GitHub access:
- Token: Use environment variable GITHUB_TOKEN
- Repository: Extracted from PR URL
- Required permissions: repo (read)

### Task
Given a pull request URL, fetch all relevant information:
- PR title and description
- Author and reviewers
- Changed files list with diff stats
- Full diff content for each file
- Existing comments and review status
- CI/CD status

Parse the PR URL to extract owner, repo, and PR number.

### Save as
`/tmp/workflow/step1_pr_info.json`

### Success criteria
- PR exists and is accessible
- All changed files retrieved with diffs
- Diff content is parseable
- At least one file changed

### If something goes wrong
- 404 Not Found → verify URL format, check if PR exists
- 403 Forbidden → token may lack permissions, try with different scopes
- Large PR (> 50 files) → fetch in batches, warn about review limitations
- Binary files → skip binary diffs, note in output

---

## Step 2: Static Analysis

### Dependencies
```bash
pip install pylint flake8 bandit radon --break-system-packages
npm install -g eslint @typescript-eslint/parser
```

### Task
Run static analysis tools on changed files based on file type:

**Python files (.py):**
- Pylint for code quality
- Flake8 for style violations
- Bandit for security issues
- Radon for complexity metrics

**JavaScript/TypeScript (.js, .ts, .tsx):**
- ESLint with recommended rules
- Check for common security patterns (eval, innerHTML)

**For all files:**
- Check for hardcoded secrets (API keys, passwords)
- Check for TODO/FIXME comments
- Check for overly long functions (> 50 lines)

### Flexibility
If analysis tools are unavailable or fail to install, provide a
manual assessment based on reading the code. The goal is finding
issues, not running specific tools.

### Constraints
- Only analyze changed files, not the entire codebase
- Limit analysis time to 5 minutes total
- Do not execute any code from the PR

### Save as
`/tmp/workflow/step2_static_analysis.json`

Contents:
- Issues by severity (error, warning, info)
- Issues by file
- Complexity scores
- Security findings

### Success criteria
- At least one analysis method completed per file type
- Results structured consistently
- No false positives from obvious test fixtures

### If something goes wrong
- Tool installation fails → skip that tool, use alternatives
- Analysis timeout → report partial results, note timeout
- Syntax errors in code → report as finding, continue with other files

---

## Step 3: Code Quality Assessment

### Task
Perform a human-like code review focusing on:

**Architecture & Design:**
- Does the change follow existing patterns?
- Are there any obvious design issues?
- Is the abstraction level appropriate?

**Readability:**
- Are variable/function names clear?
- Is the code self-documenting?
- Are there sufficient comments for complex logic?

**Testing:**
- Are tests included for new functionality?
- Do tests cover edge cases?
- Is test coverage adequate?

**Documentation:**
- Is README updated if needed?
- Are public APIs documented?
- Are breaking changes noted?

### Flexibility [autonomous]
Apply your judgment as an experienced developer. Focus on issues
that would block a merge or cause problems in production.
Minor style issues are less important than logical errors.

### Constraints
- Be constructive, not nitpicky
- Provide specific file:line references
- Suggest fixes, not just problems
- Acknowledge good practices when present

### Save as
`/tmp/workflow/step3_quality_assessment.json`

Contents:
- Must-fix issues (blockers)
- Should-fix issues (important)
- Consider issues (suggestions)
- Positive observations

### Success criteria
- Each issue has file reference and explanation
- Suggestions include example fix when possible
- Assessment covers all changed files
- Tone is professional and helpful

---

## Step 4: Generate Review Comment

### Task
Synthesize all analysis into a GitHub-ready review comment.

**Comment structure:**

```markdown
## 🤖 Automated Code Review

### Summary
[One paragraph overview]

### 🔴 Must Fix (Blockers)
[List of critical issues]

### 🟡 Should Fix (Important)  
[List of important issues]

### 🟢 Suggestions
[List of minor improvements]

### ✅ What Looks Good
[Positive observations]

### 📊 Metrics
- Files changed: X
- Complexity score: X
- Test coverage: X (if available)

---
*This review was generated automatically. Please verify findings.*
```

### Flexibility
Adapt the format based on findings. If there are no blockers,
emphasize that. If the PR is excellent, say so enthusiastically.
Match the tone to the severity of findings.

### Constraints
- Keep total comment under 2000 words
- Use GitHub-flavored markdown
- Include disclaimer about automated review
- Do not approve or request changes — provide information

### Save as
- `/tmp/workflow/step4_review_comment.md` — the formatted comment
- `/tmp/workflow/step4_review_summary.json` — structured summary

### Success criteria
- Markdown renders correctly
- All issues from previous steps included
- File references are clickable (correct format)
- Comment is actionable

---

## Step 5: Post Review (Optional)

### Configuration
Only execute if environment variable POST_REVIEW=true

### Task
Post the review comment to the pull request using GitHub API.

**Actions:**
1. Post the review comment from Step 4
2. Add appropriate labels based on findings:
   - `needs-security-review` if security issues found
   - `needs-tests` if test coverage is low
   - `good-first-review` if no blockers

### Constraints
- Never approve or request changes automatically
- Only post as a comment, not a formal review
- Do not close or merge the PR
- Rate limit: max 1 comment per run

### Save as
`/tmp/workflow/step5_post_result.json`

Contents:
- Comment URL
- Labels added
- API response status

### Success criteria
- Comment posted successfully
- Comment visible on PR
- No duplicate comments

### If something goes wrong
- Rate limited → save comment locally, report for manual posting
- Permission denied → save comment, provide instructions for manual posting
- PR closed → abort, note PR is no longer open

---

## Finalization

### After completion
1. Archive all artifacts to `/archive/pr_reviews/{repo}/{pr_number}/`
2. Log review metrics for tracking:
   - Time taken
   - Issues found by category
   - Files analyzed

### Notification
Provide summary:
- PR URL reviewed
- Number of issues by severity
- Whether comment was posted
- Link to review comment if posted
- Any limitations or skipped analyses
