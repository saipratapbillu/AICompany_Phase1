from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from app.core.config import settings

odbc = (
    f"DRIVER={{{settings.db_driver}}};SERVER={settings.db_server};"
    f"DATABASE={settings.db_name};Trusted_Connection={settings.db_trusted_connection};"
    f"Encrypt={settings.db_encrypt};TrustServerCertificate=yes;"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc)}", pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
