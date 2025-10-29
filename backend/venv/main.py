from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os

# Create app instance
app = FastAPI(title="Smart Career Advisor API")

# Allow frontend (React) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create 'uploads' folder if it doesn’t exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Career Advisor API!"}

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Endpoint to upload and save resume file locally.
    """
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename, "status": "uploaded successfully"}
