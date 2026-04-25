from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.models.state import CoachState
from app.agents.nodes import context_ingestor_node, assessment_node, planner_node

def create_coach_graph():
    workflow = StateGraph(CoachState)

    # Add Nodes
    workflow.add_node("ingest_context", context_ingestor_node)
    workflow.add_node("assess", assessment_node)
    workflow.add_node("plan", planner_node)

    # Define Connections
    workflow.set_entry_point("ingest_context")
    workflow.add_edge("ingest_context", "assess")
    workflow.add_edge("assess", "plan")
    workflow.add_edge("plan", END)

    # Add Memory Checkpointer for persistence
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)
