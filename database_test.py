import os
from sqlalchemy import create_engine, text  # type: ignore[import]

# Simple .env loader to avoid external dependency
def load_dotenv(dotenv_path=".env"):
    if not os.path.exists(dotenv_path):
        return
    with open(dotenv_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)

# Load variables from the .env file
load_dotenv()

# Build connection string from environment variables — no passwords in code
engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(result.fetchone())