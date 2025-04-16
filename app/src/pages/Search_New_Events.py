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

if "query" not in st.session_state:
    st.session_state["query"] = ""

# Create a search bar
query = st.text_input("Search for events:", value=st.session_state["query"])
st.session_state["query"] = query

def event_card(event):
    with st.container():
        st.subheader(event["name"])
        st.caption(f"📅 {event['start_time']} — {event['end_time']}")
        st.write(f"📍 Location: {event['location']}")
        st.write(f"💸 Cost: ${event['cost']}")
        st.write(f"🏷️ Category: {event['category_name']}")
        st.write(f"🧑‍💼 Organized By: {event['organizer_name']}")
        if event['sponsor_by']:
            st.write(f"🤝 Sponsored By: {event['sponsor_name']}")
        st.write(f"**Event Details:**\n{event['description']}")

        # Check if the user has already RSVPed to the event
        attendee_id = st.session_state.get("attendee_id", 1)  # Replace with dynamic attendee ID
        try:
            rsvp_check_response = requests.get(f"http://web-api:4000/attendee/{attendee_id}/rsvps")
            rsvp_check_response.raise_for_status()
            rsvped_events = rsvp_check_response.json()
            rsvped_event_ids = [rsvp['event_id'] for rsvp in rsvped_events]

            if event['event_id'] in rsvped_event_ids:
                st.info(f"You have already RSVPed to {event['name']}.")
            else:
                # Add RSVP button
                if st.button(f"RSVP to {event['name']}", key=f"rsvp_{event['event_id']}"):
                    try:
                        response = requests.post(f"http://web-api:4000/attendee/{attendee_id}/rsvps/{event['event_id']}")
                        if response.status_code == 200:
                            st.success(f"You have successfully RSVPed to {event['name']}!")
                        else:
                            st.error(f"Failed to RSVP: {response.text}")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
        except Exception as e:
            st.error(f"Failed to check RSVP status: {e}")

        st.markdown("-----")

        
# When the user types something, show results
if query:
    st.write(f"You searched for: {query}")

    # Example: Simulate search results
    dummy_results = ["apple", "banana", "cherry", "date"]
    filtered = [item for item in results if query.lower() in item['name'].lower()]


    if filtered:
        st.write("Results found:")
        for item in filtered:
            event_card(item)

        if st.button("New Search"):
            st.session_state["query"] = ""
            st.switch_page('pages/Search_New_Events.py')
            st.rerun() 

    else:
        st.write("No results found.")
        
        if st.button("New Search"):
            st.session_state["query"] = ""
            st.switch_page('pages/Search_New_Events.py')
            st.rerun() 
else:
    if results:
        for val in results:
            if val['approved_by'] is not None:
                event_card(val)



    



  