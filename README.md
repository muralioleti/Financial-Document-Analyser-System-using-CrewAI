### **Financial Document Analyzer**

- A financial document analysis system built using CrewAI, FastAPI, and Celery.

- This project analyzes financial documents (PDF, DOCX, TXT) to extract investment opportunities and risk assessments.

- Supports both synchronous API calls and asynchronous processing (via Celery + Redis queue).

- Results are stored in an SQLite database.

### **Features**

- AI-powered financial document analysis (CrewAI agents).
- REST API with FastAPI.
- Supports sync and async analysis.
- Results stored in SQLite database.
- Queue worker model with Celery + Redis.
- Upload documents and retrieve analysis results anytime.

### **Bugs Fixed**

**1. Agent misconfiguration**

- Agents were not properly structured with roles/goals.
- Fixed by rewriting agents.py with clear definitions for Financial Analyst and Risk Manager.

**2. Task bugs**

- Tasks didn’t map correctly to agents.
- Fixed in tasks.py by properly associating tasks with each agent.

**3. Crew pipeline issues**

- crew.py had execution errors.
- Fixed by creating a clean run_financial_analysis(filepath) function that executes agents in sequence and returns structured results.

**4. Prompt inefficiency**

- Overly vague prompts led to inconsistent results.
- Fixed with concise, clear prompts in tasks.py.

**5. API errors**

- main.py failed when handling file uploads.
- Fixed by saving uploads temporarily and passing file paths to the crew pipeline.

**6. Missing async support**

- Added /analyze_async endpoint and /task/{task_id} to fetch Celery task results.

### **Installation**

**1. Clone Repository**
`git clone https://github.com/your-username/financial-analyzer.git`
`cd financial-analyzer`

**2. Create Virtual Environment**
`python -m venv venv`
`source venv/bin/activate`
`venv\Scripts\activate`

**3. Install Requirements**
`pip install -r requirements.txt`

**4. Setup Environment Variables**
`REDIS_URL=redis://localhost:6379/0`
`DATABASE_URL=sqlite:///./analysis.db`

### **Running the Project**

**1. Start FastAPI Server**
`uvicorn main:app --reload`
App runs at: http://127.0.0.1:8000

**2. Start Redis**
Make sure Redis is running locally:
`redis-server`

**3. Start Celery Worker**
`celery -A worker.celery_app worker --loglevel=info`
