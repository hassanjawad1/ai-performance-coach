import sqlite3
from app.services.database import DB_PATH

def send_weekly_report(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get last 7 entries
    cursor.execute("SELECT date, plan FROM history WHERE user_id = ? ORDER BY date DESC LIMIT 7", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No history found for this user.")
        return

    summary = " *YOUR WEEKLY SUMMARY*\n\n"
    for date, plan in reversed(rows):
        # Taking just the first line of each plan to keep it short
        summary += f"• {date}: {plan.splitlines()[0] if plan else 'Active'}\n"
    
    summary += "\n🚀 *Keep going, Jawad!*"
    
    # Trigger this manually when you have 1 message left in Twilio!
    print(summary) 
    # send_whatsapp(f"whatsapp:+{user_id}", summary)

if __name__ == "__main__":
    send_weekly_report("923173237613")