from pydantic import BaseModel, Field
from typing import List, Optional

# --- Model for Core Output ---
class ServiceOutput(BaseModel):
    """Schema for the structured output of the core business logic."""
    status: str = Field(description="The overall status of the process (e.g., SUCCESS, FAILURE).")
    summary: str = Field(description="A concise, human-readable summary of the results.")
    confidence_score: float = Field(description="The model's confidence in the generated summary, ranging from 0.0 to 1.0.")
    detailed_findings: List[dict] = Field(description="A list of structured findings extracted from the input text.")

# --- Model for Input ---
class AnalysisRequest(BaseModel):
    """Schema for the input data provided to the service."""
    text_content: str = Field(description="The raw text that needs to be analyzed and summarized.")
    focus_area: str = Field(description="The specific area the user wants the analysis to focus on.")

# --- Model for API Response ---
class AnalysisResponse(BaseModel):
    """The final structured response returned to the client."""
    request_id: str = Field(description="Unique identifier for the analysis request.")
    input_text_length: int = Field(description="The character length of the input text.")
    analysis_result: ServiceOutput
