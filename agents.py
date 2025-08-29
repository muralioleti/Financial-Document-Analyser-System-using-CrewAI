# agents.py
import os
from dotenv import load_dotenv
load_dotenv()

from crewai.agents import Agent
from tools import search_tool, FinancialDocumentTool

# LLM placeholder / best-effort initialization. Replace with your project's LLM if required.
llm = None
try:
    from langchain.chat_models import ChatOpenAI
    llm = ChatOpenAI(temperature=0.0)
except Exception:
    # Fallback: keep None (CrewAI SDK may accept None or its own llm config)
    llm = None

# Financial Analyst - evidence-based, conservative
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal=(
        "Read the provided financial document (from tools) and produce a clear,"
        " evidence-based analysis. If information is missing, state that explicitly."
        " Highlight key metrics, risks, assumptions, and provide conservative investment considerations."
    ),
    verbose=True,
    memory=False,
    backstory=(
        "You are an experienced financial analyst who prioritizes accuracy and transparency."
    ),
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    llm=llm,
    max_iter=3,
    max_rpm=60,
    allow_delegation=True,
)

# Verifier - validates file readability and basic metadata
verifier = Agent(
    role="Financial Document Verifier",
    goal=(
        "Confirm uploaded file is a readable PDF, attempt parsing via the PDF tool, "
        "and report page count / parsing issues. If unreadable, explain why."
    ),
    verbose=True,
    memory=False,
    backstory="You validate file type and parsing results and report issues concisely.",
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=2,
    max_rpm=60,
    allow_delegation=False,
)

# Investment advisor (objective and conservative)
investment_advisor = Agent(
    role="Investment Advisor",
    goal=(
        "Based on verified document & analysis, provide objective and conservative investment options "
        "with rationale. Label hypothetical suggestions and avoid promoting specific third-party products."
    ),
    verbose=True,
    memory=False,
    backstory="Provide balanced options and explain trade-offs.",
    tools=[search_tool],
    llm=llm,
    max_iter=2,
    max_rpm=60,
    allow_delegation=False,
)

# Risk assessor - evidence-focused
risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal=(
        "Analyze document and context to identify real risk factors, estimated impacts, and mitigations. "
        "Be explicit about uncertainties."
    ),
    verbose=True,
    memory=False,
    backstory="Focus on realistic risk quantification and practical mitigations.",
    tools=[search_tool],
    llm=llm,
    max_iter=2,
    max_rpm=60,
    allow_delegation=False,
)
