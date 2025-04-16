import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Submit Organizer Review")

# Sample organizer mapping
attendee_id = st.session_state.get('attendee_id', 1)  # Fetch organizers from the backend
organizers = []
organizer_map = {}  # Hash map to store organizer name to organizer id mapping
try:
    response = requests.get(f"http://web-api-test:4000/attendee/{attendee_id}/organizers")
    if response.status_code == 200:
        organizers_data = response.json()
        if organizers_data:
            organizers = [organizer['name'] for organizer in organizers_data]
            organizer_map = {organizer['name']: organizer['organizer_id'] for organizer in organizers_data}
        else:
            st.warning("No organizers available for review.")
            st.stop()
    else:
        st.error("Failed to fetch organizers. Please try again later.")

except Exception as e:
    st.error(f"An error occurred while fetching organizers: {e}")
    st.stop()

# Form inputs
rating = st.selectbox("Rating (1-5)", options=["1", "2", "3", "4", "5"])
comments = st.text_area("Comments (optional)")
being_reviewed = st.selectbox("Select Organizer", options=["Select an organizer"] + organizers, index=0)

# Submit logic
if st.button("Submit Review"):
    data = {
        "rating": rating,
        "comments": comments
    }

    organizer_id = organizer_map[being_reviewed] if being_reviewed != "Select an organizer" else None
    if not organizer_id:
        st.error("Please select a valid organizer.")
        st.stop()
    url = f"http://web-api-test:4000/attendee/{attendee_id}/review/organizer/{organizer_id}"

    response = requests.post(url, json=data)

    if response.status_code == 200:
        st.success("Review submitted successfully!")
        # Switch to 00_Attendee_Home.py
        #wait for 2 seconds before switching

    else:
        st.error("Error submitting review. Please try again.")