import logging
import os
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

backend_url = "http://localhost:4000"


st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()
results = None


try:
    response = requests.get(f"http://web-api:4000/events")
    response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
    results = response.json()

    # Example display
    for event in results:
        st.write(event)

except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch events: {e}")



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
        
def event_card(event):
    print("making event")
    with st.container():
        st.subheader(event["name"])
        st.caption(f"📅 {event['start_time']} — {event['end_time']}")
        st.write(f"📍 Location: {event['location']}")
        st.write(f"💸 Cost: ${event['cost']}")
        st.write(f"🏷️ Category: {event['category_name']}")
        st.write(f"🧑‍💼 Organized By: {event['organized_by']}")
        if event['sponsor_by']:
            st.write(f"🤝 Sponsored By: {event['sponsor_by']}")
        # if event['approved_by']:
        #     st.write(f"✅ Approved By: {event['approved_by']}")

        st.markdown("---")
        st.write(f"**Event Details:**\n{event['description']}")
        st.markdown("-----")

# Example dictionary, could come from MySQL or another source
sample_event = {
    "event_id": 1,
    "name": "Community Tech Expo",
    "cost": 15.00,
    "start_time": "2025-05-10 09:00:00",
    "end_time": "2025-05-10 17:00:00",
    "location": "Downtown Innovation Center",
    "description": "A day full of networking, tech demos, and talks from industry experts.",
    "category_name": "Technology",
    "organized_by": 101,
    "sponsor_by": 501,
    "approved_by": 301,
    "sponsor_cost": 5000
}

# Show the event card in the Streamlit app
event_card(sample_event)
if results:
    for val in results:
        if val['approved_by'] is not None:
            event_card(val)





if st.button('View World Bank Data Visualization', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_World_Bank_Viz.py')

if st.button('View World Map Demo', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Map_Demo.py')
  
  