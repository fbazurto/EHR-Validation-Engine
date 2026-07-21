from validation_service import ValidationService

# Create an instance of ValidationService
vs = ValidationService()

# Test a normal blood pressure
print(vs.validate_vital("systolic_bp", 115, 45, "F"))

# Test a warning blood pressure
print(vs.validate_vital("systolic_bp", 145, 45, "F"))

# Test a critical blood pressure
print(vs.validate_vital("systolic_bp", 225, 45, "F"))