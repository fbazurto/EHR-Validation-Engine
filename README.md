# FHIR Vital Sign Data-Quality Validation and Feednback Engine

A system that chedcks a patient's vital sign data for possible errors before it gets saved into an Electronic Health Record (EHR). When a nurse or medical assistant enters a blood pressure reading , this system checks whether the number fits within the normal range for the patient's age and sex. If something looks wrong, it returns a warning or a critical alert with a plain message explaining what the problem might be. 

The system works with two input formats: simple JSON for testing and FHIR R4 Observation resources, which is the standard data format used by real hospital  systems like EPIC.

IMPORTANT: This project uses fake patient data only. The alert thresholds come from published medical references but have not been reviewed by a doctor. When this system flags something as critical, that means it's a data-quality concern NOT a medical emergency. This project is a demonstration for a capstone class and is not meant for use in a real hospital.

## What Each Feature Does


| Feature | What it does |
|---------|-------------|
| Feature 1: Input Validation and Rules | Checks two things separately: first, is the submitted data complete and correctly formatted? Second, does the vital sign value fall within a normal range for this patient? Returns ok, warning, or critical. Logs every check into the database.  |
| Feature 2: Unit Conversion | Before checking any value, convert it to one standard unit. For example, if someone submits temperature in Fahrenheit, convert it to Celsius first. This prevents false alerts caused by the wrong unit rather than a wrong value. Saves both the original and converted value so you cab tell what kind of error ocurred. |
| Feature 3: Additional Checks | Additional rules that go beyond simple range checks. For example: oxygen saturation can never be above 100%, systolic blood pressure must always be higher than diastolic, and a reasing with a future timestamp gets flagged. |
| Feature 4: Duplication Detection | Checks whether thte same vital sign was already submitted for the same patient recently. Returns a confidence level: possible duplicate, probable duplicate, or exact duplicate, along with a reason. Never automatically deletes anything. Always asks a human to review. |
| Feature 5: Feedback Dashboard |A React web page for the person managing the system. Shows things like how many alerts fired per 50 submissions, how often the clinicians accepted or ignored alerts. |

## How a Request Gets Processed
Every request goes through these steps in order:
1. Read the input (FHIR Observation or simple JSON)
2. Check that the required fields are present (status, LOINC code, patient ID, value, unit)
3. Check that the unit is one that the system recognizes.
4. Convert the value to a standard unit (e.g. Fahrenheit -> Celsius)
5. Check the converted value against the rules for this patient's age and sex.
6. Run any extra checks (oxygen over 100%, systolic s diastolic, etc.)
7. Save the event to the database (original value, converted value, rule version, result)
8. Return the result with plain language explanation

## Unit COnversion
This system converts everything to one agreed-upon unit before checking anything. Those agreed-upon units are:

| Vital Sign | Standard Unit Used |
|---------|-------------|
| Temperature: Celsius (°C) |
| Weight: Kilograms (kg) |
| Blood Pressure: mmHg |
| Oxygen Saturation: Percent (%) |
| Heart Rate: Beats per minute |
| Respiratory rate: Beats per minute |

Both the original submitted value and the converted value are saved in the database. This way you cab tell the difference between someone who entered the wrong number vs someone who entered the right number in the wrong unit.

## Why Rules Have Version Numbers
The alert thresholds in this system can change. For example, the threshold for a critical systolic blood pressure might start at 180 mmHg and later get adjusted to 160 mmHg.

If the databasr doesn't track which version iff the rule was used for each alert, you can't tell which alerts fires at 180 abd which fired at 160. That makes it impossible to whether the change helped or not.

Every rule in this project has a version number and an effective data saved in the database. Every logged alert records which rule version triggered it. This lets an administraator compare alert rates before and after a threshold change and make data-driven decisions.

Each rule stores:

