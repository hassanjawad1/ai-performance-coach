from app.models.state import CoachState
from app.agents.prompts import ASSESSMENT_PROMPT, PLANNER_PROMPT
from app.services.calender import calendar_manager
from langchain_openai import ChatOpenAI
import os

# Define the OpenRouter configuration
llm = ChatOpenAI(
    # Explicitly pull the key from your env
    api_key=os.getenv("OPENAI_API_KEY"), 
    model="google/gemini-2.5-flash-lite",
    openai_api_base="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "AI Performance Coach",
    }
)

async def context_ingestor_node(state: CoachState):
# Fetch REAL data from Google Calendar
    actual_calendar = calendar_manager.get_todays_context()
    return {
        "calendar_summary": actual_calendar
    }

async def assessment_node(state: CoachState):
    
    calendar_data = state.get('calendar_summary')


    response = await llm.ainvoke([
        ("system", ASSESSMENT_PROMPT),
        ("user", f"Context: {calendar_data}")
    ])
    return {"assessment_logic": response.content}


async def planner_node(state: CoachState):
    user_msg = state["messages"][-1].content.lower()
    
    if "tech" in user_msg:
        persona = "### ROLE: Senior AI Engineer\nFocus on architecture, clean code, and logic."
    elif "gym" in user_msg or "be tough" in user_msg:
        persona = "### ROLE: Hardcore Drill Sergeant\nBe aggressive, brief, and push for physical limits."
    else:
        persona = "### ROLE: High-Performance Habit Coach\nFocus on discipline, consistency, and mental clarity."

    # 2. Logic for Streak (Fetch from state)
    streak_val = state.get("streak", 0)
    streak_text = f"The user is on a {streak_val}-day burn! Keep the fire alive." if streak_val > 0 else "This is day 1. Let's start strong."

    # 3. Format the prompt with our variables
    formatted_prompt = PLANNER_PROMPT.format(
        persona_prefix=persona,
        streak_info=streak_text
    )

    # 4. Invoke LLM
    response = await llm.ainvoke([
        ("system", formatted_prompt),
        ("user", f"Assessment: {state['assessment_logic']}")
    ])
    
    return {"current_plan": response.content}