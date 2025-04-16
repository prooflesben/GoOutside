import streamlit as st
import requests

st.set_page_config(page_title="Organizer Reviews", layout="centered")
st.title("⭐ Organizer Reviews")

# Organizer ID (could be pulled from login session)
organizer_id = 1
BACKEND_URL = f"http://web-api:4000/organizer/{organizer_id}/reviews"

try:
    with st.spinner("Fetching reviews..."):
        response = requests.get(BACKEND_URL)

    if response.status_code == 200:
        reviews = response.json()
        if not reviews:
            st.info("No reviews available.")
        else:
            for review in reviews:
                st.markdown("---")
                st.subheader(f"⭐ Rating: {review['rating']}/5")
                st.write(f"**Reviewer:** {review['first_name']} {review['last_name']}")
                st.write(f"**Organizer:** {review['name']}")
                st.write(f"**Comment:** {review['comments']}")
    else:
        st.error(f"Failed to fetch reviews. Error: {response.text}")

except Exception as e:
    st.error(f"Error connecting to backend: {e}")
