import logging
import os
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title("Message Inbox")
st.write("View your messages here.")

attendee_id = st.session_state.get('attendee_id', 1)

# Get messages for attendee
try:    
    event_announcments = requests.get(f"http://web-api:4000/attendee/{attendee_id}/event_announcments")
    event_announcments.raise_for_status()
    event_messages = event_announcments.json()
    if event_announcments:
        for message in event_messages:
            st.subheader(message['event_name'])
            st.write(f"**Event Time:** {message['start_time']} - {message['end_time']}")
            st.write(f"**Location:** {message['location']}")
            st.write(f"**Message:** {message['description']}")
            st.write("---")
    else:
        st.info("No messages available.")

    admin_announcments = requests.get(f"http://web-api:4000/attendee/{attendee_id}/admin_announcments")
    admin_announcments.raise_for_status()
    admin_messages = admin_announcments.json()
    if admin_announcments:
        for message in admin_messages:
            st.subheader(message['event_name'])
            st.write(f"**Event Time:** {message['start_time']} - {message['end_time']}")
            st.write(f"**Location:** {message['location']}")
            st.write(f"**Message:** {message['description']}")
            st.write("---")
    else:
        st.info("No admin announcements available.")
    

except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch messages: {e}")
    st.info("If the message service is not yet available, this is expected.")

# Add a back button to return to the home page
if st.button("Return to Home"):
    st.switch_page("pages/00_Attendee_Home.py")