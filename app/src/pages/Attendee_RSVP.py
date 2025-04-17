import logging
import os
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests


st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()
results = None


try:
    response = requests.get(f"http://web-api:4000/events")
    response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
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
    # Try to get unread message count
    unread_count = 0
    try:
        msg_response = requests.get(f"http://web-api:4000/admin/")
        if msg_response.status_code == 200:
            unread_count = msg_response.json().get('count', 0)
    except:
        pass
        
    inbox_label = "Inbox"
        
    if st.button(f"📬 {inbox_label}", 
                type='primary',
                use_container_width=True):
        st.switch_page('pages/05_Attendee_Inbox.py')


# Create a search bar
query = st.text_input("Search for events:")

def event_card(event):
    print("making event")
    with st.container():
        st.subheader(event["name"])
        st.caption(f"📅 {event['start_time']} — {event['end_time']}")
        st.write(f"📍 Location: {event['location']}")
        st.write(f"💸 Cost: ${event['cost']}")
        st.write(f"🏷️ Category: {event['category_name']}")
        st.write(f"🧑‍💼 Organized By: {event['organizer_name']}")
        if event['sponsor_by']:
            st.write(f"🤝 Sponsored By: {event['sponsor_name']}")
        # if event['approved_by']:
        #     st.write(f"✅ Approved By: {event['approved_by']}")

        st.markdown("---")
        st.write(f"**Event Details:**\n{event['description']}")
        st.markdown("-----")
        
# When the user types something, show results
if query:
    st.write(f"You searched for: **{query}**")

    # Example: Simulate search results
    dummy_results = ["apple", "banana", "cherry", "date"]
    filtered = [item for item in results if query.lower() in item['name'].lower()]

    if filtered:
        st.write("Results found:")
        for item in filtered:
            event_card(item)
    else:
        st.write("No results found.")
else:
    if results:
        for val in results:
            if val['approved_by'] is not None:
                event_card(val)