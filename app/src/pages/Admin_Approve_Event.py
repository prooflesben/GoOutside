# pages/admin_event_moderation.py
import streamlit as st
import requests
from modules.nav import SideBarLinks

API_BASE = "http://web-api:4000"
ADMIN_ID = 1  # Hardcoded admin ID

SideBarLinks()

st.title("🗂️ Moderation – Pending Events")

# Load events
@st.cache_data(show_spinner=False)
def load_pending_events():
    try:
        r = requests.get(f"{API_BASE}/events/not-approved", timeout=5)
        if r.status_code == 200:
            return r.json()
        else:
            st.error(f"API error {r.status_code}: {r.text}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return []

def reload():
    st.cache_data.clear()
    st.rerun()

events = load_pending_events()

if not events:
    st.success("✅ No events to review!")
    st.stop()

# Display each event vertically
for event in events:
    event_id = event["event_id"]
    name = event.get("name", "Unnamed Event")
    location = event.get("location", "Unknown location")
    start_time = event.get("start_time", "Unknown time")
    description = event.get("description", "")

    with st.container():
        st.subheader(name)
        st.markdown(f"📍 **Location:** {location}")
        st.markdown(f"⏰ **Start:** {start_time}")
        st.markdown(f"📝 **Description:** {description}")
        
        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"✅ Approve", key=f"approve_{event_id}"):
                resp = requests.put(f"{API_BASE}/admin/{ADMIN_ID}/event/{event_id}")
                if resp.status_code == 200:
                    st.success(f"Approved: {name}")
                    reload()
                else:
                    st.error(f"Failed to approve ({resp.status_code})")

        with col2:
            if st.button(f"🗑️ Delete", key=f"delete_{event_id}"):
                resp = requests.delete(f"{API_BASE}/admin/{ADMIN_ID}/event/{event_id}")
                if resp.status_code == 200:
                    st.warning(f"Deleted: {name}")
                    reload()
                else:
                    st.error(f"Failed to delete ({resp.status_code})")

        st.divider()
