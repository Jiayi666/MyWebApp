from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config.config import MySQLConfig

DATABASE_URL = f"mysql+pymysql://{MySQLConfig.USER}:{MySQLConfig.PASSWORD}@{MySQLConfig.HOST}:{MySQLConfig.PORT}/{MySQLConfig.DATABASE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class WorkloadData(Base):
    __tablename__ = "workload_data"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String(255))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()