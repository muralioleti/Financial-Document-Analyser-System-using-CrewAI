# crew.py
from crewai import Crew, Process
from agents import verifier, financial_analyst, investment_advisor, risk_assessor
from task import (
    analyze_financial_document,
    investment_analysis,
    risk_assessment,
    verification,
)

# Assemble Crew with agents and tasks
financial_crew = Crew(
    agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
    tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
    process=Process.sequential,
    verbose=True,
)

def run_financial_analysis(query: str, file_path: str):
    """
    Kickoff the Crew run. Inputs:
      - query: user query / analysis prompt
      - file_path: path to uploaded PDF
    Returns Crew result object (convert to string or JSON for API).
    """
    inputs = {"query": query, "file_path": file_path}
    result = financial_crew.kickoff(inputs=inputs)
    return result
