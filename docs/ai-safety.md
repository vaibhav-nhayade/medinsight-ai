# MedInsight AI — Safety Specification

## 1. Purpose

Medical information requires a higher standard of caution than ordinary AI applications.

MedInsight AI is designed as an informational and educational system.

It must not act as a medical diagnosis or treatment system.

---

## 2. Prohibited AI Behavior

The system must not:

- Diagnose diseases
- Prescribe medication
- Recommend medication changes
- Recommend stopping medication
- Claim certainty about a medical condition
- Present speculation as fact
- Invent laboratory reference ranges
- Invent medical evidence
- Hide uncertainty
- Provide unsupported medical instructions

---

## 3. Allowed Behavior

The system may:

- Explain medical terminology
- Describe what a test generally measures
- Identify values outside the reference range provided by the report
- Explain potential relationships between findings
- Describe general educational information
- Identify changes between reports
- Generate questions for healthcare professionals
- Recommend discussing potentially important findings with a healthcare professional

---

## 4. Uncertainty

The system must explicitly communicate uncertainty.

Examples:

```text
The system could not confidently determine the reference range.
```

```text
This value should be verified against the original report.
```

```text
This finding can have multiple possible explanations and should be interpreted by a healthcare professional in context.
```

---

## 5. Reference Range Policy

The system should prioritize reference ranges supplied by the laboratory report.

If a reliable range is unavailable:

```text
status = unknown
```

The AI must not fabricate a reference range.

---

## 6. Human Verification

Low-confidence extraction must require user verification before analysis.

```text
Extraction
    ↓
Confidence Check
    ↓
Low confidence?
    ├── Yes → User Verification
    └── No  → Continue
```

---

## 7. AI Output Validation

Generated output should pass a safety validation stage before being displayed.

The validator should check for:

- Diagnostic language
- Treatment instructions
- Medication recommendations
- Unsupported claims
- Excessive certainty
- Missing evidence
- Contradictions

---

## 8. Evidence

Medical explanations should be grounded in trusted medical sources whenever possible.

The system should preserve source information associated with evidence-grounded insights.

---

## 9. Emergency Situations

MedInsight AI is not an emergency medical service.

If a user describes an urgent or potentially life-threatening situation, the system should direct them toward appropriate immediate professional/emergency care rather than attempting to manage the situation through AI-generated treatment instructions.

---

## 10. Safety Principle

> When uncertain, the system should be conservative.