HubSpot Deals ETL Service - API Documentation

📋 Table of Contents

1. Overview
2. Authentication
3. Base URLs
4. Common Response Formats
5. API Endpoints
6. Health Endpoint
7. Error Handling
8. Examples
9. Rate Limiting

---

🔍 Overview

The HubSpot Deals ETL Service provides REST APIs for extracting, monitoring, and managing HubSpot deal data extraction jobs.

API Version

- Version: 1.0.0
- Base Path: "/api/v1"
- Content Type: "application/json"
- Documentation: Available at "/docs"

Key Features

- Extract HubSpot deals using private app tokens
- Track extraction progress
- Monitor scan status
- Cancel running scans
- Perform maintenance and cleanup operations

---

🔐 Authentication

The service uses HubSpot Private App Access Tokens.

Required Credentials

- HubSpot Private App Token: Used to access HubSpot CRM APIs.
- Tenant ID: Identifies the customer/organization.
- Scan ID: Unique identifier for extraction jobs.

Required Permissions

- "crm.objects.deals.read" - Read deal records
- "crm.schemas.deals.read" - Read deal properties
- "crm.objects.owners.read" - Read owner information

Authentication Headers

Authorization: Bearer <hubspot-private-app-token>
Content-Type: application/json

---

🌐 Base URLs

Development

http://localhost:5000

Swagger Documentation

http://localhost:5000/docs

---

📊 Common Response Formats

Success Response

{
  "status": "success",
  "message": "Operation completed successfully",
  "timestamp": "2026-06-26T10:30:00Z"
}

Error Response

{
  "status": "error",
  "message": "Invalid request",
  "timestamp": "2026-06-26T10:30:00Z"
}

---

🔍 API Endpoints

1. Start Deal Extraction

POST "/api/v1/scan/start"

Starts a new HubSpot deal extraction process.

Request Body

{
  "tenant_id": "tenant-001",
  "hubspot_token": "private-app-token",
  "batch_size": 100,
  "include_archived": false
}

Response

{
  "scan_id": "scan_12345",
  "status": "pending",
  "message": "Deal extraction started successfully"
}

Status Codes

- 202 Extraction started
- 400 Invalid request
- 500 Internal server error

---

2. Get Scan Status

GET "/api/v1/scan/{scan_id}/status"

Returns extraction status.

Example

GET /api/v1/scan/scan_12345/status

Response

{
  "scan_id": "scan_12345",
  "status": "running",
  "processed_items": 250,
  "total_items": 1000,
  "progress_percentage": 25
}

Status Codes

- 200 Success
- 404 Scan not found

---

3. List All Scans

GET "/api/v1/scan/list"

Returns all extraction jobs.

Response

[
  {
    "scan_id": "scan_12345",
    "status": "completed",
    "created_at": "2026-06-26T10:00:00Z"
  }
]

---

4. Cancel Scan

POST "/api/v1/scan/{scan_id}/cancel"

Cancels a running extraction.

Response

{
  "scan_id": "scan_12345",
  "status": "cancelled",
  "message": "Extraction cancelled successfully"
}

---

5. Pipeline Information

GET "/api/v1/pipeline/info"

Returns service pipeline information.

Response

{
  "service": "HubSpot Deals ETL",
  "version": "1.0.0",
  "supported_object": "deals"
}

---

6. Cleanup Old Jobs

POST "/api/v1/maintenance/cleanup"

Deletes old completed jobs and temporary data.

Response

{
  "message": "Cleanup completed successfully"
}

---

🏥 Health Endpoint

Health Check

GET "/api/v1/health"

Checks service availability.

Response

{
  "status": "healthy",
  "service": "HubSpot Deals ETL",
  "version": "1.0.0"
}

Status Codes

- 200 Healthy
- 503 Unhealthy

---

⚠️ Error Handling

Validation Error (400)

{
  "status": "error",
  "error_code": "VALIDATION_ERROR",
  "message": "Input validation failed"
}

Unauthorized (401)

{
  "status": "error",
  "error_code": "UNAUTHORIZED",
  "message": "Authentication required"
}

Forbidden (403)

{
  "status": "error",
  "error_code": "FORBIDDEN",
  "message": "Insufficient permissions"
}

Not Found (404)

{
  "status": "error",
  "error_code": "NOT_FOUND",
  "message": "Resource not found"
}

Rate Limit (429)

{
  "status": "error",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests",
  "retry_after": 60
}

Internal Error (500)

{
  "status": "error",
  "error_code": "INTERNAL_ERROR",
  "message": "Unexpected server error"
}

---

📚 Examples

Start Extraction

curl -X POST "http://localhost:5000/api/v1/scan/start" \
-H "Content-Type: application/json" \
-d '{
  "tenant_id":"tenant-001",
  "hubspot_token":"your-private-app-token",
  "batch_size":100
}'

Check Status

curl "http://localhost:5000/api/v1/scan/scan_12345/status"

List Scans

curl "http://localhost:5000/api/v1/scan/list"

Cancel Scan

curl -X POST "http://localhost:5000/api/v1/scan/scan_12345/cancel"

---

🚦 Rate Limiting

- Maximum of approximately 100 requests every 10 seconds.
- Daily limits depend on HubSpot subscription plans.
- Implement exponential backoff for HTTP 429 responses.
- Respect the "Retry-After" header before retrying requests.

---

API Version: 1.0.0

Service: HubSpot Deals ETL Service

Last Updated: June 2026