import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')


if st.button("Enter Chat Room", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Entering Chat Room")
    st.switch_page('pages/Chat_Room.py')

if st.button("See Sponsor Stastistics", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Entering sponsosr statistics")
    st.switch_page('pages/Sponsor_Stats.py')

    
if st.button("Sponsor an Event", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Search for Events to Sposnor")
    st.switch_page('pages/Sponsor_Events.py')

