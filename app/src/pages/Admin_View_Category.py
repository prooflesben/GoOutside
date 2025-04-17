import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks


# Page config
st.set_page_config(page_title="Admin - Event Categories", layout="centered")

SideBarLinks()

st.title("📂 Admin Panel: Event Categories")
st.markdown("View and manage event categories below.")

# -------------------
# Fetch categories
# -------------------
@st.cache_data
def fetch_categories():
    try:
        response = requests.get('http://web-api:4000/event_categories')
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)  # Ensure it's a DataFrame
    except Exception as e:
        st.error(f"Failed to fetch categories: {e}")
        return pd.DataFrame()  # Return empty DataFrame to prevent crashes

# -------------------
# Add a new category
# -------------------
st.subheader("➕ Add New Event Category")
with st.form("add_category_form"):
    new_name = st.text_input("Category Name", max_chars=50)
    new_description = st.text_area("Description", height=100)
    submit = st.form_submit_button("Add Category")

    if submit:
        if not new_name.strip():
            st.warning("Category name cannot be empty.")
        else:
            payload = {"name": new_name.strip(), "description": new_description.strip()}
            try:
                post_resp = requests.post("http://web-api:4000/event_categories", json=payload)
                if post_resp.status_code == 200:
                    st.success(f"Category '{new_name}' added successfully!")
                    st.cache_data.clear()  # Clear cache to force refresh
                else:
                    st.error(f"Failed to add category. Status code: {post_resp.status_code}")
            except requests.RequestException as e:
                st.error(f"Error: {e}")

# -------------------
# Display existing categories
# -------------------
st.subheader("📄 Current Categories")

categories_df = fetch_categories()

if categories_df.empty:
    st.info("No categories found.")
else:
    st.dataframe(categories_df)
