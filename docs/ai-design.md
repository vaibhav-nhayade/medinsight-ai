# MedInsight AI — AI Pipeline Design

## 1. Objective

The AI pipeline converts medical reports into structured, validated, understandable, and evidence-grounded information.

The pipeline must prioritize accuracy, transparency, safety, and appropriate uncertainty.

---

## 2. Pipeline

```text
Medical Document
       ↓
Document Ingestion
       ↓
Text Extraction / OCR
       ↓
Document Structure Detection
       ↓
Medical Parameter Extraction
       ↓
Extraction Validation
       ↓
Reference Range Analysis
       ↓
Pattern Analysis
       ↓
Medical Knowledge Retrieval
       ↓
AI Reasoning
       ↓
Safety Validation
       ↓
Structured Analysis Result
```

---

## 3. Pipeline Stages

### Stage 1 — Document Ingestion

Validate:

- File type
- File size
- File readability
- Page count

Supported formats initially:

- PDF
- PNG
- JPG/JPEG

---

### Stage 2 — Text Extraction

For digital PDFs:

```text
PDF → Text extraction
```

For scanned documents:

```text
Image/PDF → Image preprocessing → OCR → Text
```

The system should preserve page and location information whenever possible.

---

### Stage 3 — Structure Detection

Identify document sections such as:

- Patient information
- Laboratory information
- Test panels
- Individual test rows
- Reference ranges
- Units
- Report dates

---

### Stage 4 — Medical Parameter Extraction

Extract:

```text
Test name
Value
Unit
Reference range
Report date
Category
Source location
Confidence
```

Extraction should use a hybrid approach:

```text
Deterministic parsing
        +
Pattern matching
        +
AI/NLP extraction
        ↓
Validation
```

---

### Stage 5 — Extraction Validation

Every extracted result receives a confidence score.

Example:

```json
{
  "confidence": 0.97,
  "needs_verification": false
}
```

Low-confidence values must be presented to the user for verification.

The system must never silently convert uncertain extraction into a high-confidence result.

---

### Stage 6 — Reference Range Analysis

Where the report provides a reference range:

```text
value < minimum → LOW
value > maximum → HIGH
otherwise → NORMAL
```

If a reliable reference range cannot be determined:

```text
status → UNKNOWN
```

The system must not invent a reference range.

---

### Stage 7 — Pattern Analysis

Analyze relationships among multiple results.

Example:

```text
Result A
   +
Result B
   +
Result C
   ↓
Potentially related pattern
```

Pattern detection may combine:

- Deterministic medical rules
- Statistical relationships
- Medical knowledge retrieval
- AI reasoning

Patterns must be described as observations or possibilities, never as diagnoses.

---

### Stage 8 — Medical Knowledge Retrieval

Relevant trusted medical information is retrieved before generating explanations.

```text
Finding
   ↓
Retriever
   ↓
Relevant evidence
   ↓
AI reasoning
```

The retrieval system should provide source information for generated explanations.

---

### Stage 9 — AI Reasoning

The AI receives structured information rather than raw uncontrolled document text whenever possible.

Inputs may include:

- Extracted test results
- Reference ranges
- Findings
- Historical values
- Retrieved evidence

Outputs should follow predefined schemas.

---

### Stage 10 — Safety Validation

Generated output is checked for:

- Diagnosis claims
- Treatment recommendations
- Medication recommendations
- Unsupported medical claims
- Excessive certainty
- Contradictions
- Missing evidence
- Unsafe instructions

Unsafe or invalid responses must be rejected or regenerated.

---

## 4. Output Structure

The pipeline should produce structured data:

```json
{
  "summary": {},
  "results": [],
  "findings": [],
  "insights": [],
  "doctor_questions": [],
  "sources": [],
  "warnings": []
}
```

---

## 5. Core Design Principle

Use deterministic software for deterministic tasks.

Use AI where interpretation, language understanding, retrieval, or reasoning is genuinely required.

The pipeline must prefer:

**Accuracy over fluency.**

**Transparency over confidence.**

**Safety over completeness.**