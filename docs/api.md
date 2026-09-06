# MedInsight AI — API Contract

Base URL:

```text
/api/v1
```

## Reports

### POST `/reports`

Upload a medical report.

**Request:** `multipart/form-data`

```text
file: PDF / PNG / JPG
title: optional string
report_date: optional date
```

**Response:**

```json
{
  "report_id": "uuid",
  "status": "uploaded"
}
```

---

### GET `/reports`

Return the user's reports.

**Response:**

```json
{
  "reports": [
    {
      "id": "uuid",
      "title": "Blood Test",
      "report_date": "2026-09-01",
      "status": "completed"
    }
  ]
}
```

---

### GET `/reports/{report_id}`

Return report details and analysis.

**Response:**

```json
{
  "id": "uuid",
  "title": "Blood Test",
  "report_date": "2026-09-01",
  "status": "completed",
  "summary": {
    "total": 24,
    "normal": 18,
    "attention": 4,
    "important": 2
  },
  "results": [],
  "findings": [],
  "insights": [],
  "doctor_questions": []
}
```

---

### DELETE `/reports/{report_id}`

Delete a report and its associated data.

**Response:**

```json
{
  "success": true
}
```

---

# Analysis

### POST `/reports/{report_id}/analyze`

Start the AI analysis pipeline.

**Response:**

```json
{
  "analysis_id": "uuid",
  "status": "queued"
}
```

---

### GET `/reports/{report_id}/status`

Return current processing status.

**Response:**

```json
{
  "report_id": "uuid",
  "status": "processing",
  "progress": 65
}
```

Possible statuses:

```text
uploaded
processing
verification
completed
failed
```

---

# Results

### GET `/reports/{report_id}/results`

Return extracted medical test results.

**Response:**

```json
{
  "results": [
    {
      "id": "uuid",
      "test_name": "Hemoglobin",
      "value": 13.8,
      "unit": "g/dL",
      "reference_min": 12.0,
      "reference_max": 16.0,
      "status": "normal",
      "confidence": 0.98,
      "needs_verification": false
    }
  ]
}
```

---

### GET `/reports/{report_id}/findings`

Return important report findings.

**Response:**

```json
{
  "findings": [
    {
      "id": "uuid",
      "type": "attention",
      "title": "Elevated LDL",
      "observation": "LDL is above the provided reference or target range.",
      "explanation": "...",
      "confidence": 0.91
    }
  ]
}
```

---

### GET `/reports/{report_id}/insights`

Return AI-generated insights.

**Response:**

```json
{
  "insights": [
    {
      "id": "uuid",
      "title": "Potentially related findings",
      "explanation": "...",
      "evidence": [],
      "confidence": 0.87,
      "safety_checked": true
    }
  ]
}
```

---

### GET `/reports/{report_id}/questions`

Return questions generated for discussion with a healthcare professional.

**Response:**

```json
{
  "questions": [
    {
      "id": "uuid",
      "question": "Should this result be repeated?",
      "source_finding_id": "uuid"
    }
  ]
}
```

---

# Trends

### GET `/trends`

Return available parameters across the user's reports.

**Response:**

```json
{
  "parameters": [
    "Hemoglobin",
    "LDL",
    "TSH"
  ]
}
```

---

### GET `/trends/{parameter}`

Return historical values for a parameter.

**Response:**

```json
{
  "parameter": "Hemoglobin",
  "unit": "g/dL",
  "data": [
    {
      "date": "2026-01-10",
      "value": 10.2
    },
    {
      "date": "2026-05-12",
      "value": 11.1
    },
    {
      "date": "2026-09-01",
      "value": 12.0
    }
  ]
}
```

---

# API Design Principles

1. All endpoints use `/api/v1`.
2. JSON is the default response format.
3. File uploads use `multipart/form-data`.
4. IDs use UUIDs.
5. API responses must use defined schemas.
6. Errors must return structured error responses.
7. Sensitive information must not appear in logs.
8. AI-generated content must pass safety validation before being returned.
9. The API must never expose internal AI prompts, API keys, or credentials.
10. Authentication and authorization will be added before production deployment.