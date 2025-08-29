# tools.py
import os
import re
import logging
from dotenv import load_dotenv
load_dotenv()

# Optional search tool (crewai_tools Serper)
try:
    from crewai_tools.tools.serper_dev_tool import SerperDevTool
    search_tool = SerperDevTool()
except Exception:
    logging.info("SerperDevTool not available; search_tool set to None")
    search_tool = None

# PDF loader: LangChain's PyPDFLoader (uses pypdf)
try:
    from langchain.document_loaders import PyPDFLoader
except Exception:
    PyPDFLoader = None

class FinancialDocumentTool:
    @staticmethod
    def read_data_tool(path: str = "data/sample.pdf") -> str:
        """Read and return cleaned text content of a PDF file."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"PDF not found at path: {path}")

        if PyPDFLoader is None:
            raise RuntimeError("PyPDFLoader is required but not installed. Install pypdf & langchain.")

        loader = PyPDFLoader(path)
        docs = loader.load()
        pages = []
        for doc in docs:
            content = (doc.page_content or "").strip()
            # collapse multiple newlines into a single newline
            content = re.sub(r"\n{2,}", "\n", content)
            # normalize multiple spaces
            content = re.sub(r" {2,}", " ", content)
            pages.append(content)
        return "\n".join(pages)

class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(financial_document_data: str):
        """Simple deterministic placeholder for investment analysis."""
        if not financial_document_data:
            return {"error": "No data provided for analysis"}
        text = financial_document_data.strip()
        words = text.split()
        word_count = len(words)
        numbers = re.findall(r"-?\d[\d,\.]*", text)
        normalized = [n.replace(",", "") for n in numbers]
        sample_numbers = normalized[:12]
        return {
            "word_count": word_count,
            "sample_numbers": sample_numbers,
            "advice": (
                "Placeholder summary. For actionable investment recommendations, parse structured tables (income statement, balance sheet) "
                "and consult a licensed professional."
            ),
        }

class RiskTool:
    @staticmethod
    def create_risk_assessment_tool(financial_document_data: str):
        """Simple keyword-based risk scan."""
        if not financial_document_data:
            return {"error": "No data provided for risk assessment"}
        text = financial_document_data.lower()
        risk_keywords = [
            "debt", "default", "loss", "negative", "write-down", "impairment",
            "lawsuit", "volatility", "liability", "bankruptcy"
        ]
        found = [kw for kw in risk_keywords if kw in text]
        return {
            "found_risk_terms": found,
            "note": "This is a conservative keyword scan. For quantitative risk measurement, extract numeric exposures and run models."
        }
