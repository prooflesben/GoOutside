import logging
logger = logging.getLogger(__name__)
import requests

import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

organizer_id = st.session_state.get('organizer_id', 1)

if st.button("Enter Chat Room", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Entering Chat Room")
    st.switch_page('pages/Chat_Room.py')

if st.button("Create a new event", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Search for Events")
    st.switch_page('pages/Create_Event.py')
    
if st.button("Promote an event", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Promote Event")
    st.switch_page('pages/Promote_Event.py')

if st.button("Send an Event Announcement", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Send Event Announcement")
    st.switch_page('pages/Event_Update.py')

with st.expander("View Event Stats"):
    st.write("Select an Event to view stats.")
    try:
        # Fetch organizer data from the backend
        response = requests.get(f"http://web-api:4000/organizer/{organizer_id}/events")
        if response.status_code == 200:
            events = response.json()
            event_names = {event['name']: event['event_id'] for event in events}

            # Dropdown to select an organizer
            selected_event_name = st.selectbox("Select an Event", options=list(event_names.keys()))

            # Submit button
            if st.button("View Stats"):
                logger.info(f"Viewing stats of event: {selected_event_name}")
                st.session_state['organizer_id'] = organizer_id
                st.session_state['event_id'] = event_names[selected_event_name]
                st.switch_page('pages/Organizer_Reviews.py')
        else:
            st.error("Failed to fetch organizers. Please try again later.")
            st.error("Error: " + response.text)
    except Exception as e:
        st.error(f"An error occurred while fetching organizers: {e}")
        
        

