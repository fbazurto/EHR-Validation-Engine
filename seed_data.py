import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)

df = pd.read_csv("reference_ranges.csv")
df.to_sql("reference_ranges", con=engine, if_exists="append", index=False)
print(f"Inserted {len(df)} rows successfully")