import streamlit as st
import requests
from modules.nav import SideBarLinks

API_BASE = "http://web-api-test:4000"
organizer_id = st.session_state.get("organizer_id")

SideBarLinks()
st.title("📝 Review a Sponsor")

if not organizer_id:
    st.error("You must be logged in as an organizer to submit a review.")
    st.stop()

# Load sponsor options
try:
    response = requests.get(f"{API_BASE}/sponsor")
    response.raise_for_status()
    sponsors = response.json()
    sponsor_options = {s["name"]: s["sponsor_id"] for s in sponsors}
except Exception as e:
    st.error(f"Error fetching sponsors: {e}")
    st.stop()

# Review form
sponsor_name = st.selectbox("Select a Sponsor", options=sponsor_options.keys())
sponsor_id = sponsor_options[sponsor_name]

rating = st.radio("Rating", ["1", "2", "3", "4", "5"], horizontal=True)
comments = st.text_area("Optional Comments")

if st.button("Submit Review"):
    try:
        payload = {
            "rating": rating,
            "comments": comments
        }
        review_url = f"{API_BASE}/organizer/{organizer_id}/review/sponsor/{sponsor_id}"
        res = requests.post(review_url, json=payload)

        if res.status_code == 200:
            st.success(f"✅ Your review for **{sponsor_name}** has been submitted!")
        else:
            st.error(f"❌ Failed to submit review: {res.text}")
    except Exception as e:
        st.error(f"⚠️ Error submitting review: {e}")
