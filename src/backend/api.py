from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

# Import our custom engines
import engine_db
import engine_ai

router = APIRouter()

# Define the expected JSON structure from the frontend chat interface
class ChatRequest(BaseModel):
    prompt: str
    current_chart: Optional[Dict[str, Any]] = None

@router.get("/status")
def get_status():
    """
    The frontend pings this endpoint every 2 seconds.
    If a table is active, it tells the frontend to unlock the chat.
    """
    return {
        "active_table": engine_db.CURRENT_FILE_METADATA["active_table"],
        "columns": engine_db.CURRENT_FILE_METADATA["columns"]
    }

@router.post("/chat")
def process_chat(request: ChatRequest):
    """
    Receives the user's prompt, checks the database schema, 
    and asks the local LLM to generate the Chart.js JSON.
    """
    meta = engine_db.CURRENT_FILE_METADATA
    
    # Safeguard: Ensure a file has been dropped before chatting
    if not meta["active_table"]:
        raise HTTPException(status_code=400, detail="Please drop a CSV file into the data_in folder first!")
    
    # Pass the prompt, the available data columns, and the current chart state to Ollama
    chart_config = engine_ai.chat_to_modify_chart(
        user_instruction=request.prompt,
        columns=meta["columns"],
        current_chart_state=request.current_chart
    )
    
    # If the AI engine script caught an error (like Ollama being offline), pass it to the UI
    if "error" in chart_config:
        return {"error": chart_config["error"]}
        
    return {"chart_config": chart_config}
