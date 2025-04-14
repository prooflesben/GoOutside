import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')


# Create a search bar
query = st.text_input("Search for events:")

# When the user types something, show results
if query:
    st.write(f"You searched for: **{query}**")

    # Example: Simulate search results
    dummy_results = ["apple", "banana", "cherry", "date"]
    filtered = [item for item in dummy_results if query.lower() in item.lower()]

    if filtered:
        st.write("Results found:")
        for item in filtered:
            st.write(f"✅ {item}")
    else:
        st.write("No results found.")


if st.button('View World Bank Data Visualization', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_World_Bank_Viz.py')

if st.button('View World Map Demo', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Map_Demo.py')
  
  