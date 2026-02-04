# Failure Strategies

Real-world workflows encounter failures. This guide explains how to write robust failure handling in IntentFlow.

## Philosophy

Traditional code uses try/catch with specific exception types. IntentFlow uses natural language because:

1. **LLMs can interpret context** — "API seems slow today" → might need longer timeout
2. **Failures are often ambiguous** — Is 50% data missing a failure or acceptable?
3. **Recovery often needs judgment** — When to retry vs. when to give up?

## The Failure Handling Section

```markdown
### If something goes wrong
- [condition] → [action]
- [condition] → [action]
```

Each line maps a failure condition to a recovery action.

## Condition Patterns

### Specific Technical Errors

```markdown
- Connection timeout → retry with 30 second timeout
- HTTP 401 → credentials expired, abort with auth error
- HTTP 429 → rate limited, wait 60 seconds, retry
- HTTP 500 → server error, wait 10 seconds, retry up to 3 times
- HTTP 503 → service unavailable, try backup endpoint
```

### Data Quality Issues

```markdown
- Missing required fields → log warning, use default values
- Invalid date format → attempt auto-parsing, fail if ambiguous
- Null values > 10% → abort, data quality too low
- Duplicate records → dedupe on primary key, keep latest
- Values outside expected range → flag as anomaly, continue
```

### Resource Issues

```markdown
- File not found → check alternate paths, abort if still missing
- Permission denied → report required permissions, abort
- Disk space low → clean temp files, retry
- Memory exceeded → process in smaller batches
```

### Logical Issues

```markdown
- No records match criteria → expand criteria, note in output
- Too many records (>1M) → sample 100k, note limitation
- Calculation produces infinity/NaN → use fallback method
- Results don't pass sanity check → flag for human review
```

## Action Patterns

### Retry Actions

```markdown
→ retry immediately
→ retry after 5 seconds  
→ retry with exponential backoff (1s, 2s, 4s, 8s)
→ retry up to 3 times
→ retry once with different parameters
```

### Fallback Actions

```markdown
→ use backup endpoint at backup.api.com
→ use cached data from /cache/last_good.json
→ use default value of 0
→ skip this record, continue with others
→ use alternative method (describe method)
```

### Abort Actions

```markdown
→ abort immediately
→ save progress, then abort
→ abort with clear error message: "[specific message]"
→ abort and notify: describe what happened and next steps
```

### Adaptation Actions

```markdown
→ expand date range to last 6 months
→ reduce batch size to 100
→ increase timeout to 60 seconds
→ switch to synchronous processing
→ simplify analysis (skip advanced metrics)
```

### Documentation Actions

```markdown
→ log warning, continue
→ note limitation in output metadata
→ add to exceptions report
→ flag for human review
```

## Severity Levels

Organize failures by how they should be handled:

```markdown
### If something goes wrong

**Transient (retry):**
- Network timeout → exponential backoff, max 5 retries
- Rate limited → wait, retry
- Temporary server error → wait 30s, retry

**Recoverable (adapt):**
- Partial data available → use what we have, note incompleteness
- Alternative source available → switch to backup
- Non-critical feature fails → skip it, continue core workflow

**Fatal (abort):**
- Authentication failed → cannot proceed, abort with auth instructions
- Critical data source unavailable with no backup → abort
- Data corruption detected → abort, do not produce potentially wrong results
```

## Cascading Strategies

When first strategy fails, try the next:

```markdown
### If something goes wrong
- API unavailable:
  1. First: retry 3 times with backoff
  2. Then: try backup API
  3. Then: use cached data (note staleness)
  4. Finally: abort if cache also unavailable
```

## Preserving Progress

For long-running steps:

```markdown
### If something goes wrong
- Any error during processing:
  1. Save completed work to /tmp/checkpoint_{step}_{timestamp}.json
  2. Log error with context
  3. If recoverable → resume from checkpoint
  4. If fatal → abort, report checkpoint location for manual recovery
```

## Partial Success

Not every failure needs to stop the workflow:

```markdown
### If something goes wrong
- Some records fail validation:
  - If < 5% fail → log failures, continue with valid records
  - If 5-20% fail → continue but add WARNING to output
  - If > 20% fail → abort, data quality too low

### Success criteria
- At least 80% of input records processed successfully
- Failure report generated for skipped records
```

## Context-Dependent Strategies

Sometimes the right action depends on context:

```markdown
### If something goes wrong
- Insufficient data:
  - If this is a daily report → use available data, note incompleteness
  - If this is a compliance report → abort, incomplete data is unacceptable
  
- External API slow:
  - If we're in batch mode → wait patiently, we have time
  - If this is real-time → timeout after 5s, use cached value
```

## Human Escalation

Some failures need human judgment:

```markdown
### If something goes wrong
- Ambiguous data detected (conflicting records for same entity):
  1. Document the conflict
  2. Use most recent record as default
  3. Flag for human review in output
  4. Continue processing

- Security anomaly detected:
  1. Stop processing immediately
  2. Do NOT proceed or attempt to fix
  3. Save current state
  4. Report: "Security review required before continuing"
```

## Failure Strategy Templates

### API Integration Step

```markdown
### If something goes wrong
- Connection refused → check if service is up, retry 3 times
- Timeout → increase timeout to 60s, retry once
- 401 Unauthorized → credentials may be expired, abort with auth error
- 403 Forbidden → check permissions, abort with access error  
- 404 Not Found → resource may have moved, check alternate endpoints
- 429 Too Many Requests → wait for rate limit reset, retry
- 500 Internal Error → server issue, retry with backoff
- Invalid response format → log response, try to parse anyway, abort if unparseable
```

### Data Processing Step

```markdown
### If something goes wrong
- File not found → check alternate locations, abort if truly missing
- Parse error → try alternate encoding (UTF-8, Latin-1), abort if still failing
- Schema mismatch → log differences, attempt to map fields, abort if critical fields missing
- Memory error → process in chunks of 10000 records
- Unexpected nulls → use appropriate imputation based on field type
- Duplicates found → dedupe, keep most complete record
```

### Report Generation Step

```markdown
### If something goes wrong
- Visualization fails → try simpler chart type, use table as last resort
- PDF generation error → fall back to HTML output
- Styling issues → use minimal default styling, note in output
- Data too large for visualization → aggregate or sample, note in caption
- Missing optional data → omit section, note "data unavailable"
```

## Anti-Patterns

### Too Generic

```markdown
### If something goes wrong
- Error → retry or abort
```

**Better:** Be specific about which errors and which actions.

### No Final Fallback

```markdown
### If something goes wrong  
- Timeout → retry
- Retry fails → retry again
```

**Better:** Always have a terminal action (abort, use fallback, etc.)

### Hiding Failures

```markdown
### If something goes wrong
- Any error → continue silently
```

**Better:** At minimum, log and note in output metadata.

### Overly Complex

```markdown
### If something goes wrong
- If error code is 429 and it's Monday and we've retried less than 3 times 
  and the queue depth is below 100 → wait 30 seconds and retry
```

**Better:** Use simpler rules. LLM can apply judgment within reasonable bounds.
