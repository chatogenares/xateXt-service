from typing import Dict, Any

def process_text(text: str) -> Dict[str, Any]:
    """
    Simulated text processing logic.
    In a real system, this would call an AI model or external service.
    """
    word_count = len(text.split())
    char_count = len(text)

    summary = text[:120] + "..." if len(text) > 120 else text

    return {
        "summary": summary,
        "word_count": word_count,
        "char_count": char_count,
        "status": "processed"
    }
