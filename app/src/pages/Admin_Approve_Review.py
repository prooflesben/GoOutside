import streamlit as st
import requests

st.set_page_config(page_title="Admin Reviews", layout="wide")
BASE_URL = "http://web-api:4000"

st.title("🔧 Admin Panel: Manage Sponsor Reviews")

# -------------------
# Helpers for Sponsors
# -------------------
@st.cache_data
def fetch_sponsors():
    try:
        res = requests.get(f"{BASE_URL}/sponsor")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching sponsors: {e}")
        return []

def fetch_sponsor_reviews(sponsor_id):
    try:
        res = requests.get(f"{BASE_URL}/sponsor/{sponsor_id}/reviews")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching sponsor reviews: {e}")
        return []

def flag_sponsor_review(sponsor_review_id):
    admin_id = st.session_state.get("admin_id", 1)
    try:
        res = requests.put(
            f"{BASE_URL}/admin/sponsor-reviews",
            json={"admin_id": admin_id, "sponsor_review_id": sponsor_review_id}
        )
        return res.status_code == 200
    except Exception as e:
        st.error(f"Failed to flag review: {e}")
        return False

def delete_sponsor_review(sponsor_review_id):
    try:
        res = requests.delete(
            f"{BASE_URL}/admin/sponsor-reviews",
            json={"sponsor_review_id": sponsor_review_id}
        )
        return res.status_code == 200
    except Exception as e:
        st.error(f"Failed to delete review: {e}")
        return False

# -------------------
# UI: Sponsors Only
# -------------------
sponsors = fetch_sponsors()
if not sponsors:
    st.warning(f"No sponsors found—check that {BASE_URL}/sponsor is up.")
    st.stop()

# Build mapping and dropdown
sponsor_map = {s["name"].strip(): s["sponsor_id"] for s in sponsors}
selected_name = st.selectbox("Select Sponsor", list(sponsor_map.keys()))
sponsor_id = sponsor_map.get(selected_name)

st.subheader(f"📄 Reviews for {selected_name}")
reviews = fetch_sponsor_reviews(sponsor_id)

if not reviews:
    st.info("No reviews found.")
else:
    for review in reviews:
        with st.container():
            st.markdown(f"**Review ID:** {review['sponsor_review_id']}")
            st.markdown(f"**Rating:** {review.get('rating', 'N/A')}")
            st.markdown(f"**Comment:** {review.get('comment', 'No comment')}")
            st.markdown(f"**Flagged by:** {review.get('flagged_by', 'Not flagged')}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    f"🚩 Flag Review {review['sponsor_review_id']}",
                    key=f"flag_{review['sponsor_review_id']}"
                ):
                    if flag_sponsor_review(review['sponsor_review_id']):
                        st.success("Review flagged.")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to flag review.")
            with col2:
                if st.button(
                    f"🗑️ Delete Review {review['sponsor_review_id']}",
                    key=f"delete_{review['sponsor_review_id']}"
                ):
                    if delete_sponsor_review(review['sponsor_review_id']):
                        st.success("Review deleted.")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to delete review.")
