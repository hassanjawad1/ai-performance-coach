from typing import Annotated, TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

class CoachState(TypedDict):
    # Chat history for context awareness
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Ingested Context
    calendar_summary: str
    # Reasoning & Plans
    assessment_logic: str
    current_plan: str
    explanation: str
    streak: int 
    user_id: str