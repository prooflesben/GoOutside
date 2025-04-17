import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests

# Initialize the sidebar navigation
SideBarLinks()

# Set up logging
logger = logging.getLogger(__name__)

# Page title
st.title("🌟 Recommended Events")

# Attendee ID (replace with dynamic user ID if available)
attendee_id = st.session_state.get("attendee_id", 1)

if attendee_id:
    try:
        # Fetch recommended events from the backend
        with st.spinner("Fetching recommended events..."):
            response = requests.get(f"http://web-api:4000/attendee/{attendee_id}/recommendations")
            response.raise_for_status()
            recommended_events = response.json()

        if recommended_events:
            st.success("Here are your recommended events:")
            for event in recommended_events:
                with st.container():
                    st.subheader(event["event_name"])
                    st.caption(f"📅 {event['start_time']} — {event['end_time']}")
                    st.write(f"📍 Location: {event['location']}")
                    st.write(f"💸 Cost: ${event['cost']}")
                    st.write(f"📝 Description: {event['description']}")

                    # Check if the user has already RSVPed to the event
                    attendee_id = st.session_state.get("attendee_id", 1)
                    try:
                        rsvp_check_response = requests.get(f"http://web-api:4000/attendee/{attendee_id}/rsvps")
                        rsvp_check_response.raise_for_status()
                        rsvped_events = rsvp_check_response.json()
                        rsvped_event_ids = [rsvp['event_id'] for rsvp in rsvped_events]

                        if event['event_id'] in rsvped_event_ids:
                            st.info(f"You have already RSVPed to {event['event_name']}.")
                        else:
                            if st.button(f"RSVP to {event['event_name']}", key=f"rsvp_{event['event_id']}"):
                                try:
                                    response = requests.post(f"http://web-api:4000/attendee/{attendee_id}/rsvps/{event['event_id']}")
                                    if response.status_code == 200:
                                        st.success(f"You have successfully RSVPed to {event['event_name']}!")
                                    else:
                                        st.error(f"Failed to RSVP: {response.text}")
                                except Exception as e:
                                    st.error(f"An error occurred: {e}")
                    except Exception as e:
                        st.error(f"Failed to check RSVP status: {e}")

                    # Check if the user has already bookmarked the event
                    try:
                        bookmark_check_response = requests.get(f"http://web-api:4000/attendee/{attendee_id}/bookmarks")
                        bookmark_check_response.raise_for_status()
                        bookmarked_events = bookmark_check_response.json()
                        bookmarked_event_ids = [b['event_id'] for b in bookmarked_events]

                        if event['event_id'] in bookmarked_event_ids:
                            st.info(f"You already bookmarked {event['event_name']}.")
                        else:
                            if st.button(f"🔖 Bookmark {event['event_name']}", key=f"bookmark_{event['event_id']}"):
                                try:
                                    response = requests.post(f"http://web-api:4000/attendee/{attendee_id}/bookmarks/{event['event_id']}")
                                    if response.status_code == 200:
                                        st.success(f"Bookmarked {event['event_name']}!")
                                        st.rerun()
                                    else:
                                        st.error(f"Failed to bookmark: {response.text}")
                                except Exception as e:
                                    st.error(f"An error occurred while bookmarking: {e}")
                    except Exception as e:
                        st.error(f"Failed to check bookmark status: {e}")
                    st.markdown("-----")

        else:
            st.info("No recommended events available at the moment.")
    except Exception as e:
        logger.error(f"Error fetching recommended events: {e}")
        st.error("An error occurred while fetching recommended events.")
else:
    st.warning("Please log in to view your recommended events.")