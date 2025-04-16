import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Create Event", layout="centered")
st.title("📅 Create a New Event")

# Organizer making the request
organized_by = 1
sponsor_by = 1
approved_by = 1

# Flask endpoint
CREATE_EVENT_URL = f"http://web-api:4000/organizer/{organized_by}/events"

# 🔄 Fetch event categories from backend
category_name = None
try:
    res = requests.get("http://web-api:4000/event_categories/")
    if res.status_code == 200:
        categories_data = res.json()
        category_list = [cat["name"] for cat in categories_data]
        if category_list:
            category_name = st.selectbox("Event Category", category_list)
        else:
            st.warning("No event categories available.")
    else:
        st.error("Failed to fetch event categories.")
except Exception as e:
    st.error(f"Error loading categories: {e}")

# Event form
with st.form("event_form"):
    name = st.text_input("Event Name")
    cost = st.number_input("Cost ($)", min_value=0.0, step=0.01)
    start_date = st.date_input("Start Date", min_value=datetime.today())
    start_time = st.time_input("Start Time")
    end_date = st.date_input("End Date", min_value=start_date)
    end_time = st.time_input("End Time")
    location = st.text_input("Location")
    description = st.text_area("Description")
    sponsor_cost = st.text_input("Sponsor Cost (optional)")

    submitted = st.form_submit_button("Create Event")

    if submitted:
        start_dt = datetime.combine(start_date, start_time).isoformat()
        end_dt = datetime.combine(end_date, end_time).isoformat()

        if not name or not location or not description or not category_name:
            st.error("Please fill in all required fields.")
        elif end_dt <= start_dt:
            st.error("End time must be after start time.")
        else:
            payload = {
                "name": name,
                "cost": cost,
                "start_time": start_dt,
                "end_time": end_dt,
                "location": location,
                "description": description,
                "category_name": category_name,
                "sponsor_by": int(sponsor_by) if sponsor_by else None,
                "approved_by": int(approved_by) if approved_by else None,
                "sponsor_cost": int(sponsor_cost) if sponsor_cost else None,
            }

            try:
                with st.spinner("Submitting event..."):
                    res = requests.post(CREATE_EVENT_URL, json=payload)
                    if res.status_code == 201:
                        st.success("✅ Event created successfully!")
                    else:
                        st.error(f"❌ Failed: {res.text}")
            except Exception as e:
                st.error(f"Error: {e}")
