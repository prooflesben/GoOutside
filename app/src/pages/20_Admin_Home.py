import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Make Announcement', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Admin_Announcement.py')
if st.button('Approve/Reject Events', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Admin_Approve_Event.py')
if st.button('View categories/Add new categories', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Admin_View_Category.py')
if st.button('Approve Reviews', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Admin_Approve_Review.py')

with st.expander("View Event Stats"):
    st.write("Select an Organizer to view their stats.")
    try:
        # Fetch organizer data from the backend
        response = requests.get("http://web-api:4000/organizer")
        if response.status_code == 200:
            organizers = response.json()
            organizer_names = {organizer['name']: organizer['organizer_id'] for organizer in organizers}

            # Dropdown to select an organizer
            selected_organizer_name = st.selectbox("Select an Organizer", options=list(organizer_names.keys()))

            # Submit button
            if st.button("View Stats"):

                logger.info(f"Viewing stats of organizer: {selected_organizer_name}")
                st.session_state['organizer_id'] = organizer_names[selected_organizer_name]
                st.switch_page('pages/Event_Stats_for_Admin.py')
        else:
            st.error("Failed to fetch organizers. Please try again later.")
            st.error("Error: " + response.text)
    except Exception as e:
        st.error(f"An error occurred while fetching organizers: {e}")
