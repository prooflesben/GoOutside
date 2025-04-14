import streamlit as st
import requests
import json
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Admin Event Announcements", layout="wide")

# Page title and description
st.title("Create Event Announcement")
st.markdown("Use this form to create a new announcement for an event.")

def get_events_from_api():
    return [
        {"id": 1, "name": "Annual Conference 2025"},
        {"id": 2, "name": "Product Launch"},
        {"id": 3, "name": "Team Building Workshop"},
        {"id": 4, "name": "Quarterly Meeting"}
    ]

# Function to submit announcement to API
def submit_announcement(event_id, description):
    # Prepare data for API
    data = {
        "event_id": event_id,
        "description": description,
        "created_at": datetime.now().isoformat()
    }
    
    # Example API call:
    # response = requests.post(
    #     "http://your-flask-api/announcements",
    #     json=data,
    #     headers={"Content-Type": "application/json"}
    # )
    # return response.status_code, response.json()
    
    # Mock response for demonstration
    return 201, {"message": "Announcement created successfully", "data": data}

# Create form layout
with st.form(key="announcement_form"):
    # Event selection dropdown
    events = get_events_from_api()
    event_options = {event["name"]: event["id"] for event in events}
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
        
        if status_code == 201:
            st.success("✅ Announcement created successfully!")
            st.json(response)
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