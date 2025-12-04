from sqlalchemy.orm import Session
from src.database.mysql_db import WorkloadData
import random
import string

def create_workload_data(db: Session):
    # Generate random string
    random_data = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    db_item = WorkloadData(data=random_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_workload_data(db: Session, limit: int = 100):
    return db.query(WorkloadData).limit(limit).all()