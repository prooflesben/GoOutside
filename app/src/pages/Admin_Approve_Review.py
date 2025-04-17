import streamlit as st
import requests

st.set_page_config(page_title="Admin Reviews", layout="wide")
BASE_URL = "http://web-api-test:4000"

st.title("🔧 Admin Panel: Manage Reviews")

# -------------------
# Helpers for Sponsors
# -------------------
@st.cache_data
def fetch_sponsors():
    try:
        response = requests.get(f"{BASE_URL}/sponsor")
        response.raise_for_status()
        data = response.json()
        return response.json()  
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

# -------------------
# Flag sponsor review
# -------------------
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

# -------------------
# Delete sponsor review
# -------------------
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
# Helpers for Organizers
# -------------------
@st.cache_data
def fetch_organizers():
    try:
        res = requests.get(f"{BASE_URL}/organizers")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching organizers: {e}")
        return []

def fetch_organizer_reviews(organizer_id):
    try:
        res = requests.get(f"{BASE_URL}/organizers/{organizer_id}/reviews")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching organizer reviews: {e}")
        return []

def flag_organizer_review(organizer_id, review_id, admin_id=1):
    try:
        res = requests.put(
            f"{BASE_URL}/organizers/{organizer_id}/reviews/{review_id}",
            json={"admin_id": admin_id}
        )
        return res.status_code == 200
    except:
        return False

def delete_organizer_review(organizer_id, review_id):
    try:
        res = requests.delete(f"{BASE_URL}/organizers/{organizer_id}/reviews/{review_id}")
        return res.status_code == 200
    except:
        return False

# -------------------
# UI with Tabs
# -------------------
tab1, tab2 = st.tabs(["🏢 Sponsors", "👩‍💼 Organizers"])

# ------------------- Sponsor Tab -------------------
# … your imports and helpers …

with tab1:
    # 1) Fetch and dump raw sponsor list for debugging
    sponsors = fetch_sponsors()

    # 2) Fail fast if no sponsors
    if not sponsors:
        st.warning("No sponsors found—check that http://localhost:4001/sponsor is up.")
        st.stop()

    # 3) Build a mapping from sponsor name → sponsor_id
    sponsor_map = {s["name"]: s["sponsor_id"] for s in sponsors}

    # 4) Show the dropdown of sponsor names
    selected_name = st.selectbox("Select Sponsor", list(sponsor_map.keys()), key="sponsor_select")
    st.write("👉 selected_name:", selected_name)

    # 5) Guard against invalid selection
    if selected_name not in sponsor_map:
        st.error(f"‘{selected_name}’ not found in map—check spelling or whitespace!")
        st.stop()
    sponsor_id = sponsor_map[selected_name]

    # 6) Fetch and display reviews for the selected sponsor
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
                    if st.button(f"🚩 Flag Review {review['sponsor_review_id']}",
                                 key=f"flag_sponsor_{review['sponsor_review_id']}"):
                        if flag_sponsor_review(review['sponsor_review_id']):
                            st.success("Review flagged.")
                            st.experimental_rerun()
                        else:
                            st.error("Failed to flag review.")
                with col2:
                    if st.button(f"🗑️ Delete Review {review['sponsor_review_id']}",
                                 key=f"delete_sponsor_{review['sponsor_review_id']}"):
                        if delete_sponsor_review(review['sponsor_review_id']):
                            st.success("Review deleted.")
                            st.experimental_rerun()
                        else:
                            st.error("Failed to delete review.")


# ------------------- Organizer Tab -------------------
with tab2:
    organizers = fetch_organizers()
    organizer_map = {o["name"]: o["organizer_id"] for o in organizers}
    selected_organizer = st.selectbox("Select Organizer", organizer_map.keys(), key="organizer_select")
    organizer_id = organizer_map[selected_organizer]

    st.subheader(f"📄 Reviews for {selected_organizer}")
    reviews = fetch_organizer_reviews(organizer_id)

    if not reviews:
        st.info("No reviews found.")
    else:
        for review in reviews:
            with st.container():
                st.markdown(f"**Review ID:** {review['organizer_review_id']}")
                st.markdown(f"**Rating:** {review.get('rating', 'N/A')}")
                st.markdown(f"**Comment:** {review.get('comment', 'No comment')}")
                st.markdown(f"**Flagged by:** {review.get('flagged_by', 'Not flagged')}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"🚩 Flag Review {review['organizer_review_id']}", key=f"flag_organizer_{review['organizer_review_id']}"):
                        if flag_organizer_review(organizer_id, review['organizer_review_id']):
                            st.success("Review flagged.")
                            st.experimental_rerun()
                        else:
                            st.error("Failed to flag review.")
                with col2:
                    if st.button(f"🗑️ Delete Review {review['organizer_review_id']}", key=f"delete_organizer_{review['organizer_review_id']}"):
                        if delete_organizer_review(organizer_id, review['organizer_review_id']):
                            st.success("Review deleted.")
                            st.experimental_rerun()
                        else:
                            st.error("Failed to delete review.")
