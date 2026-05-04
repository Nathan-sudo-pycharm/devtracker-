from fastapi import FastAPI, Request
from app.routers import tasks

# Initialize FastAPI app with a title and version
app = FastAPI(title="DevTracker", version="0.1.0")

# Register the tasks router
# All /tasks endpoints are now available
app.include_router(tasks.router)

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "ok"}

# Status endpoint — reads app metadata
@app.get("/status")
def get_status(request: Request):
    return {"app_name": request.app.title, "version": request.app.version}