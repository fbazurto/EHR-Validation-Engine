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