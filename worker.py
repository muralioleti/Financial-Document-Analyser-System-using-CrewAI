# worker.py
from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("financial_analyzer", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task(bind=True)
def run_analysis_task(self, query: str, file_path: str):
    # import locally to avoid circular import at module load time in some setups
    from crew import run_financial_analysis
    return str(run_financial_analysis(query=query, file_path=file_path))
