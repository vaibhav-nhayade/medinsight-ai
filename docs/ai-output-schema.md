# MedInsight AI — Output Schema

## Purpose

All AI pipeline stages should produce structured outputs.

The frontend must not depend on arbitrary AI-generated text.

---

## 1. Analysis Result

```json
{
  "report_id": "uuid",
  "status": "completed",
  "summary": {
    "total": 24,
    "normal": 18,
    "attention": 4,
    "important": 2,
    "unknown": 0
  },
  "results": [],
  "findings": [],
  "insights": [],
  "doctor_questions": [],
  "sources": [],
  "warnings": []
}
```

---

## 2. Test Result

```json
{
  "id": "uuid",
  "test_name": "Hemoglobin",
  "value": 13.8,
  "unit": "g/dL",
  "reference_range": {
    "min": 12.0,
    "max": 16.0
  },
  "status": "normal",
  "confidence": 0.98,
  "needs_verification": false,
  "source": {
    "page": 1
  }
}
```

### Status values

```text
normal
low
high
unknown
```

---

## 3. Finding

```json
{
  "id": "uuid",
  "type": "attention",
  "title": "Example finding",
  "observation": "Description of what was observed.",
  "explanation": "Patient-friendly explanation.",
  "confidence": 0.91,
  "related_results": [
    "result_uuid"
  ]
}
```

### Finding types

```text
normal
attention
important
```

---

## 4. Insight

```json
{
  "id": "uuid",
  "title": "Potentially related findings",
  "explanation": "Evidence-grounded explanation.",
  "related_results": [
    "result_uuid_1",
    "result_uuid_2"
  ],
  "evidence": [
    {
      "source_id": "source_001",
      "title": "Trusted medical source",
      "reference": "source reference"
    }
  ],
  "confidence": 0.87,
  "safety_checked": true
}
```

---

## 5. Doctor Question

```json
{
  "id": "uuid",
  "question": "Should this result be repeated?",
  "source_finding_id": "finding_uuid"
}
```

Questions must help users discuss findings with healthcare professionals.

They must not contain hidden treatment recommendations.

---

## 6. Source

```json
{
  "id": "source_001",
  "title": "Medical reference",
  "publisher": "Trusted organization",
  "reference": "source location",
  "retrieved_at": "datetime"
}
```

---

## 7. Warning

```json
{
  "type": "verification_required",
  "message": "Some extracted values could not be confidently verified."
}
```

Possible warning types:

```text
verification_required
insufficient_context
low_confidence
unsupported_interpretation
safety_restriction
```

---

## 8. Confidence

Confidence values must be between:

```text
0.0 — 1.0
```

Confidence represents system confidence in the relevant output, not medical certainty.

A high confidence score must never be presented as proof of a diagnosis.

---

## 9. Safety Rules

AI output must be rejected or regenerated when it:

- Diagnoses a disease
- Prescribes medication
- Recommends changing medication
- Makes unsupported medical claims
- Presents uncertain information as certain
- Gives unsafe medical instructions

The system should prefer an explicit uncertainty message over an unsupported answer.

---

## 10. Design Principle

The AI layer produces **structured observations and educational explanations**.

The application does not present AI output as a medical diagnosis or treatment plan.