# pytest is the testing library — run all tests with: pytest test_validation.py
import pytest
from validation_service import ValidationService

# Create one ValidationService instance to use across all tests
vs = ValidationService()

def test_normal_bp():
    # A normal adult systolic blood pressure should return ok
    result = vs.validate_vital("systolic_bp", 115, 45, "F")
    assert result["severity"] == "ok"
    assert result["valid"] == True

def test_high_bp_warning():
    # A mildly elevated BP should return warning, not critical
    result = vs.validate_vital("systolic_bp", 145, 45, "F")
    assert result["severity"] == "warning"
    assert result["valid"] == False

def test_critical_high_bp():
    # A dangerously high BP should return critical
    result = vs.validate_vital("systolic_bp", 225, 45, "F")
    assert result["severity"] == "critical"
    assert result["valid"] == False

def test_normal_heart_rate():
    # A normal adult heart rate should return ok
    result = vs.validate_vital("heart_rate", 75, 30, "M")
    assert result["severity"] == "ok"
    assert result["valid"] == True

def test_low_heart_rate():
    # A dangerously low heart rate should return critical
    result = vs.validate_vital("heart_rate", 35, 30, "M")
    assert result["severity"] == "critical"
    assert result["valid"] == False

def test_high_heart_rate():
    # An elevated but not critical heart rate should return warning
    result = vs.validate_vital("heart_rate", 120, 30, "M")
    assert result["severity"] == "warning"
    assert result["valid"] == False

def test_normal_oxygen():
    # A normal oxygen saturation should return ok
    result = vs.validate_vital("oxygen_saturation", 98, 25, "F")
    assert result["severity"] == "ok"
    assert result["valid"] == True

def test_unknown_field():
    # A field that doesn't exist in the database should return unknown
    result = vs.validate_vital("glucose", 100, 45, "F")
    assert result["severity"] == "unknown"
    assert result["valid"] == False