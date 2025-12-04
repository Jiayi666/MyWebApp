from src.app.model import app
from src.database.mysql_db import engine, Base

# Create tables on startup
# In a real production app, you might use Alembic for migrations, 
# but for this simple app, create_all is fine.
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not connect to database to create tables. Error: {e}")

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
