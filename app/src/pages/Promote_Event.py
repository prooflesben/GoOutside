import logging
import os
import streamlit as st
from modules.nav import SideBarLinks
import requests

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged-in user
SideBarLinks()

# Fetch events from the backend
results = None
try:
    response = requests.get(f"http://web-api:4000/events")
    response.raise_for_status()
    results = response.json()
except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch events: {e}")

# Page title
st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('')

# Fetch categories for filtering
try:
    category_response = requests.get("http://web-api:4000/event_categories/")
    category_response.raise_for_status()
    categories = category_response.json()
    category_names = [category["name"] for category in categories]
    category_names.insert(0, "All")  # Add "All" option for no filtering
    events_response = requests.get("http://web-api:4000/events")
    events_response.raise_for_status()
    results = events_response.json()  # Populate the `results` variable with event data
except Exception as e:
    st.error(f"Failed to fetch events: {e}")
    results = []
except Exception as e:
    st.error(f"Failed to fetch categories: {e}")
    categories = []
    category_names = ["All"]

# Add filters
# Add filters
st.sidebar.header("Filter Events")
selected_category = st.sidebar.selectbox("Category", category_names)
max_cost = st.sidebar.slider("Maximum Cost ($)", min_value=0, max_value=500, value=500, step=10)
search_term = st.sidebar.text_input("Search by Event Name", "")  # Add a text input for event name search

# Add a "Clear Filters" button
if st.sidebar.button("Clear Filters"):
    selected_category = "All"
    max_cost = 500
    search_term = ""

def event_card(event):
    with st.container():
        st.subheader(event["name"])
        st.caption(f"📅 {event['start_time']} — {event['end_time']}")
        st.write(f"📍 Location: {event['location']}")
        st.write(f"💸 Cost: ${event['cost']}")
        st.write(f"🏷️ Category: {event['category_name']}")
        if event['sponsor_by']:
            st.write(f"🤝 Sponsored By: {event['sponsor_name']}")
        st.write(f"**Event Details:**\n{event['description']}")
        
        
        try:
            if st.button("Promote Event", key=f"promote_{event['event_id']}"):
                # Assuming you have a function to handle the promotion logic
                resp = requests.post(f"http://web-api:4000/events/{event['event_id']}/promote")
                st.success(f"Event {event['name']} promoted successfully!")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch RSVP status: {e}")

# Filter events
if results:
    filtered_events = results
    if selected_category != "All":
        filtered_events = [event for event in filtered_events if event["category_name"] == selected_category]
    filtered_events = [event for event in filtered_events if float(event["cost"]) <= max_cost]
    # Convert cost to float for comparison
    filtered_events = [event for event in filtered_events if float(event["cost"]) <= max_cost]
    # Filter by search term
    if search_term:
        filtered_events = [event for event in filtered_events if search_term.lower() in event["name"].lower()]

    if filtered_events:
        for event in filtered_events:
            event_card(event)
    else:
        st.info("No events match your filters.")
else:
    st.info("No events available.")