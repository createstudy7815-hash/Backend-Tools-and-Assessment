🗄️ HubSpot Deals Database Schema Document

This document defines the PostgreSQL database schema for storing HubSpot Deals data extracted by the HubSpot Deals ETL service.

---

📋 Overview

The HubSpot Deals ETL database consists of two primary tables:

1. scan_jobs - Tracks extraction jobs and ETL execution status.
2. hubspot_deals - Stores extracted HubSpot deal records.

The schema supports:

- Multi-tenant architecture
- ETL metadata tracking
- Efficient querying and filtering
- Incremental data extraction

---

🏗️ Table Schemas

1. scan_jobs Table

Purpose: Manage and track ETL extraction jobs.

Column Name| Type| Constraints| Description
id| UUID| PRIMARY KEY| Internal job identifier
scan_id| VARCHAR(100)| UNIQUE, NOT NULL| External scan identifier
status| VARCHAR(20)| NOT NULL| pending, running, completed, failed, cancelled
scan_type| VARCHAR(50)| NOT NULL| Type of extraction
config| JSONB| NOT NULL| Extraction configuration
tenant_id| VARCHAR(100)| NOT NULL| Tenant identifier
error_message| TEXT| NULLABLE| Error details if failed
started_at| TIMESTAMP| NULLABLE| Scan start time
completed_at| TIMESTAMP| NULLABLE| Scan completion time
total_items| INTEGER| DEFAULT 0| Total records found
processed_items| INTEGER| DEFAULT 0| Successfully processed records
failed_items| INTEGER| DEFAULT 0| Failed records
created_at| TIMESTAMP| NOT NULL| Record creation time
updated_at| TIMESTAMP| NOT NULL| Last update time

CREATE TABLE Statement

CREATE TABLE scan_jobs (
    id UUID PRIMARY KEY,
    scan_id VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(20) NOT NULL,
    scan_type VARCHAR(50) NOT NULL,
    config JSONB NOT NULL,
    tenant_id VARCHAR(100) NOT NULL,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    total_items INTEGER DEFAULT 0,
    processed_items INTEGER DEFAULT 0,
    failed_items INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

---

2. hubspot_deals Table

Purpose: Store extracted HubSpot deals.

Column Name| Type| Constraints| Description
id| UUID| PRIMARY KEY| Internal identifier
scan_job_id| UUID| FOREIGN KEY| Reference to scan_jobs
hubspot_deal_id| VARCHAR(100)| UNIQUE, NOT NULL| HubSpot deal ID
deal_name| VARCHAR(255)| NOT NULL| Name of the deal
amount| NUMERIC(15,2)| NULLABLE| Deal amount
deal_stage| VARCHAR(100)| INDEX| Current stage
pipeline| VARCHAR(100)| INDEX| Pipeline name
close_date| TIMESTAMP| NULLABLE| Expected close date
owner_id| VARCHAR(100)| NULLABLE| HubSpot owner ID
deal_type| VARCHAR(100)| NULLABLE| Deal type
is_closed| BOOLEAN| DEFAULT FALSE| Closed status
created_date| TIMESTAMP| NULLABLE| HubSpot creation date
last_modified_date| TIMESTAMP| NULLABLE| Last modification date
raw_data| JSONB| NOT NULL| Complete API response
_extracted_at| TIMESTAMP| NOT NULL| ETL extraction timestamp
_scan_id| VARCHAR(100)| NOT NULL| Extraction job identifier
_tenant_id| VARCHAR(100)| NOT NULL| Tenant identifier
created_at| TIMESTAMP| NOT NULL| Record creation time
updated_at| TIMESTAMP| NOT NULL| Last update time

CREATE TABLE Statement

CREATE TABLE hubspot_deals (
    id UUID PRIMARY KEY,
    scan_job_id UUID NOT NULL REFERENCES scan_jobs(id) ON DELETE CASCADE,
    hubspot_deal_id VARCHAR(100) UNIQUE NOT NULL,
    deal_name VARCHAR(255) NOT NULL,
    amount NUMERIC(15,2),
    deal_stage VARCHAR(100),
    pipeline VARCHAR(100),
    close_date TIMESTAMP,
    owner_id VARCHAR(100),
    deal_type VARCHAR(100),
    is_closed BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP,
    last_modified_date TIMESTAMP,
    raw_data JSONB NOT NULL,
    _extracted_at TIMESTAMP NOT NULL,
    _scan_id VARCHAR(100) NOT NULL,
    _tenant_id VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

---

🔗 Relationships

scan_jobs.id ← hubspot_deals.scan_job_id

One scan job can extract multiple deals.

---

📈 Indexes

CREATE INDEX idx_scan_status_created
ON scan_jobs(status, created_at);

CREATE INDEX idx_scan_tenant
ON scan_jobs(tenant_id);

CREATE INDEX idx_deal_stage
ON hubspot_deals(deal_stage);

CREATE INDEX idx_pipeline
ON hubspot_deals(pipeline);

CREATE INDEX idx_close_date
ON hubspot_deals(close_date);

CREATE INDEX idx_tenant_id
ON hubspot_deals(_tenant_id);

CREATE INDEX idx_scan_id
ON hubspot_deals(_scan_id);

CREATE INDEX idx_hubspot_deal_id
ON hubspot_deals(hubspot_deal_id);

CREATE INDEX idx_tenant_stage
ON hubspot_deals(_tenant_id, deal_stage);

CREATE INDEX idx_tenant_close_date
ON hubspot_deals(_tenant_id, close_date);

---

🔒 Multi-Tenant Data Isolation

Tenant isolation is achieved using:

_tenant_id

All queries must filter records by tenant ID.

Each tenant can only access its own data.

Application-level filtering and authorization checks ensure complete tenant isolation.

Example:

SELECT *
FROM hubspot_deals
WHERE _tenant_id = 'tenant-001';

---

📊 Example Queries

Get Deal by ID

SELECT *
FROM hubspot_deals
WHERE hubspot_deal_id = '12345';

Get Deals by Stage

SELECT deal_name, amount, deal_stage
FROM hubspot_deals
WHERE deal_stage = 'appointmentscheduled';

Get Deals for a Tenant

SELECT *
FROM hubspot_deals
WHERE _tenant_id = 'tenant-001';

Count Deals by Pipeline

SELECT pipeline, COUNT(*)
FROM hubspot_deals
GROUP BY pipeline;

---

🛡️ Data Integrity Constraints

ALTER TABLE scan_jobs
ADD CONSTRAINT check_status
CHECK (
status IN ('pending','running','completed','failed','cancelled')
);

---

Database Schema Version

Version: 1.0

Compatible With: PostgreSQL