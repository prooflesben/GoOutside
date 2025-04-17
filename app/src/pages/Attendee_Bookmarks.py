import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests

# Initialize sidebar
SideBarLinks()

# Set up logging
logger = logging.getLogger(__name__)

# Page title
st.title("🔖 My Bookmarked Events")

# Get attendee ID from session state
attendee_id = st.session_state.get('attendee_id', 1)

if attendee_id:
    try:
        with st.spinner("Fetching your bookmarked events..."):
            response = requests.get(f"http://web-api:4000/attendee/{attendee_id}/bookmarks")

        if response.status_code == 200:
            events = response.json()

            if events:
                st.success("Here are your bookmarked events:")
                for event in events:
                    st.write(f"**Event Name:** {event['name']}")
                    st.write(f"**Start Time:** {event['start_time']}")
                    st.write(f"**Location:** {event['location']}")

                    # Check if the user has already RSVPed to the event
                    attendee_id = st.session_state.get("attendee_id", 1)
                    try:
                        rsvp_check_response = requests.get(f"http://web-api:4000/attendee/{attendee_id}/rsvps")
                        rsvp_check_response.raise_for_status()
                        rsvped_events = rsvp_check_response.json()
                        rsvped_event_ids = [rsvp['event_id'] for rsvp in rsvped_events]

                        if event['event_id'] in rsvped_event_ids:
                            st.info(f"You have already RSVPed to {event['name']}.")
                        else:
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

                    if st.button(f"🗑️ Remove Bookmark for {event['name']}", key=f"remove_{event['event_id']}"):
                        try:
                            delete_response = requests.delete(
                                f"http://web-api:4000/attendee/{attendee_id}/bookmarks/{event['event_id']}"
                            )
                            if delete_response.status_code == 200:
                                st.success(f"Bookmark removed for: {event['name']}")
                                st.rerun()
                            else:
                                st.error(f"Failed to remove bookmark: {delete_response.text}")
                        except Exception as e:
                            logger.error(f"Error removing bookmark: {e}")
                            st.error("An error occurred while removing the bookmark.")

                    st.write("---")
            else:
                st.info("You have not bookmarked any events.")
        else:
            st.error(f"Failed to fetch bookmarks: {response.text}")
    except Exception as e:
        logger.error(f"Error fetching bookmarks: {e}")
        st.error("An error occurred while fetching your bookmarked events.")
