<!--
Domain: Data Engineering
Complexity: Medium
Tested with: Claude Sonnet 4
Author: IntentFlow Examples
-->

# Workflow: Customer Data Pipeline

## Meta
version: 0.1
author: IntentFlow Team
requires: Claude with computer use
estimated_time: 20 minutes
tags: etl, data-pipeline, analytics

## Context
This workflow extracts customer interaction data from multiple sources,
transforms it into a unified format, and loads it into an analytics-ready
data warehouse structure. The pipeline runs weekly and feeds into
customer segmentation and churn prediction models.

---

## Step 1: Extract from CRM API

### Dependencies
```bash
pip install requests pandas --break-system-packages
```

### Configuration
API credentials:
- Base URL: Use environment variable CRM_API_URL
- API Key: Use environment variable CRM_API_KEY
- Rate limit: 100 requests per minute

### Task
Extract customer records updated in the last 7 days from the CRM system.
Use pagination to fetch all records. For each customer, retrieve:
- Customer ID
- Email (hash for privacy)
- Signup date
- Last activity date
- Subscription tier
- Total lifetime value
- Support tickets count

### Save as
`/tmp/workflow/step1_crm_extract.parquet`

### Success criteria
- API responds with 200 status
- At least 100 customer records extracted
- All required fields present
- No duplicate customer IDs

### If something goes wrong
- Rate limited (429) → implement exponential backoff, max 5 retries
- Auth failed (401) → abort with clear error, credentials may be expired
- Timeout → reduce batch size to 50 records per request
- Partial data → save what was retrieved, log missing fields

---

## Step 2: Extract from Event Stream

### Dependencies
```bash
pip install confluent-kafka avro-python3 --break-system-packages
```

### Configuration
Kafka connection:
- Bootstrap servers: Use environment variable KAFKA_BROKERS
- Topic: customer-events
- Consumer group: intentflow-pipeline
- Read from: last 7 days

### Task
Consume customer behavioral events from the Kafka topic.
Relevant event types to extract:
- page_view
- feature_used
- purchase_completed
- support_chat_started

Aggregate events per customer:
- Total page views
- Unique features used
- Purchase count and total amount
- Support interactions

### Flexibility
If certain event types are missing or have different names than expected,
adapt the extraction logic accordingly. The goal is to capture customer
engagement signals, regardless of exact event naming conventions.

### Save as
`/tmp/workflow/step2_events_extract.parquet`

### Success criteria
- Successfully connected to Kafka cluster
- Events span the expected 7-day window
- Aggregations computed without errors
- Customer IDs match format from Step 1

### If something goes wrong
- Connection refused → check VPN, try alternate broker from list
- No messages → verify topic name, check if retention period is sufficient
- Deserialization error → log problematic messages, skip and continue
- Consumer lag too high → limit to last 3 days, note in metadata

---

## Step 3: Transform and Join

### Dependencies
```bash
pip install pandas numpy scikit-learn --break-system-packages
```

### Task
Merge CRM data with event data to create a unified customer profile.

**Transformations required:**
- Join on customer_id (inner join — only customers in both sources)
- Calculate engagement score: weighted combination of page views, features used, purchases
- Calculate days since last activity
- Categorize customers: active (< 7 days), at-risk (7-30 days), churned (> 30 days)
- Normalize numerical features for ML readiness

**Data quality checks:**
- Remove customers with impossible values (negative LTV, future dates)
- Handle missing values: impute or flag
- Deduplicate any remaining duplicates

### Flexibility [guided]
The exact engagement score formula is at your discretion. Use reasonable
weights based on business intuition (purchases likely matter more than page views).
Document the formula chosen.

### Constraints
- Do not drop customers without explanation
- All transformations must be documented in a separate log
- Original customer IDs must be preserved

### Save as
- `/tmp/workflow/step3_unified_customers.parquet` — transformed data
- `/tmp/workflow/step3_transform_log.json` — transformation decisions and stats

### Success criteria
- Join produces at least 80% match rate
- No null values in required output columns
- Engagement scores are between 0 and 100
- Category distribution is reasonable (not 100% in one category)

### If something goes wrong
- Low match rate (< 50%) → investigate ID format mismatch, try fuzzy matching on email hash
- Too many nulls → report which fields are problematic, use median imputation
- Outliers detected → cap at 99th percentile, document in log

---

## Step 4: Load to Data Warehouse

### Dependencies
```bash
pip install google-cloud-bigquery pyarrow --break-system-packages
```

### Configuration
BigQuery settings:
- Project: Use environment variable GCP_PROJECT_ID
- Dataset: customer_analytics
- Table: weekly_customer_profiles
- Write mode: append with date partition

### Task
Load the transformed data into BigQuery. 

**Operations:**
1. Validate schema matches existing table (or create if first run)
2. Add processing metadata: run_timestamp, source_version, record_count
3. Upload data using streaming insert or load job (prefer load job for this volume)
4. Verify row count matches source

### Constraints
- Never overwrite existing data — always append
- Include processing timestamp for each record
- Respect BigQuery quotas (max 1000 requests/100 seconds)

### Save as
`/tmp/workflow/step4_load_receipt.json`

Contents:
- Destination table full path
- Rows loaded
- Load job ID
- Any warnings

### Success criteria
- Load job completes successfully
- Row count in receipt matches source count
- No schema validation errors
- Data queryable in BigQuery

### If something goes wrong
- Schema mismatch → log differences, attempt automatic schema evolution if safe
- Quota exceeded → batch into smaller chunks, add delays
- Partial failure → record which rows failed, retry failed subset
- Permission denied → abort with clear instructions to check IAM

---

## Finalization

### After completion
1. Archive source files to `/archive/pipeline_runs/{date}/`
2. Create summary report with:
   - Records processed at each step
   - Match rates and data quality metrics
   - Any warnings or anomalies
3. Send completion notification (log to stdout for now)
4. Clean up `/tmp/workflow/`

### Notification
Report:
- Total customers processed
- New customers this week
- Data quality score (% records with no issues)
- Link to BigQuery table
- Any issues that need human review
