import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

if st.button("Search for new Events", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Entering Chat Room")
    st.switch_page('pages/Search_Events.py')

if st.button("Bookmarked Events", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Checking Bookmarked events")
    st.switch_page('Home.py')
