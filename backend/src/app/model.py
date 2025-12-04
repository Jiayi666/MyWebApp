# Define RESTFul API routes and high level handling
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.mysql_db import get_db
from src.database import access_db
import time
import math
import os
import fcntl

# APIs
app = FastAPI()

# Multi-process CPU expensive task
@app.get("/run/backendCPUExpensiveTask/{seconds}")
def run_backend_cpu_expensive_task(seconds: int):
    start_time = time.time()
    while time.time() - start_time < seconds:
        # Perform some CPU intensive calculation
        math.factorial(1000)
    return {"message": f"CPU task ran for {seconds} seconds"}

# Multi-process file lock contention
@app.get("/run/backendIoContentionTask/{seconds}")
def run_backend_io_contention_task(seconds: int):
    start_time = time.time()
    file_path = "/tmp/backend_io_contention.txt"
    
    # Ensure file exists
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("0")

    while time.time() - start_time < seconds:
        with open(file_path, "r+") as f:
            try:
                fcntl.flock(f, fcntl.LOCK_EX)
                content = f.read()
                count = int(content) if content else 0
                f.seek(0)
                f.write(str(count + 1))
                f.truncate()
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
    return {"message": f"IO task ran for {seconds} seconds"}

# /run/dbReadTask -- concurrent DB read, start with no-join
@app.get("/run/dbReadTask/{seconds}")
def run_db_read_task(seconds: int, with_join: bool = False, db: Session = Depends(get_db)):
    start_time = time.time()
    count = 0
    while time.time() - start_time < seconds:
        access_db.get_workload_data(db)
        count += 1
    return {"message": f"DB read task ran for {seconds} seconds, performed {count} reads"}

# /run/dbWriteTask -- concurrent DB write
@app.get("/run/dbWriteTask/{seconds}")
def run_db_write_task(seconds: int, db: Session = Depends(get_db)):
    start_time = time.time()
    count = 0
    while time.time() - start_time < seconds:
        access_db.create_workload_data(db)
        count += 1
    return {"message": f"DB write task ran for {seconds} seconds, performed {count} writes"}