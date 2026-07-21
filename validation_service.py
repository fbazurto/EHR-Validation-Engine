# Import os to access environment variables
import os

# load_dotenv reads the .env file
from dotenv import load_dotenv

# SQLAlchemy tools for connecting and running SQL
from sqlalchemy import create_engine, text

# Import RangeService to look up reference ranges
from range_service import RangeService

# Load environment variables
load_dotenv()

# Build the database engine
engine = create_engine(f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")

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
        
        # If no range found in database, we can't validate — return unknown and log it
        if not range_row:
            result ={
                "valid": False,
                "severity": "unknown",
                "message": f"No reference range found for {field} at age {age}."
            }
            self._log_event(field, value, age, sex, result)
            return result
        
        # Unpack the range values from the database row
        low_value, high_value, critical_low, critical_high = range_row
        
        # Check critical low threshold first — most urgent
        if value < critical_low:
            result ={
                "valid": False,
                "severity": "critical",
                "message": f"{field} value of {value} is critically low. Normal range is {low_value}–{high_value}. Please confirm immediately."
            }
            self._log_event(field, value, age, sex, result) 
            return result
        
        # Check critical high threshold
        if value > critical_high:
            result ={
                "valid": False,
                "severity": "critical",
                "message": f"{field} value of {value} is critically high. Normal range is {low_value}–{high_value}. Please confirm immediately."
            }
            self._log_event(field, value, age, sex, result)
            return result
        
        # Check warning low — outside normal but not critical
        if value < low_value:
            result = {
                "valid": False,
                "severity": "warning",
                "message": f"{field} value of {value} is below the normal range of {low_value}–{high_value}. Please review."
            }
            self._log_event(field, value, age, sex, result)
            return result

        # Check warning high — outside normal but not critical
        if value > high_value:
            result = {
                "valid": False,
                "severity": "warning",
                "message": f"{field} value of {value} is above the normal range of {low_value}–{high_value}. Please review."
            }
            self._log_event(field, value, age, sex, result)
            return result
        
        # Value is within normal range
        result = {
            "valid": True,
            "severity": "ok",
            "message": f"{field} value of {value} is within the normal range of {low_value}–{high_value}."
        }
        self._log_event(field, value, age, sex, result)
        return result