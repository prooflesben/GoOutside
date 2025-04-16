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

try:
    # Replace with your actual API endpoint for messages
    response = requests.get(f"http://web-api:4000/admin/announcements")
    response.raise_for_status()
    messages = response.json()
    
    if not messages:
        st.info("No messages found. Your inbox is empty.")
    else:
        # Display messages
        for message in messages:
            with st.container():
                st.subheader(f"**Event:** {message['event_name']}")
                st.write(f"**Event Time:** {message['event_time']}")
                st.write(f"**Message:** {message['message']}")
                st.write("---")
    

except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch messages: {e}")
    st.info("If the message service is not yet available, this is expected.")

# Add a back button to return to the home page
if st.button("Return to Home"):
    st.switch_page("pages/00_Attendee_Home.py")