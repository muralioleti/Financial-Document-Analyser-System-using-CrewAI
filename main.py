# main.py
from fastapi import FastAPI, UploadFile, File
from crew import run_financial_analysis
from database import SessionLocal, AnalysisResult
from worker import analyze_document_task

app = FastAPI()


# ---------- SYNC ENDPOINT ----------
@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """
    Synchronous analysis endpoint.
    Upload a financial document, run analysis immediately,
    and store results in the database.
    """
    # Save uploaded file
    contents = await file.read()
    filepath = f"data/{file.filename}"
    with open(filepath, "wb") as f:
        f.write(contents)

    # Run analysis directly
    results = run_financial_analysis(filepath)

    # Save results to DB
    db = SessionLocal()
    analysis_entry = AnalysisResult(
        filename=file.filename,
        investment_analysis=results["analysis"],
        risk_assessment=results["risk"]
    )
    db.add(analysis_entry)
    db.commit()
    db.refresh(analysis_entry)
    db.close()

    return {
        "id": analysis_entry.id,
        "filename": file.filename,
        "analysis": results["analysis"],
        "risk": results["risk"]
    }


# ---------- ASYNC ENDPOINT (Celery) ----------
@app.post("/analyze_async")
async def analyze_document_async(file: UploadFile = File(...)):
    """
    Asynchronous analysis endpoint.
    Upload a financial document and offload analysis to Celery worker.
    """
    # Save uploaded file
    contents = await file.read()
    filepath = f"data/{file.filename}"
    with open(filepath, "wb") as f:
        f.write(contents)

    # Send task to Celery worker
    task = analyze_document_task.delay(filepath, file.filename)
    return {"task_id": task.id, "status": "processing"}


# ---------- TASK STATUS CHECK ----------
@app.get("/task/{task_id}")
def get_task_result(task_id: str):
    """
    Check the status of an async analysis task.
    """
    from worker import celery_app
    task = celery_app.AsyncResult(task_id)

    if task.state == "PENDING":
        return {"status": "pending"}
    elif task.state == "SUCCESS":
        return {"status": "completed", "result": task.result}
    elif task.state == "FAILURE":
        return {"status": "failed", "error": str(task.info)}
    else:
        return {"status": task.state}
