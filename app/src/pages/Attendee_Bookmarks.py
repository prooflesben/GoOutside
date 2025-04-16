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
