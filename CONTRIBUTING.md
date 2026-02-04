# Contributing to IntentFlow

Thank you for your interest in contributing to IntentFlow! This document provides guidelines for contributing to the project.

## Ways to Contribute

### 1. Add Examples

The best way to grow the project is through diverse examples. We need workflows from:

- **Data Engineering** — ETL pipelines, data quality checks, migrations
- **DevOps** — Deployment workflows, monitoring setup, incident response
- **Content** — Blog posts, documentation, reports
- **Finance** — Analysis, reporting, compliance
- **Research** — Literature review, experiment design, data collection
- **Any other domain** — We want to see what's possible!

### 2. Improve Documentation

- Fix typos and unclear explanations
- Add more examples to existing docs
- Translate documentation to other languages
- Write tutorials or guides

### 3. Build Tools

- IDE extensions (VS Code, JetBrains)
- Converters (to/from other workflow formats)
- Runners for specific LLMs
- Visualization tools

### 4. Enhance the Specification

- Propose new sections or features
- Identify edge cases
- Suggest clarifications

## Submitting Examples

### Example Quality Checklist

- [ ] Follows the [specification](SPEC.md)
- [ ] Passes validation: `python tools/validator/validate.py your-example.md`
- [ ] Includes meaningful comments explaining non-obvious decisions
- [ ] Uses realistic (but not sensitive) data scenarios
- [ ] Demonstrates at least one unique aspect of IntentFlow

### Example Structure

```markdown
# Workflow: Clear Descriptive Title

## Meta
version: 1.0
author: Your Name
tags: relevant, tags, here

## Context
Brief explanation of what this workflow accomplishes
and why it's useful.

---

## Step 1: ...
```

### Naming Convention

- Filename: `domain-specific-name.md` (lowercase, hyphens)
- Examples: `data-quality-audit.md`, `weekly-newsletter.md`

## Submitting Code Changes

### Setup

1. Fork the repository
2. Clone your fork
3. Create a feature branch: `git checkout -b feature/your-feature`

### Code Style

**Python:**
- Follow PEP 8
- Use type hints
- Add docstrings to public functions

**Markdown:**
- Use ATX-style headers (`#` not underlines)
- One sentence per line for easier diffs
- Use fenced code blocks with language hints

### Testing

Before submitting:

```bash
# Validate all examples
for f in examples/*.md; do python tools/validator/validate.py "$f"; done

# Run any Python tests
python -m pytest tools/
```

### Commit Messages

Format:
```
type: Short description

Longer explanation if needed. Wrap at 72 characters.

Fixes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `examples`: New or updated examples
- `tools`: Tooling changes
- `spec`: Specification changes

## Pull Request Process

1. Update documentation if needed
2. Add your example to the examples/ folder
3. Ensure all validation passes
4. Create PR with clear description
5. Respond to review feedback

### PR Description Template

```markdown
## What

Brief description of the change.

## Why

Why is this change needed?

## Testing

How was this tested?

## Checklist

- [ ] Validation passes
- [ ] Documentation updated (if needed)
- [ ] Examples work as intended
```

## Proposing Specification Changes

Specification changes require discussion before implementation:

1. Open an issue with `[SPEC]` prefix
2. Describe the proposed change
3. Explain the motivation
4. Show example usage
5. Wait for community feedback

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on the work, not the person
- Assume good intentions

## Questions?

- Open an issue with `[Question]` prefix
- Join discussions in existing issues
- Be patient — maintainers are volunteers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
