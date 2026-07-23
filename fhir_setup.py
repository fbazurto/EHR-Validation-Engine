# requests is a Python library for making HTTP calls
# install it first with: venv\Scripts\python.exe -m pip install requests
import requests
import json

# The base URL of the local HAPI FHIR server
FHIR_BASE = "http://localhost:8080/fhir"

# This is a fake Patient resource in FHIR R4 format
# resourceType and birthDate are required fields
patient = {
    "resourceType": "Patient",
    "gender": "female",
    "birthDate": "1979-01-01"  # This makes the patient 45 years old
}

# POST the patient to HAPI FHIR
response = requests.post(
    f"{FHIR_BASE}/Patient",
    json=patient,
    headers={"Content-Type": "application/fhir+json"}
)

# Get the patient ID from the response — must come AFTER the POST
patient_id = response.json()["id"]

# Print the response to confirm patient was created
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))

# to run: venv\Scripts\python.exe fhir_setup.py
# output 201 means the patient was created successfully

# This is a fake Observation resource representing a systolic blood pressure reading
observation = {
    "resourceType": "Observation",
    "status": "final",
    "code": {
        "coding": [{
            "system": "http://loinc.org",
            "code": "8480-6",          # LOINC code for systolic blood pressure
            "display": "Systolic blood pressure"
        }]
    },
    # Link this observation to our fake patient
    "subject": {
        "reference": f"Patient/{patient_id}"
    },
    # The actual vital sign value
    "valueQuantity": {
        "value": 225,                  # The blood pressure reading
        "unit": "mmHg",
        "system": "http://unitsofmeasure.org",
        "code": "mm[Hg]"
    }
}

# POST the observation to HAPI FHIR
obs_response = requests.post(
    f"{FHIR_BASE}/Observation",
    json=observation,
    headers={"Content-Type": "application/fhir+json"}
)

# Print the response so to see the observation ID assigned by the server
print(f"Observation Status: {obs_response.status_code}")
print(json.dumps(obs_response.json(), indent=2))

# to run: venv\Scripts\python.exe fhir_setup.py