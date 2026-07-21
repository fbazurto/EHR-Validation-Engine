from range_service import RangeService

# Create one instance of RangeService to reuse across all calls
range_service = RangeService()

class ValidationService:
    def validate_vital(self, field, value, age, sex):
        """
        Validates a vital sign value against reference ranges.
        Returns a dictionary with valid (bool), severity (str), and message (str).
        Severity levels: 'ok', 'warning', 'critical'
        """
        
        # Look up the reference range for this field, age, and sex
        range_row = range_service.get_range(field, age, sex)
        
        # If no range found in database, we can't validate — return unknown
        if not range_row:
            return {
                "valid": False,
                "severity": "unknown",
                "message": f"No reference range found for {field} at age {age}."
            }
        
        # Unpack the range values from the database row
        low_value, high_value, critical_low, critical_high = range_row
        
        # Check critical low threshold first — most urgent
        if value < critical_low:
            return {
                "valid": False,
                "severity": "critical",
                "message": f"{field} value of {value} is critically low. Normal range is {low_value}–{high_value}. Please confirm immediately."
            }
        
        # Check critical high threshold
        if value > critical_high:
            return {
                "valid": False,
                "severity": "critical",
                "message": f"{field} value of {value} is critically high. Normal range is {low_value}–{high_value}. Please confirm immediately."
            }
        
        # Check warning low — outside normal but not critical
        if value < low_value:
            return {
                "valid": False,
                "severity": "warning",
                "message": f"{field} value of {value} is below the normal range of {low_value}–{high_value}. Please review."
            }
        
        # Check warning high — outside normal but not critical
        if value > high_value:
            return {
                "valid": False,
                "severity": "warning",
                "message": f"{field} value of {value} is above the normal range of {low_value}–{high_value}. Please review."
            }
        
        # Value is within normal range
        return {
            "valid": True,
            "severity": "ok",
            "message": f"{field} value of {value} is within the normal range of {low_value}–{high_value}."
        }