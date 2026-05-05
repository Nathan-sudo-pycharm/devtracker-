from fastapi import FastAPI, Request
from app.routers import tasks, auth

# Initialize FastAPI app
app = FastAPI(title="DevTracker", version="0.1.0")

# Register routers
app.include_router(auth.router)
app.include_router(tasks.router)

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "ok"}

# Status endpoint
@app.get("/status")
def get_status(request: Request):
    return {"app_name": request.app.title, "version": request.app.version}