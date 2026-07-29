# EHR Validation Engine

A middleware system that validates patient vital sign data at the point of entry before it is saved into an Electronic Health Record (EHR). The goal is to catch documentation errors early, reduce data quality problems, and give clinical informatics administrators evidence for tuning alert thresholds.

## What It Does

When a clinician enters a vital sign, the system checks whether the value makes clinical sense for the patient's age and sex. It returns a severity level — ok, warning, or critical — along with a plain language message the clinician can act on immediately.

The system accepts two input formats:
- Direct JSON for development and testing
- FHIR R4 Observation resources for realistic healthcare simulation

Every validation call is logged to a database for later analysis by a clinical informatics administrator through a dashboard.

## Features

| Feature | Description |
|---------|-------------|
| Feature 1: Vital Sign Rule Validation | Checks values like blood pressure, heart rate, oxygen saturation, respiratory rate, and temperature against age/sex-adjusted normal and critical ranges |
| Feature 2: ML Anomaly Detection | Uses Isolation Forest to flag values that look unusual compared to expected patterns, then compares results against the rule-based check |
| Feature 3: Duplicate Entry Detection | Uses fuzzy matching to identify duplicate medication or allergy entries for the same patient |
| Feature 4: Clinical Code Consistency Prototype | Checks whether a diagnosis code matches the words in a clinical note using keyword matching |
| Feature 5: Feedback Dashboard | React dashboard showing alert counts, clinician response outcomes, and rule vs ML agreement for administrators |

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Database:** MySQL, SQLAlchemy
- **FHIR Sandbox:** HAPI FHIR R4 (Docker)
- **Machine Learning:** scikit-learn (Isolation Forest)
- **Fuzzy Matching:** RapidFuzz
- **Testing:** pytest
- **Dashboard:** React (Vite)

## Project Status

| Month | Goal | Status |
|-------|------|--------|
| April | Research, environment setup, system design | Complete |
| May | Feature 1 — vital sign rule validation + FHIR integration | Complete |
| June–July | Features 2 and 3 | In progress |
| August–September | Features 4 and 5 | Planned |
| October | Integration, testing, bug fixes | Planned |
| November | Report writing, demo prep | Planned |
| December 1 | Submission | Planned |

## Setup

### Requirements
- Python 3.11+
- Docker Desktop
- MySQL database
- Node.js (for dashboard, Feature 5)

### Environment Variables
Create a `.env` file in the project root with the following: