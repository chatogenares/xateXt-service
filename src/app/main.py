from fastapi import FastAPI, HTTPException, status
from fastapi import FastAPI, HTTPException, status
from dotenv import load_dotenv
import os
import uuid
from typing import Any

# Local imports
from .schemas import AnalysisRequest, AnalysisResponse, ServiceOutput
from .crud import create_analysis_record, get_analysis_record

load_dotenv()

app = FastAPI(
    title="AI Content Analyzer Service",
    description="Analyzes text content based on a specified focus area and returns structured findings.",
    version="1.0.0"
)

def _simulate_ai_analysis(text: str, focus: str) -> tuple[ServiceOutput, str]:
    """
    [CORE BUSINESS LOGIC SIMULATION]
    This function simulates the complex call to an external LLM/AI API.
    In a production system, this is where the actual API client call (e.g., OpenAI, Anthropic) goes.
    """
    print(f"--- [AI Simulation] Analyzing text (Focus: {focus})... ---")
    
    # Simple heuristic simulation based on input content
    if "quantum computing" in text.lower() and "potential" in focus.lower():
        summary = "The text heavily discusses the potential of quantum computing breakthroughs in the next decade."
        confidence = 0.92
        findings = [
            {"key": "Breakthrough Focus", "detail": "Quantum computing is cited as a major area of research."},
            {"key": "Timeline", "detail": "Potential impact noted within 10 years."}
        ]
    elif "climate change" in text.lower() and "policy" in focus.lower():
        summary = "The core message is the urgent need for immediate, sweeping global policy changes regarding emissions."
        confidence = 0.88
        findings = [
            {"key": "Urgency", "detail": "High urgency level specified across global policy discussions."},
            {"key": "Recommended Action", "detail": "Requires international treaties and immediate industrial transition."}
        ]
    else:
        summary = f"Analysis focused on '{focus}' yielded general insights about the provided text."
        confidence = 0.75
        findings = [
            {"key": "General Insight", "detail": "The text discusses multiple varied topics, requiring a nuanced summary."}
        ]
        
    output = ServiceOutput(
        status="SUCCESS",
        summary=summary,
        confidence_score=confidence,
        detailed_findings=findings
    )
    
    # Return the structured output and a simple message
    return output, "Analysis simulation completed successfully."


@app.post("/analyze", response_model=AnalysisResponse, status_code=status.HTTP_200_OK)
async def analyze_content(request: AnalysisRequest):
    """
    Endpoint to submit text for AI analysis.
    """
    request_id = str(uuid.uuid4())
    input_text_length = len(request.text_content)
    
    try:
        # 1. Core Analysis Call
        analysis_result, status_message = _simulate_ai_analysis(
            text=request.text_content, 
            focus=request.focus_area
        )
        
        # 2. Persistence Layer Interaction (CRUD)
        crud_data = {
            "request_id": request_id,
            "input_data": request.model_dump(),
            "analysis_result": analysis_result.model_dump()
        }
        create_analysis_record(request_id, request.model_dump(), analysis_result.model_dump())
        
        # 3. Final API Response Construction
        response = AnalysisResponse(
            request_id=request_id,
            input_text_length=input_text_length,
            analysis_result=analysis_result
        )
        return response

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Analysis failed due to a backend error: {str(e)}"
        )

@app.get("/history/{request_id}", response_model=Any)
async def get_history(request_id: str):
    """
    Retrieves the saved record for a specific request ID.
    """
    record = get_analysis_record(request_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    return record
