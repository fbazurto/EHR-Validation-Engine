import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load variables from the .env file
load_dotenv()

# Build connection string from environment variables — no passwords in code
engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(result.fetchone())