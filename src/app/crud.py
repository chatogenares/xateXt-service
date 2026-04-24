from typing import Dict, Any, Optional
from datetime import datetime

# Simulated in-memory database
_database_records: Dict[str, Dict[str, Any]] = {}

def create_analysis_record(request_id: str, input_data: dict, result_data: dict) -> Dict[str, Any]:
    """
    Creates a new record of the analysis result in the simulated database.
    """
    record = {
        "record_id": f"record_{hash(request_id)}",
        "request_id": request_id,
        "input_data": input_data,
        "analysis_result": result_data,
        "created_at": datetime.utcnow().isoformat()
    }
    _database_records[request_id] = record
    print(f"--- [DB] Successfully recorded analysis for {request_id} ---")
    return record

def get_analysis_record(request_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a specific analysis record by its request_id.
    """
    return _database_records.get(request_id)