1. A short rule ID (e.g. sbp-adult-critical-high)
2. Which vital sign it applies to
3. The age range it covers
4. The warning and critical thresholds
5. Where the threshold number came from
6. The version number and date it became active

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Database:** MySQL hosted on cikeys.com, Saccessed through sQLAlchemy and PyMySQL
- **Fake EHR Server:** HAPI FHIR R4 running in Docker (this is the sandbox for testing, not a real hospital system)
- **Duplicate mathcing:** RapidFuzz(Feature 4)
- **Testing:** pytest
- **Dashboard:** React with Vite

All patient data in this project is fake. No real patient data is used anywhere.

## API Endpoints
Method	Endpoint	                   What It Does
GET	     /	                           Checks that the server is running
POST	/validate/vitals	           Validates a vital sign submitted as simple JSON
POST	/validate/fhir-observation	   Validates a FHIR R4 Observation resource

Example — Normal Value
POST /validate/vitals
{
  "field": "systolic_bp",
  "value": 115,
  "age": 45,
  "sex": "F"
}

{
  "valid": true,
  "severity": "ok",
  "message": "systolic_bp value of 115.0 is within the normal range of 90.0–120.0."
}

Example — Problem Detected
POST /validate/vitals
{
  "field": "systolic_bp",
  "value": 225,
  "age": 45,
  "sex": "F"
}
{
  "valid": false,
  "severity": "critical",
  "message": "systolic_bp value of 225.0 is critically high. Normal range is 90.0–120.0. Please verify the value and unit before submitting."
}


## Project Status

| Month | Goal | Status |
|-------|------|--------|
| April | Research, environment setup, system design | Complete |
| May - July | Feature 1 — vital sign rule validation + FHIR integration, unit tests, integration test | Complete |
| September 2026 | Features 2 and 3- unit conversion and extra data quality rules | In progress |
| October 2026 | Feature 4- duplicate detection and full integration testing| Planned |
| Noember 2026 | Feature 5 - React dashboard, final report, demo prep | Planned |
| December 2026 | Submission | Planned |

## Setup

### Requirements
- Python 3.11+
- Docker Desktop
- MySQL database
- Node.js (for dashboard, Feature 5)

### Step 1- Create your Environment Variables File
Create a `.env` file in the project root with the following:
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_NAME=ehr_validation

### Step 2 — Install Python Packages

python -m venv venv
venv\Scripts\activate
venv\Scripts\python.exe -m pip install fastapi uvicorn sqlalchemy pymysql python-dotenv rapidfuzz pytest httpx scikit-learn pandas joblib requests

### Step 3 — Create the Database Tables and Load Data

venv\Scripts\python.exe create_tables.py
venv\Scripts\python.exe seed_data.py

### Step 4 — Start the Fake EHR Server
docker run -p 8080:8080 hapiproject/hapi:latest

This starts HAPI FHIR on your computer at http://localhost:8080. It's a fake hospital server used for testing. Run fhir_setup.py to create fake patient records inside it.

### Step 5 — Start the API
venv\Scripts\python.exe -m uvicorn main:app --reload

Go to http://127.0.0.1:8000/docs to test all endpoints interactively.

### Step 6 — Run Tests
# Unit tests
venv\Scripts\python.exe -m pytest test_validation.py -v

# Full end-to-end test (HAPI FHIR and uvicorn must both be running)
Unit tests:
venv\Scripts\python.exe -m 

Full end-to-end test (HAPI FHIR and uvicorn must both be running)
pytest test_integration.py -v

## Where the Reference Ranges Come From

The normal and critical thresholds in this project come from:

Medscape Clinical Reference — Normal Vital Signs
University of Iowa Health Care — Pediatric Vital Signs Normal Ranges (Flynn et al. 2017)

Blood pressure ranges are split by sex for patients aged 1 through 17 using the Iowa pediatric reference. All other vital signs use age-grouped ranges that apply to both sexes. These are demonstration thresholds only and have not been reviewed by a licensed clinician.
