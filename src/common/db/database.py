from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASSWORD")
db_database = os.environ.get("DB_DATABASE")
db_port = os.environ.get("DB_PORT") 
DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_database}"

engine = create_engine(
  DATABASE_URL,
  pool_size=10,
  max_overflow=20,
  pool_pre_ping=True,
)

SessionLocal = sessionmaker(
  bind=engine,
  autoflush=False,
  autocommit=False,
)