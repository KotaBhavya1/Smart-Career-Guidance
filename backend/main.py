from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from resume_parser import extract_resume_data  # <-- your custom module

# ----------------------------------------------------------
# Setup
# ----------------------------------------------------------
app = FastAPI(title="Smart Career Advisor API")

# Allow frontend access (adjust if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------
# Logging configuration
# ----------------------------------------------------------
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------------------------------------------------
# Folder setup
# ----------------------------------------------------------
UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# ----------------------------------------------------------
# Allowed file types
# ----------------------------------------------------------
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

# ----------------------------------------------------------
# Routes
# ----------------------------------------------------------
@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Career Advisor API!"}


@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    filename = file.filename
    extension = os.path.splitext(filename)[1].lower()

    # Validate file type
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a PDF, DOCX, or TXT file."
        )

    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save the uploaded file
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        logging.error(f"Failed to save file {filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Extract data from resume
    try:
        extracted_data = extract_resume_data(file_path)
    except Exception as e:
        logging.error(f"Error parsing resume {filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")

    return {
        "filename": filename,
        "status": "uploaded and parsed successfully",
        "extracted_data": extracted_data
    }
