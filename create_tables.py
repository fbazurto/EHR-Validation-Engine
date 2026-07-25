from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS reference_ranges (
            id INT AUTO_INCREMENT PRIMARY KEY,
            field_name VARCHAR(50),
            age_min INT,
            age_max INT,
            sex VARCHAR(10),
            low_value FLOAT,
            high_value FLOAT,
            critical_low FLOAT,
            critical_high FLOAT
        )
    """))
    conn.commit()
    print("reference_ranges table created successfully")

    # age_min and age_max are in years. A value of 0 represents patients under 1 year of age.

# Create the validation_events table to log every validation call
# This data will feed the Feature 5 dashboard later
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS validation_events (
            id INT AUTO_INCREMENT PRIMARY KEY,
            field_name VARCHAR(50),
            value FLOAT,
            age INT,
            sex VARCHAR(10),
            rule_severity VARCHAR(20),
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """))
    conn.commit()
    print("validation_events table created successfully")
    # to run: venv\Scripts\python.exe create_tables.py