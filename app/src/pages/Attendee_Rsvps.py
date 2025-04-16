import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests

# Initialize the sidebar navigation
SideBarLinks()

# Set up logging
logger = logging.getLogger(__name__)

# Page title
st.title("📋 RSVPd Events")

# Attendee ID (replace with dynamic user ID if available)
attendee_id = st.session_state.get('attendee_id', 1)

if attendee_id:
    try:
        # Fetch RSVPd events from the backend
        with st.spinner("Fetching your RSVPd events..."):
            response = requests.get(f"http://web-api:4000/attendee/{attendee_id}/rsvps")
        
        if response.status_code == 200:
            events = response.json()
            
            if events:
                st.success("Here are your RSVPd events:")
                for event in events:
                    st.write(f"**Event Name:** {event['name']}")
                    st.write(f"**Start Time:** {event['start_time']}")
                    st.write(f"**Location:** {event['location']}")
                    
                    # Add a delete button for each event
                    if st.button(f"Un-RSVP for {event['name']}", key=event['event_id']):
                        try:
                            delete_response = requests.delete(f"http://web-api:4000/attendee/{attendee_id}/rsvp/{event['event_id']}")
                            if delete_response.status_code == 200:
                                st.success(f"RSVP for {event['name']} deleted successfully!")
                                st.rerun()
                            else:
                                st.error(f"Failed to delete RSVP: {delete_response.text}")
                        except Exception as e:
                            logger.error(f"Error deleting RSVP: {e}")
                            st.error("An error occurred while deleting the RSVP.")
                    
                    st.write("---")
            else:
                st.info("You have not RSVPd to any events.")
        else:
            st.error(f"Failed to fetch RSVPd events: {response.text}")
    except Exception as e:
        logger.error(f"Error fetching RSVPd events: {e}")
        st.error("An error occurred while fetching your RSVPd events.")