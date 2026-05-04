from fastapi import FastAPI, Request

app = FastAPI(title="DevTracker", version="0.1.0")

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/status")
def get_status(request: Request):
    return {"app_name": request.app.title, "version": request.app.version}