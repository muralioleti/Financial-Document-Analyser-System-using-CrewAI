# task.py
from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import FinancialDocumentTool

# Main document analysis (uses financial_analyst)
analyze_financial_document = Task(
    description=(
        "Verify the PDF can be parsed, read contents, extract key financial metrics (if present), "
        "and produce an evidence-based analysis including key metrics, risks, and suggested next steps."
    ),
    expected_output=(
        "Structured analysis: verification summary, key metrics (if available), top 3 risks, and follow-up questions."
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

investment_analysis = Task(
    description="Produce conservative investment options based on the analysis and document.",
    expected_output="Short list of conservative investment ideas (labelled hypothetical).",
    agent=investment_advisor,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

risk_assessment = Task(
    description="Produce a concise risk assessment based on document and market context.",
    expected_output="Prioritized list of real risks, estimated impacts, and mitigations.",
    agent=risk_assessor,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

verification = Task(
    description="Verify the uploaded file can be parsed as a PDF and summarize metadata (pages, size).",
    expected_output="Document metadata and parsing notes.",
    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)
