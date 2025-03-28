import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Thông tin kết nối SQL Server Tùng sửa sửaaa
SERVER = "ADMIN"
DATABASE = "qlsach1"
USERNAME = "sa"
PASSWORD = "Xuanxam2005."
DRIVER = "ODBC Driver 17 for SQL Server"

# Tạo chuỗi kết nối
params = urllib.parse.quote_plus(f'DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}')
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# Khởi tạo engine và session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency để tạo database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()