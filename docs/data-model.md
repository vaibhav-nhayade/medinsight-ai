# MedInsight AI — Data Model

## 1. User

Represents an application user.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique user identifier |
| email | String | User email |
| created_at | DateTime | Account creation time |

---

## 2. Report

Represents one uploaded medical report.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique report identifier |
| user_id | UUID | Owner of the report |
| title | String | Report title |
| report_date | Date | Date of medical report |
| document_id | UUID | Associated document |
| status | Enum | uploaded / processing / verification / completed / failed |
| created_at | DateTime | Upload time |

---

## 3. Document

Represents the uploaded PDF/image.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique document identifier |
| report_id | UUID | Associated report |
| filename | String | Original filename |
| file_type | String | PDF / PNG / JPG |
| storage_path | String | Storage location |
| page_count | Integer | Number of pages |
| created_at | DateTime | Upload time |

---

## 4. Test Result

Represents an extracted medical parameter.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique result identifier |
| report_id | UUID | Associated report |
| test_name | String | Name of test |
| value | Decimal | Numerical result |
| unit | String | Measurement unit |
| reference_min | Decimal | Lower reference value |
| reference_max | Decimal | Upper reference value |
| status | Enum | normal / low / high / unknown |
| confidence | Decimal | Extraction confidence |
| needs_verification | Boolean | Whether user verification is required |

---

## 5. Finding

Represents an important observation from the report.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique finding identifier |
| report_id | UUID | Associated report |
| type | Enum | normal / attention / important |
| title | String | Finding title |
| observation | Text | What was observed |
| explanation | Text | Patient-friendly explanation |
| confidence | Decimal | AI confidence |

---

## 6. Insight

Represents an AI-generated interpretation based on one or more findings.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique insight identifier |
| report_id | UUID | Associated report |
| title | String | Insight title |
| explanation | Text | Explanation |
| evidence | JSON | Supporting evidence |
| confidence | Decimal | AI confidence |
| safety_checked | Boolean | Safety validation status |

---

## 7. Doctor Question

Represents a question generated to help the user prepare for a medical consultation.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique question identifier |
| report_id | UUID | Associated report |
| question | Text | Generated question |
| source_finding_id | UUID | Related finding |

---

## 8. Analysis Run

Represents one execution of the AI analysis pipeline.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique analysis identifier |
| report_id | UUID | Associated report |
| status | Enum | queued / processing / completed / failed |
| pipeline_version | String | Version of analysis pipeline |
| started_at | DateTime | Processing start |
| completed_at | DateTime | Processing completion |
| error_message | Text | Error information if processing failed |

---

## 9. Relationships

```text
User
 │
 └──< Reports
        │
        ├── Document
        │
        ├──< Test Results
        │
        ├──< Findings
        │
        ├──< Insights
        │
        ├──< Doctor Questions
        │
        └──< Analysis Runs
```

A user can have multiple reports.

A report has one document and multiple extracted results, findings, insights, questions, and analysis runs.