import streamlit as st
import requests
import pandas as pd
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="AI Performance Coach", page_icon="⚡", layout="wide")
API_URL = "http://localhost:8000/webhook"
DB_PATH = "coach_memory.db"

# --- HELPER: FETCH DATA FOR DASHBOARD ---
def get_dashboard_data():
    conn = sqlite3.connect(DB_PATH)
    # Get current streak
    streak = pd.read_sql_query("SELECT streak FROM users LIMIT 1", conn)
    # Get history for the chart
    history = pd.read_sql_query("SELECT date, id FROM history ORDER BY date ASC", conn)
    conn.close()
    return streak, history

# --- SIDEBAR: USER STATS ---
with st.sidebar:
    st.title("🏃 User Profile")
    streak_df, history_df = get_dashboard_data()
    
    current_streak = streak_df.iloc[0]['streak'] if not streak_df.empty else 0
    st.metric(label="Current Streak", value=f"{current_streak} Days", delta="🔥")
    
    st.write("---")
    st.write("### Consistency Tracker")
    if not history_df.empty:
        # Simple bar chart of activity counts per date
        chart_data = history_df.groupby('date').count()
        st.bar_chart(chart_data)

# --- MAIN UI: CHAT INTERFACE ---
st.title("⚡ AI Performance Coach")
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How are you feeling today? (e.g., Tech: I'm at fatigue 5)"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call your FastAPI Backend
    with st.spinner("Analyzing CNS readiness..."):
        try:
            payload = {"From": "whatsapp:+923173237613", "Body": prompt}
            response = requests.post(API_URL, data=payload)
            
            if response.status_code == 200:
                # In a real app, you'd return the plan in the JSON response
                # For now, we'll simulate the AI's "thought" process
                full_response = "✅ Plan generated! Check your terminal or history."
                
                with st.chat_message("assistant"):
                    st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("Backend Error. Is FastAPI running?")
        except Exception as e:
            st.error(f"Connection failed: {e}")