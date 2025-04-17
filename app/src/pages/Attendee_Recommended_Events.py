import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests

# Initialize the sidebar navigation
SideBarLinks()

# Set up logging
logger = logging.getLogger(__name__)

# Page title
st.title("🌟 Recommended Events")

# Attendee ID (replace with dynamic user ID if available)
attendee_id = st.session_state.get("attendee_id", 1)

if attendee_id:
    try:
        # Fetch recommended events from the backend
        with st.spinner("Fetching recommended events..."):
            response = requests.get(f"http://web-api:4000/attendee/{attendee_id}/recommendations")
            response.raise_for_status()
            recommended_events = response.json()

        if recommended_events:
            st.success("Here are your recommended events:")
            for event in recommended_events:
                with st.container():
                    st.subheader(event["event_name"])
                    st.caption(f"📅 {event['start_time']} — {event['end_time']}")
                    st.write(f"📍 Location: {event['location']}")
                    st.write(f"💸 Cost: ${event['cost']}")
                    st.write(f"📝 Description: {event['description']}")
                    st.write("---")
        else:
            st.info("No recommended events available at the moment.")
    except Exception as e:
        logger.error(f"Error fetching recommended events: {e}")
        st.error("An error occurred while fetching recommended events.")
else:
    st.warning("Please log in to view your recommended events.")