# MedInsight AI — System Architecture

## 1. Overview

MedInsight AI follows a modular architecture consisting of:

```text
Frontend
   ↓
API Layer
   ↓
Application Services
   ↓
AI / Document Processing
   ↓
Data Layer
```

---

## 2. Main Components

### Frontend

Technology:

- Next.js
- React
- TypeScript

Responsibilities:

- User interface
- File upload
- Processing status
- Result visualization
- Report history
- User verification
- AI insight presentation

---

### Backend

Technology:

- Python
- FastAPI

Responsibilities:

- API endpoints
- Authentication and authorization
- Report management
- File handling
- Analysis orchestration
- Database access
- AI service coordination

---

### Document Processing

Responsibilities:

- PDF parsing
- Image preprocessing
- OCR
- Document structure detection
- Text normalization

---

### AI Layer

Responsibilities:

- Medical parameter extraction
- Pattern analysis
- Knowledge retrieval
- Explanation generation
- Doctor-question generation
- Safety validation

---

### Database

Technology:

**PostgreSQL**

Stores structured application data including:

- Users
- Reports
- Results
- Findings
- Insights
- Analysis runs

---

### Object Storage

Stores uploaded medical documents separately from relational data.

The database stores metadata and references to stored documents.

---

### Vector Database

Used by the RAG subsystem for retrieval of relevant medical knowledge.

The exact vector database will be selected during implementation based on project requirements.

---

## 3. Logical Architecture

```text
                    USER
                      │
                      ▼
                ┌───────────┐
                │ Frontend  │
                └─────┬─────┘
                      │
                      ▼
                ┌───────────┐
                │ FastAPI   │
                └─────┬─────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
     Report       Analysis      User
     Service      Service       Service
          │           │
          │           ▼
          │      AI Pipeline
          │           │
          │    ┌──────┼──────┐
          │    ▼      ▼      ▼
          │   OCR  Extract  RAG
          │           │
          │           ▼
          │       Reasoning
          │           │
          │           ▼
          │        Safety
          │
          └───────────┬───────────
                      ▼
               ┌──────────────┐
               │ PostgreSQL   │
               └──────────────┘
```

---

## 4. Architectural Principle

The system will initially use a **modular monolith** rather than independent microservices.

This keeps development and deployment simple while maintaining clear boundaries between components.

Individual services can be separated later if scale or operational requirements justify it.

---

## 5. Data Flow

```text
Upload
  ↓
Report Created
  ↓
Document Stored
  ↓
Processing Started
  ↓
OCR / Text Extraction
  ↓
Parameter Extraction
  ↓
Validation
  ↓
Analysis
  ↓
RAG
  ↓
AI Reasoning
  ↓
Safety Validation
  ↓
Results Stored
  ↓
Frontend Displays Results
```

---

## 6. Security Boundaries

Sensitive documents must not be exposed directly to the frontend.

The frontend communicates with the backend through authenticated APIs.

Secrets and API keys must remain server-side.

Real patient information must never be included in source control or development datasets.