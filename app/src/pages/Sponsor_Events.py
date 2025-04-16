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
    response = requests.get(f"http://web-api:4000/events/no-sponsor")
    response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
    results = response.json()

except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch events: {e}")



st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('')
st.write('')

# Add inbox button with notification count
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.write('### Choose an event to sponsor')
with col2:
    # Add popularity sort toggle
    sort_by_popularity = st.toggle("Sort by Popularity", value=False)
    if sort_by_popularity:
        sort_direction = st.radio("Sort Direction", ["Highest First", "Lowest First"], horizontal=True)

# Create a search bar
query = st.text_input("Search for events:")

# will display a given event card based on the event.
def event_card(event):
    with st.container():
        st.subheader(event["name"])
        st.caption(f"📅 {event['start_time']} — {event['end_time']}")
        st.write(f"📍 Location: {event['location']}")
        st.write(f"💸 Cost: ${event['cost']}")
        st.write(f"🏷️ Category: {event['category_name']}")
        st.write(f"🧑‍💼 Organized By: {event['organizer_name']}")
        
        # get the contact info
        try:
            contact_response = requests.get(f"http://web-api:4000/organizer/{event['organized_by']}/contact-info")
            if contact_response.status_code == 200:
                contact_info = contact_response.json()
                if contact_info:
                    st.write(f"📧 Contact Email: {contact_info[0]['email']}")
                    st.write(f"📞 Contact Phone: {contact_info[0]['phone']}")
        except Exception as e:
            st.error(f"Error fetching contact information: {e}")
            
        if event['sponsor_by']:
            st.write(f"🤝 Sponsored By: {event['sponsor_name']}")
        else:
            st.write("🤝 Sponsored By: None")
            # Add buttons for sponsoring and viewing stats
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"Sponsor this event", key=f"sponsor_{event['event_id']}"):
                    sponsor_id = st.session_state.get("sponsor_id")
                    sponsor_id = 1
                    if sponsor_id:
                        try:
                            # Call the API to sponsor the event
                            response = requests.put(
                                f"http://web-api:4000/sponsor/{sponsor_id}/events/{event['event_id']}"
                            )
                            if response.status_code == 200:
                                st.success(f"You have successfully sponsored the event: {event['name']}")
                            else:
                                st.error(f"Failed to sponsor the event: {response.text}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"An error occurred: {e}")
                    else:
                        st.error("You must be logged in as a sponsor to sponsor an event.")
            with col2:
                if st.button(f"See Event Stats", key=f"stats_{event['event_id']}"):
                    st.session_state['organizer_id'] = event['organized_by']
                    st.session_state['event_id'] = event['event_id']
                    st.switch_page('pages/organizer_reviews.py')

        st.markdown("---")
        st.write(f"**Event Details:**\n{event['description']}")
        st.markdown("-----")

# When the user types something, show results
if query:
    st.write(f"You searched for: **{query}**")

    filtered = [item for item in results if query.lower() in item['name'].lower()]

    if filtered:
        st.write("Results found:")
        for item in filtered:
            event_card(item)
    else:
        st.write("No results found.")
else:
    if results:
        # Sort results if popularity sort is enabled
        if sort_by_popularity:
            # Get popularity data for each event
            for event in results:
                # NOTE: error handling will just set the stats to 0
                try:
                    stats_response = requests.get(f"http://web-api:4000/events/{event['event_id']}/stats/popularity")
                    if stats_response.status_code == 200:
                        stats = stats_response.json()
                        event['bookmarks'] = stats.get('bookmarks', 0)
                    else:
                        event['bookmarks'] = 0
                except:
                    event['bookmarks'] = 0
                    
                try:
                    attendance_response = requests.get(f"http://web-api:4000/events/{event['event_id']}/attendance")
                    if attendance_response.status_code == 200:
                        attendance = attendance_response.json()
                        event['rsvps'] = len(attendance)
                    else:
                        event['rsvps'] = 0
                except:
                    event['rsvps'] = 0
                
                # will sort based off this
                event['total_engagement'] = event['bookmarks'] + event['rsvps']
            
            # Sort by total engagement, either highest or lowest
            results.sort(key=lambda x: x['total_engagement'], reverse=(sort_direction == "Highest First"))
            
        for val in results:
            if val['approved_by'] is not None:
                event_card(val)
