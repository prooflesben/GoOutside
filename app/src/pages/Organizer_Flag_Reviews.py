import streamlit as st
import requests
from modules.nav import SideBarLinks

API_BASE = "http://web-api-test:4000"
ADMIN_ID = st.session_state.get("admin_id", 1)

SideBarLinks()
st.title("🛡️ Review Moderation – Organizer Reviews")

# Track hidden (flagged/deleted) reviews during session
if "hidden_reviews" not in st.session_state:
    st.session_state["hidden_reviews"] = set()

@st.cache_data(show_spinner=False)
def load_reviews():
    try:
        res = requests.get(f"{API_BASE}/organizer_reviews")
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"Failed to load reviews: {res.status_code}")
            return []
    except Exception as e:
        st.error(f"Error loading reviews: {e}")
        return []

reviews = load_reviews()

# Filter out hidden reviews
visible_reviews = [r for r in reviews if r["org_review_id"] not in st.session_state["hidden_reviews"]]

if not visible_reviews:
    st.info("No visible reviews.")
    st.stop()

for review in visible_reviews:
    review_id = review["org_review_id"]
    rating = review["rating"]
    comments = review["comments"] or "No comment provided."
    written_by = review.get("written_by")
    being_reviewed = review.get("being_reviewed")
    flagged_by = review.get("flagged_by")

    with st.container():
        st.markdown(f"### Review #{review_id}")
        st.markdown(f"⭐ **Rating:** {rating}")
        st.markdown(f"🧾 **Comment:** {comments}")
        st.markdown(f"✍️ **Written By:** {written_by or 'Anonymous'}")
        st.markdown(f"🧑‍💼 **Organizer Reviewed (ID):** {being_reviewed}")

        col1, col2 = st.columns(2)
        with col1:
            if flagged_by:
                st.info(f"🚩 Already flagged by Admin ID **{flagged_by}**")
            else:
                if st.button("🚩 Flag Review", key=f"flag_{review_id}"):
                    try:
                        r = requests.put(f"{API_BASE}/admin/{ADMIN_ID}/organizer_reviews/{review_id}")
                        if r.status_code == 200:
                            st.success("Review flagged ✅")
                            st.session_state["hidden_reviews"].add(review_id)
                        else:
                            st.error("Failed to flag review.")
                    except Exception as e:
                        st.error(f"Error flagging: {e}")

        with col2:
            if st.button("🗑️ Delete Review", key=f"delete_{review_id}"):
                try:
                    r = requests.delete(f"{API_BASE}/organizer_reviews/organizer/{review_id}")
                    if r.status_code == 200:
                        st.warning(f"Review #{review_id} deleted.")
                        st.session_state["hidden_reviews"].add(review_id)
                    else:
                        st.error("Failed to delete review.")
                except Exception as e:
                    st.error(f"Error deleting: {e}")

        st.divider()
