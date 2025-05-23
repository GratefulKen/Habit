
import streamlit as st
import json
import os
from datetime import datetime, date
import pandas as pd
import matplotlib.pyplot as plt

# ---------- File Handling ----------
DATA_FILE = "habits.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- App Layout ----------
st.title("🌱 Daily Habit Tracker")
st.sidebar.header("📋 Add / Manage Habits")

habits_data = load_data()
today = str(date.today())

# ---------- Add Habits ----------
new_habit = st.sidebar.text_input("Add a new habit:")
if st.sidebar.button("➕ Add Habit"):
    for habit in habits_data:
        if habit.lower() == new_habit.lower():
            st.sidebar.warning("Habit already exists.")
            break
    else:
        habits_data[new_habit] = {}
        save_data(habits_data)
        st.experimental_rerun()

# ---------- Show & Check Habits ----------
if not habits_data:
    st.info("Add some habits to get started.")
else:
    st.subheader(f"✅ Today's Habits: {today}")
    for habit in habits_data:
        checked = habits_data[habit].get(today, False)
        updated = st.checkbox(habit, value=checked)
        habits_data[habit][today] = updated
    save_data(habits_data)

# ---------- Weekly Overview ----------
st.subheader("📈 Weekly Progress")

dates = pd.date_range(end=date.today(), periods=7).strftime("%Y-%m-%d").tolist()
chart_data = {habit: [habits_data[habit].get(d, 0) for d in dates] for habit in habits_data}
df = pd.DataFrame(chart_data, index=dates)

st.dataframe(df)

st.line_chart(df)

# ---------- Reset ----------
if st.sidebar.button("🗑️ Reset All Data"):
    os.remove(DATA_FILE)
    st.experimental_rerun()
