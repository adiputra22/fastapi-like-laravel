from fastapi import FastAPI
from app.routes.api import router as api_router
from app.config.database import engine, Base

# Create database tables (seperti php artisan migrate)
Base.metadata.create_all(bind=engine)

# Create FastAPI app (seperti Laravel Application)
app = FastAPI(
    title="My FastAPI App",
    description="Laravel-style FastAPI application",
    version="1.0.0"
)

# Include routes (seperti include routes di Laravel)
app.include_router(api_router)

@app.get("/")
def welcome():
    return {"message": "Welcome to FastAPI Laravel-style!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)