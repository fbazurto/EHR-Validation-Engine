# Integration test — tests the full pipeline from FHIR to validation result
# Requires HAPI FHIR running on localhost:8080 and uvicorn running on localhost:8000
import requests

# Base URLs for the two servers
FHIR_BASE = "http://localhost:8080/fhir"
VALIDATION_BASE = "http://127.0.0.1:8000"

def test_fhir_observation_critical():
    """
    Full end-to-end test:
    1. Creates a fake patient in HAPI FHIR
    2. Creates a fake Observation linked to that patient
    3. Posts the Observation to the validation engine
    4. Asserts the result is critical
    """

    # Step 1 — create a fake patient in HAPI FHIR
    patient = {
        "resourceType": "Patient"
        "gender": "female",
        "birthDate": "1979-01-01"
    }
    patient_response = requests.post(
        f"{FHIR_BASE}/Patient",
        json=patient,
        headers={"Content-Type": "application/fhir+json"}
    )
    # Confirm patient was created successfully
    assert patient_response.status_code == 201, "Patient creation failed"

    # Get the patient ID assigned by HAPI FHIR
    patient_id = patient_response.json()["id"]

    # Step 2 — create a fake Observation linked to that patient
    observation = {
        "resourceType": "Observation",
        "status": "final",
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "8480-6",
                "display": "Systolic blood pressure"
            }]
        },
        # Link to the patient created above
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        # Critically high blood pressure value
        "valueQuantity": {
            "value": 225,
            "unit": "mmHg",
            "system": "http://unitsofmeasure.org",
            "code": "mm[Hg]"
        }
    }

    # Step 3 — send the Observation to the validation engine
    validation_response = requests.post(
        f"{VALIDATION_BASE}/validate/fhir-observation",
        json=observation
    )
    # Confirm the validation engine responded successfully
    assert validation_response.status_code == 200, "Validation request failed"

    # Step 4 — assert the result is critical
    result = validation_response.json()
    assert result["severity"] == "critical", f"Expected critical, got {result['severity']}"
    assert result["valid"] == False, "Expected valid to be False"

    print(f"Integration test passed. Patient {patient_id} — result: {result['severity']}")