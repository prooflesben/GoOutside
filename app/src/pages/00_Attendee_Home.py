import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

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
        
        # Add button to add event to calendar
        if st.button(f"Copy '{event['name']}'", key=f"add_to_calendar_{event['event_id']}"):
            event_info = (
            f"Event: {event['name']}\n\n"
            f"Date: {event['start_time']} — {event['end_time']}\n\n"
            f"Location: {event['location']}\n\n"
            f"Cost: ${event['cost']}\n\n"
            f"Organizer: {event['organizer_name']}\n\n"
            f"Details: {event['description']}\n\n"
            )
            
            # Copy to clipboard using Streamlit's JavaScript integration
            st.code(event_info, language="text")
            st.markdown(
            f"""
            <script>
            navigator.clipboard.writeText({repr(event_info)});
            </script>
            """,
            unsafe_allow_html=True,
            )
            st.success("Event details copied to clipboard!")

            # add close button to close the copied message
            st.button("Close", key=f"close_{event['event_id']}")
            
        st.markdown("-----")
        
# When the user types something, show results
if query:
    st.write(f"You searched for: **{query}**")

    # Example: Simulate search results
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


if st.button("Search for new Events", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Entering Chat Room")
    st.switch_page('pages/Search_New_Events.py')

if st.button("Bookmarked Events", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Checking Bookmarked events")
    st.switch_page('Home.py')
