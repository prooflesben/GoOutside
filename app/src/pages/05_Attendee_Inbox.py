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
    response = requests.get(f"http://web-api-test:4000/admin/")
    response.raise_for_status()
    messages = response.json()
    
    if not messages:
        st.info("No messages found. Your inbox is empty.")
    else:
        # Display messages
        for message in messages:
            with st.container():
                st.subheader(message.get("subject", "No Subject"))
                st.caption(f"From: {message.get('sender_name', 'Unknown')} • {message.get('date', 'No date')}")
                st.write(message.get("content", "No content"))
                st.markdown("---")
    

except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch messages: {e}")
    st.info("If the message service is not yet available, this is expected.")

# Add a back button to return to the home page
if st.button("Return to Home"):
    st.switch_page("pages/00_Attendee_Home.py")