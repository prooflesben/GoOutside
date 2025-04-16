import streamlit as st
import requests
from modules.nav import SideBarLinks

API_BASE = "http://web-api-test:4000" 
ATTENDEE_ID = st.session_state.get("attendee_id")
if not ATTENDEE_ID:
    st.error("Please log in as an attendee to view bookmarks.")
    st.stop()

SideBarLinks()

st.title("🔖 My Bookmarked Events")

# Load bookmarks
@st.cache_data(show_spinner=False)
def load_bookmarks():
    try:
        r = requests.get(f"{API_BASE}/attendee/{ATTENDEE_ID}/bookmarks", timeout=5)
        if r.status_code == 200:
            return r.json()
        else:
            st.error(f"Failed to fetch bookmarks: {r.status_code}")
            return []
    except Exception as e:
        st.error(f"Request failed: {e}")
        return []

# Refresh
def reload():
    st.cache_data.clear()
    st.rerun()

# Display bookmarks
bookmarks = load_bookmarks()

if not bookmarks:
    st.info("No bookmarks found.")
    st.write(f"for attendee ID: {ATTENDEE_ID}")
    st.stop()

for event in bookmarks:
    event_id = event["event_id"]
    name = event.get("name", "Unnamed Event")
    location = event.get("location", "Unknown")
    time = event.get("start_time", "Unknown")

    with st.container():
        st.subheader(name)
        st.markdown(f"📍 **Location:** {location}")
        st.markdown(f"🕒 **Start Time:** {time}")

        if st.button("🗑️ Remove Bookmark", key=f"remove_{event_id}"):
            try:
                r = requests.delete(f"{API_BASE}/attendee/{ATTENDEE_ID}/bookmarks/{event_id}")
                if r.status_code == 200:
                    st.success(f"Removed bookmark for: {name}")
                    reload()
                else:
                    st.error(f"Failed to delete bookmark ({r.status_code})")
            except Exception as e:
                st.error(f"Error removing bookmark: {e}")
        
        st.divider()
