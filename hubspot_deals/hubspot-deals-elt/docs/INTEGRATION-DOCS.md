📋 HubSpot Deals Service - Integration with HubSpot CRM API

This document explains the HubSpot CRM REST API endpoints required by the HubSpot Deals Service to extract deal data from HubSpot instances.

---

📋 Overview

The HubSpot Deals Service integrates with HubSpot CRM API v3 endpoints to extract deal information.

✅ Required Endpoint (Essential)

API Endpoint| Purpose| Version| Required Permissions| Usage
"/crm/v3/objects/deals"| List and retrieve deals| v3| "crm.objects.deals.read"| Required

🎯 Recommendation

Start with only the required endpoint. The "/crm/v3/objects/deals" endpoint provides all essential deal data needed for extraction.

---

🔐 Authentication Requirements

Private App Token Authentication

Authorization: Bearer <Private-App-Token>
Content-Type: application/json

Required Permissions

- "crm.objects.deals.read" : Read deal records
- "crm.schemas.deals.read" : Read deal properties
- "crm.objects.owners.read" : Read deal owner information

---

🌐 HubSpot API Endpoints

🎯 PRIMARY ENDPOINT (Required for Basic Deal Extraction)

1. Search Deals - "/crm/v3/objects/deals" ✅ REQUIRED

Purpose: Retrieve a paginated list of all deals.

Method: "GET"

URL:

https://api.hubapi.com/crm/v3/objects/deals

Query Parameters

Parameter| Description
"limit"| Number of records per request
"after"| Pagination cursor
"properties"| Specific properties to return
"archived"| Include archived records ("true/false")

Pagination Example

https://api.hubapi.com/crm/v3/objects/deals?limit=100&after=12345

Request Example

GET https://api.hubapi.com/crm/v3/objects/deals?limit=100&properties=dealname,amount,dealstage&archived=false

Authorization: Bearer <Private-App-Token>
Content-Type: application/json

Sample Response

{
  "results": [
    {
      "id": "12345",
      "properties": {
        "dealname": "Enterprise Software Deal",
        "amount": "5000",
        "dealstage": "appointmentscheduled",
        "pipeline": "default",
        "closedate": "2026-06-25T00:00:00Z",
        "createdate": "2026-06-20T10:00:00Z"
      },
      "createdAt": "2026-06-20T10:00:00Z",
      "updatedAt": "2026-06-25T12:00:00Z",
      "archived": false
    }
  ],
  "paging": {
    "next": {
      "after": "12346"
    }
  }
}

---

⚡ Performance Considerations

Rate Limiting

- Standard HubSpot APIs allow approximately 100 requests per 10 seconds per app.
- Daily limits depend on the HubSpot subscription plan.
- Implement exponential backoff for HTTP "429 Too Many Requests".

Error Handling

HTTP/401 Unauthorized
HTTP/403 Forbidden
HTTP/404 Not Found
HTTP/429 Too Many Requests

For HTTP "429" responses, wait for the value specified in the "Retry-After" header before retrying.

---

🔒 Security Requirements

Required Scopes

- "crm.objects.deals.read"
- "crm.schemas.deals.read"
- "crm.objects.owners.read"

---

📊 Common Deal Properties

The following are commonly used deal properties:

- "dealname"
- "amount"
- "dealstage"
- "pipeline"
- "closedate"
- "createdate"
- "hs_createdate"
- "hs_lastmodifieddate"
- "hubspot_owner_id"
- "dealtype"
- "hs_object_id"
- "hs_is_closed"

---

🧪 Testing API Integration

Test Authentication

curl -X GET \
"https://api.hubapi.com/crm/v3/objects/deals?limit=1" \
-H "Authorization: Bearer <Private-App-Token>" \
-H "Content-Type: application/json"

---

🚨 Common Issues & Solutions

Issue: 401 Unauthorized

Solution: Verify that the private app token is valid.

Issue: 403 Forbidden

Solution: Ensure the token has "crm.objects.deals.read" permission.

Issue: 429 Too Many Requests

Solution: Implement retry with exponential backoff and respect the "Retry-After" header value.

Issue: Empty Deal List

Solution: Verify that deals exist in the HubSpot account and the token has access permissions.

---

📞 Support Resources

- HubSpot CRM API Documentation: https://developers.hubspot.com/docs/api/crm/deals
- Authentication Guide: https://developers.hubspot.com/docs/api/private-apps
- Rate Limits Guide: https://developers.hubspot.com/docs/api/usage-details