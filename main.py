# FastAPI is the web framework that creates the API
from fastapi import FastAPI

# BaseModel is used to define what JSON shape expected in requests
from pydantic import BaseModel

# Import your ValidationService to run the actual validation logic
from validation_service import ValidationService

# Create the FastAPI app instance
app = FastAPI()

# Create one ValidationService instance to reuse across all requests
validation_service = ValidationService()

# Define the shape of the request body using Pydantic
# This tells FastAPI exactly what fields to expect in the JSON
class VitalSignRequest(BaseModel):
    field: str       # e.g. "systolic_bp"
    value: float     # e.g. 225.0
    age: int         # e.g. 45
    sex: str         # e.g. "F"

# This is the hello world endpoint (keep it for testing)
@app.get("/")
def root():
    return {"message": "EHR Validation Engine is running"}

# POST /validate/vitals — the main Feature 1 endpoint
# Accepts a vital sign and returns ok, warning, or critical
@app.post("/validate/vitals")
def validate_vitals(request: VitalSignRequest):
    """
    Accepts a vital sign value and returns a validation result.
    Also logs every call to the validation_events table.
    """
    # Call ValidationService with the values from the request body
    result = validation_service.validate_vital(
        field=request.field,
        value=request.value,
        age=request.age,
        sex=request.sex
    )
    # Return the result as JSON
    return result

# To start the server: venv\Scripts\python.exe -m uvicorn main:app --reload
# Then go to http://127.0.0.1:8000/docs in your browser.
# Should see the /validate/vitals endpoint listed there.
# Click it, click Try it out, and test these three cases separately
# The /docs page only accepts one JSON object at a time:

# Normal: {"field": "systolic_bp", "value": 115, "age": 45, "sex": "F"}

# Warning: {"field": "systolic_bp", "value": 145, "age": 45, "sex": "F"}

# Critical: {"field": "systolic_bp", "value": 225, "age": 45, "sex": "F"}


# Add the new endpoint:
# Import the FHIR parser
from fhir_parser import parse_observation

# POST /validate/fhir-observation — accepts a raw FHIR Observation JSON
# Extracts field, value, age, and sex then runs through ValidationService
@app.post("/validate/fhir-observation")
def validate_fhir_observation(observation: dict):
    """
    Accepts a raw FHIR Observation resource.
    Parses it, looks up the patient, and returns a validation result.
    """
    # Parse the FHIR Observation to extract validation inputs
    parsed = parse_observation(observation)

    # If parsing failed, return the error
    if "error" in parsed:
        return parsed

    # Run the parsed values through ValidationService
    result = validation_service.validate_vital(
        field=parsed["field"],
        value=parsed["value"],
        age=parsed["age"],
        sex=parsed["sex"]
    )

    return result