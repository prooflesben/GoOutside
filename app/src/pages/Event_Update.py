import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
from modules.nav import SideBarLinks



# Set page configuration
st.set_page_config(page_title="Organizer Event Announcements", layout="wide")

SideBarLinks()

# Page title and description
st.title("Create Event Announcement")
st.markdown("Use this form to create a new announcement for an event.")

def get_events_from_api():
    try:
        response = requests.get(f"http://web-api-test:4000/organizer/{st.session_state['organizer_id']}/events")
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)  # Ensure it's a DataFrame
    except Exception as e:
        st.error(f"Failed to fetch categories: {e}")
        return pd.DataFrame()  # Return empty DataFrame to prevent crashes

# Function to submit announcement to API
def submit_announcement(event_id, description):
    # Prepare data for API
    data = {
        "event_id": event_id,
        "description": description
    }
    response = requests.post("http://web-api-test:4000/organizer/announcement", json=data, headers={"Content-Type": "application/json"})
    return response.status_code, response.json()

# Create form layout
with st.form(key="announcement_form"):
    # Event selection dropdown
    events = get_events_from_api()
    event_options = {event["name"]: event["event_id"] for event in events.to_dict(orient="records")}
    selected_event = st.selectbox(
        "Select Event",
        options=list(event_options.keys()),
        index=0
    )
    
    # Description text area
    announcement_text = st.text_area(
        "Announcement Description",
        height=200,
        placeholder="Enter the announcement details here..."
    )
    
    # Submit button
    submit_button = st.form_submit_button(label="Create Announcement")

# Handle form submission
if submit_button:
    if not announcement_text.strip():
        st.error("Please enter an announcement description.")
    else:
        event_id = event_options[selected_event]
        status_code, response = submit_announcement(event_id, announcement_text)
        
        if status_code == 200:
            st.success("✅ Announcement created successfully!")
        else:
            st.error(f"Error creating announcement: {response.get('message', 'Unknown error')}")

# Show a preview section
if announcement_text:
    st.subheader("Preview")
    preview_col1, preview_col2 = st.columns([1, 3])
    with preview_col1:
        st.markdown("**Event:**")
    with preview_col2:
        st.markdown(selected_event)
    
    with preview_col1:
        st.markdown("**Description:**")
    with preview_col2:
        st.markdown(announcement_text)