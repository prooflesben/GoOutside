import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()
results = None

try:
    response = requests.get(f"http://web-api:4000/events")
    response.raise_for_status()
    results = response.json()

except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch events: {e}")

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('')
st.write('')

# Add inbox button with notification count
col1, col2 = st.columns([3, 1])
with col1:
    st.write('### What would you like to do today?')
with col2:
    try:
        msg_response = requests.get(f"http://web-api:4000/admin/")
    except:
        msg_response = None
        
    inbox_label = "Inbox"

    # button to open inbox
    if st.button(f"📬 {inbox_label}", 
                type='primary',
                use_container_width=True):
        st.switch_page('pages/05_Attendee_Inbox.py')

# button to search for events
if st.button("Search for new Events", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Entering Chat Room")
    st.switch_page('pages/Search_New_Events.py')

# button to see recommended events
if st.button("See Recommended Events", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Checking Recommended events")
    st.switch_page('pages/Attendee_Recommended_Events.py')

# button to view bookmarked events
if st.button("View Bookmarked Events", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Checking Bookmarked events")
    st.switch_page('pages/Attendee_Bookmarks.py')

# button to view RSVP'd events
if st.button("View RSVP'd Events", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Checking RSVP events")
    st.switch_page('pages/Attendee_Rsvps.py')

# button to review an event organizer
if st.button("Review an Event Organizer", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Review an Organizer")
    st.switch_page('pages/Review_Organizer.py')
