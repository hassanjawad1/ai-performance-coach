import os
from fastapi import FastAPI, Form, Request
from dotenv import load_dotenv

load_dotenv()

from app.graph.builder import create_coach_graph
from app.services.whatsapp import send_whatsapp
from app.services.database import init_db
from app.services.database import init_db,get_user_stats,log_plan_to_history

app = FastAPI()
coach_bot = create_coach_graph()
init_db()

@app.post("/webhook")
async def whatsapp_webhook(From: str = Form(...), Body: str = Form(...)):
    # Thread ID ensures memory is unique to each user's phone number
    config = {"configurable": {"thread_id": From}}
    

    user_id = From.replace("whatsapp:", "").replace("+", "")
    current_streak = get_user_stats(user_id) 

    initial_state = {
        "messages": [("user", Body)],
        "streak": current_streak, # Now it's dynamic!
        "user_id": user_id
    }

    result = await coach_bot.ainvoke(
        initial_state, 
        config=config
    )
    plan_to_save = result.get('current_plan')

    log_plan_to_history(user_id, plan_to_save)

    # Final Output Construction
    final_msg = f"✨ *Daily Plan*\n\n{result['current_plan']}\n\n🧠 *Coach's Note:*\n{result['assessment_logic']}"
    
    if len(final_msg) > 1550:
        final_msg = final_msg[:1550] + "...\n(Message truncated due to length)" 
    # Send back to WhatsApp
    send_whatsapp(From, final_msg)
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)