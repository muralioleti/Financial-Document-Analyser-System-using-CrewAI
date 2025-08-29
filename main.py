# main.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
import asyncio
import logging

from crew import run_financial_analysis

app = FastAPI(title="Financial Document Analyzer")
logging.basicConfig(level=logging.INFO)

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights"),
):
    # Basic file validation
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    os.makedirs("data", exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = os.path.join("data", f"financial_document_{file_id}.pdf")

    try:
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        if not query or query.strip() == "":
            query = "Analyze this financial document for investment insights"

        # run_financial_analysis is blocking; run in thread to avoid blocking event loop
        result = await asyncio.to_thread(run_financial_analysis, query.strip(), file_path)

        # Convert result to serializable form (Crew result may be complex)
        return JSONResponse(
            content={
                "status": "success",
                "query": query,
                "analysis": str(result),
                "file_processed": filename,
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Error processing document")
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            logging.warning("Failed to remove temp file", exc_info=True)
