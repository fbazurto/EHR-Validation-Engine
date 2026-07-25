import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables from .env file
load_dotenv()

# Build the database engine using environment variables
engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)

class RangeService:
    def get_range(self, field_name, age, sex):
        """
        Queries the reference_ranges table and returns the matching row
        for the given field, age, and sex.
        Returns None if no matching range is found.
        """
        with engine.connect() as conn:
            # Try to find a sex-specific range first
            result = conn.execute(text("""
                SELECT low_value, high_value, critical_low, critical_high
                FROM reference_ranges
                WHERE field_name = :field
                AND :age BETWEEN age_min AND age_max
                AND sex = :sex
            """), {"field": field_name, "age": age, "sex": sex})
            
            row = result.fetchone()
            
            # If no sex-specific range found, fall back to 'any'
            if not row:
                result = conn.execute(text("""
                    SELECT low_value, high_value, critical_low, critical_high
                    FROM reference_ranges
                    WHERE field_name = :field
                    AND :age BETWEEN age_min AND age_max
                    AND sex = 'any'
                """), {"field": field_name, "age": age})
                row = result.fetchone()
            
            return row