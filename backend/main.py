from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import time

from detector.url_detector import analyze_url
from detector.message_detector import analyze_message
from detector.email_detector import analyze_email

app = FastAPI(title="PhishGuard API")

# Setup CORS (though frontend is served from same origin, useful for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Models
class URLScanRequest(BaseModel):
    url: str

class MessageScanRequest(BaseModel):
    message: str

class EmailScanRequest(BaseModel):
    sender: str
    subject: str
    body: str

# API Routes
@app.post("/api/scan-url")
def scan_url(request: URLScanRequest):
    try:
        result = analyze_url(request.url)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "An error occurred during URL analysis."})

@app.post("/api/scan-message")
def scan_message(request: MessageScanRequest):
    try:
        result = analyze_message(request.message)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "An error occurred during message analysis."})

@app.post("/api/scan-email")
def scan_email(request: EmailScanRequest):
    try:
        result = analyze_email(request.sender, request.subject, request.body)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "An error occurred during email analysis."})

# Mount frontend static files
# Ensure the path resolves correctly from where main.py is run
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print(f"Warning: Frontend directory not found at {frontend_path}")
