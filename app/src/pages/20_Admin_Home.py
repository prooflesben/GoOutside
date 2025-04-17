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
  st.switch_page('pages/Organizer_Flag_Reviews.py')
if st.button('View Event Stats', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_ML_Model_Mgmt.py')