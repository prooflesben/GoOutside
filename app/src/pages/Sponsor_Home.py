import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

if st.button("Enter Chat Room", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Entering Chat Room")
    st.switch_page('pages/Chat_Room.py')

if st.button("Enter Chat Room (empty for now)", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Search for Events")
    st.switch_page('Home.py')
