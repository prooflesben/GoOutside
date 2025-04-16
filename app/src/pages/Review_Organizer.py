import streamlit as st
import requests

st.title("Submit Organizer Review")

# Hardcoded values
WRITTEN_BY = 1

# Sample organizer mapping
organizers = {
    "EventHub Org": 1,
    "PartyMasters": 2,
}

# Form inputs
rating = st.selectbox("Rating (1-5)", options=["1", "2", "3", "4", "5"])
comments = st.text_area("Comments (optional)")
being_reviewed = st.selectbox("Select Organizer", options=organizers.keys())


# Submit logic
if st.button("Submit Review"):
    data = {
        "rating": rating,
        "comments": comments
    }

    # Only include flagged_by if the box is checked
   

    organizer_id = organizers[being_reviewed]
    url = f"http://web-api:4000/attendee/{WRITTEN_BY}/review/organizer/{organizer_id}"

    response = requests.post(url, json=data)

    if response.status_code == 200:
        st.success("Review submitted successfully!")
    else:
        st.error("Error submitting review. Please try again.")
