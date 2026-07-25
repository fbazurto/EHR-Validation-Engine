# the FHIR integration layer that 
# extracts data from an Observation 
# and looks up the patient's age and sex:
import requests
from datetime import date

# The base URL of the local HAPI FHIR server
FHIR_BASE = "http://localhost:8080/fhir"

# Maps LOINC codes to the field names used in the reference_ranges table
LOINC_TO_FIELD = {
    "8480-6": "systolic_bp",
    "8462-4": "diastolic_bp",
    "8867-4": "heart_rate",
    "2708-6": "oxygen_saturation",
    "9279-1": "respiratory_rate",
    "8310-5": "temperature_f"
}

def parse_observation(observation_json):
    """
    Accepts a FHIR Observation JSON object.
    Extracts field name, value, patient age, and patient sex.
    Returns a dictionary ready to pass into ValidationService.
    """

    # Extract the LOINC code from the observation
    loinc_code = observation_json["code"]["coding"][0]["code"]

    # Convert the LOINC code to the field name used in the database
    field_name = LOINC_TO_FIELD.get(loinc_code)
    if not field_name:
        return {"error": f"Unknown LOINC code: {loinc_code}"}

    # Extract the numeric value from the observation
    value = observation_json["valueQuantity"]["value"]

    # Extract the patient ID from the subject reference (ex. "Patient/1001")
    patient_reference = observation_json["subject"]["reference"]
    patient_id = patient_reference.split("/")[1]

    # Fetch the patient resource from HAPI FHIR to get age and sex
    patient_response = requests.get(
        f"{FHIR_BASE}/Patient/{patient_id}",
        headers={"Accept": "application/fhir+json"}
    )
    patient = patient_response.json()

    # Extract sex from the patient resource
    sex = "M" if patient.get("gender") == "male" else "F"

    # Calculate age from birthDate
    birth_date = date.fromisoformat(patient["birthDate"])
    today = date.today()
    age = today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )

    # Return everything ValidationService needs
    return {
        "field": field_name,
        "value": value,
        "age": age,
        "sex": sex
    }