# Workflow: Customer Data Pipeline

## Meta
version: 1.0
author: Data Team
requires: Claude with computer use, database access
estimated_time: 20 minutes
tags: etl, data, analytics, pipeline

## Context
Extract customer transaction data from the production database, transform it 
for analytics purposes, and load it into the data warehouse. This is a weekly 
ETL job that feeds the business intelligence dashboards.

Data sensitivity: Contains PII. All intermediate files must be cleaned up.

---

## Step 1: Extract from Source Database

### Dependencies
```bash
pip install psycopg2-binary pandas sqlalchemy --break-system-packages
```

### Configuration
- Source DB: PostgreSQL at `DB_HOST:5432`
- Database: `production`
- Credentials: `DB_USER` / `DB_PASSWORD` from environment
- Connection timeout: 30 seconds

### Task
Extract data from the following tables for the last 7 days:

1. **customers** — customer profiles
   - Fields: customer_id, created_at, country, segment
   
2. **transactions** — purchase records
   - Fields: transaction_id, customer_id, amount, currency, timestamp, status
   - Filter: status = 'completed'
   
3. **products** — product catalog (full table, ~10k rows)
   - Fields: product_id, name, category, price

Join transactions with customers and products to create a denormalized view.

### Save as
`/tmp/workflow/step1_raw_extract.parquet`

### Success criteria
- File size > 1MB (indicates data was extracted)
- Contains columns: customer_id, country, segment, amount, currency, timestamp, product_name, category
- No duplicate transaction_ids
- All timestamps within last 7 days

### Constraints
- Use read replica if available (`DB_READ_HOST`)
- Maximum 10,000 rows per query batch to avoid timeouts
- Do not extract email, phone, or address fields (PII minimization)

### If something goes wrong
- Connection refused → verify VPN, try read replica
- Query timeout → reduce batch size to 5,000, add progress logging
- Permission denied → stop and report, do not attempt workarounds

---

## Step 2: Data Quality Checks

### Task
Perform data quality validation on the extracted data:

1. **Completeness checks**
   - No null customer_ids
   - No null amounts
   - No null timestamps

2. **Validity checks**
   - All amounts > 0
   - All timestamps are valid dates
   - Currency codes are valid ISO 4217

3. **Consistency checks**
   - No transactions older than customer created_at
   - Amount matches currency precision (2 decimals for USD/EUR)

4. **Anomaly detection**
   - Flag transactions > 3 standard deviations from mean
   - Flag customers with > 50 transactions (potential bots)

Generate a data quality report with:
- Total records checked
- Pass/fail counts per check
- List of flagged anomalies

### Save as
- `/tmp/workflow/step2_validated.parquet` (clean data only)
- `/tmp/workflow/step2_quality_report.json`
- `/tmp/workflow/step2_anomalies.csv` (flagged records)

### Success criteria
- At least 95% of records pass all checks
- Quality report contains all check categories
- Anomalies file exists (even if empty)

### Flexibility [guided]
If you identify additional data quality issues not listed above, include them 
in the report. Use your judgment on severity classification.

### If something goes wrong
- More than 10% failures → stop pipeline, this indicates source data issues
- Anomaly detection fails → skip it, proceed with basic validation

---

## Step 3: Transform and Enrich

### Task
Transform the validated data for analytics:

1. **Currency normalization**
   - Convert all amounts to USD using current exchange rates
   - Add `amount_usd` column
   - Keep original amount and currency

2. **Time dimensions**
   - Add: day_of_week, hour_of_day, is_weekend
   - Add: week_number, month, quarter

3. **Customer metrics**
   - Add: customer_lifetime_value (sum of all their transactions)
   - Add: customer_transaction_count
   - Add: days_since_first_purchase

4. **Product metrics**
   - Add: product_popularity_rank (by transaction count)
   - Add: category_avg_price

5. **Segmentation**
   - Classify transactions: 'small' (<$50), 'medium' ($50-200), 'large' (>$200)
   - Classify customers: 'new' (<30 days), 'active', 'dormant' (>90 days no purchase)

### Dependencies
```bash
pip install forex-python --break-system-packages
```

### Save as
`/tmp/workflow/step3_transformed.parquet`

### Success criteria
- All new columns are present
- No null values in computed columns
- amount_usd is always positive
- Segmentation columns contain only expected values

### Flexibility [autonomous]
If exchange rate API is unavailable, you may use hardcoded rates or skip 
currency conversion. Document which approach was used.

---

## Step 4: Load to Data Warehouse

### Configuration
- Warehouse: BigQuery project `analytics-prod`
- Dataset: `customer_analytics`
- Table: `weekly_transactions`
- Credentials: `GOOGLE_APPLICATION_CREDENTIALS` path

### Task
Load the transformed data into BigQuery:

1. Create table if not exists with appropriate schema
2. Delete existing data for the same date range (idempotent reload)
3. Insert new data with batch size of 10,000 rows
4. Verify row counts match between source and destination

### Dependencies
```bash
pip install google-cloud-bigquery pyarrow --break-system-packages
```

### Save as
`/tmp/workflow/step4_load_report.json`

Contents:
- rows_loaded
- load_timestamp
- destination_table
- execution_time_seconds

### Success criteria
- Row count in BigQuery matches transformed data
- No errors in load report
- Data is queryable (run simple SELECT COUNT)

### Constraints
- Use WRITE_TRUNCATE for date partition only, not entire table
- Maximum 3 retry attempts on transient errors
- Timeout: 10 minutes for entire load

### If something goes wrong
- Authentication failed → verify service account, stop and report
- Quota exceeded → wait 60 seconds, retry with smaller batches
- Schema mismatch → log differences, attempt to add new columns, never delete

---

## Step 5: Cleanup and Notification

### Task
Clean up all temporary files and send completion notification.

1. **Verify pipeline success**
   - All 4 previous steps completed
   - Data is accessible in BigQuery

2. **Cleanup**
   - Delete all files in `/tmp/workflow/`
   - This is critical for PII compliance

3. **Generate summary**
   - Records processed
   - Data quality score
   - Any warnings or anomalies
   - BigQuery table location

### Save as
`/tmp/workflow/pipeline_summary.json` (before cleanup, will be moved)

### Constraints
- Cleanup MUST happen even if notification fails
- Do not leave any PII in temporary storage

---

## Finalization

### After completion
1. Move `pipeline_summary.json` to `/home/user/logs/etl/`
2. Rename with timestamp: `etl_YYYYMMDD_HHMMSS.json`
3. Verify `/tmp/workflow/` is empty

### Notification
Provide brief summary:
- Records processed and loaded
- Data quality percentage
- Any issues or anomalies worth noting
- Confirmation that cleanup completed

### If any step failed
- Do NOT skip cleanup — PII must be removed
- Save error details to `/home/user/logs/etl/failed_TIMESTAMP.json`
- Include: step that failed, error message, partial results location (if any)
