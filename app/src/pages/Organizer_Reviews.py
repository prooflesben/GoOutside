import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests

st.set_page_config(page_title="Organizer Reviews", layout="wide")

# Get organizer_id and event_id from session state, defaults to 1 if not set
organizer_id = st.session_state.get('organizer_id', 1)  
event_id = st.session_state.get('event_id', 1)  

if st.button("Back to Events"):
    st.switch_page('pages/Sponsor_Events.py')

st.title("Organizer Reviews and Event Statistics")
# 2 columns for layout, 1 for stats, 1 for reviews
col1, col2 = st.columns([1, 2])

# first col is stats
with col1:
    st.subheader("Event Statistics")
    try:
        response = requests.get(f'http://web-api-test:4000/events/{event_id}/stats')
        if response.status_code == 200:
            stats = response.json()
            
            # some bar graph
            st.metric("Total Impressions", stats.get("impressions", 0))
            st.metric("Total Clicks", stats.get("clicks", 0))
            stats_data = {
                "Metric": ["Impressions", "Clicks"],
                "Count": [stats.get("impressions", 0), stats.get("clicks", 0)]
            }
            fig = px.bar(stats_data, x="Metric", y="Count", title="Event Engagement Metrics")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No statistics available for this event")
    except Exception as e:
        st.error(f"Error fetching event stats: {str(e)}")

# have reviews
with col2:
    st.subheader("Organizer Reviews")
    try:
        # get review data from api
        response = requests.get(f'http://web-api-test:4000/organizer/{organizer_id}/reviews')
        if response.status_code == 200:
            reviews = response.json()
            if reviews:
                avg_rating = sum(float(review["rating"]) for review in reviews) / len(reviews)
                
                # Display average rating
                st.write(f"Average Rating: {avg_rating:.1f} ⭐ ({len(reviews)} reviews)")
                
                # rating distribution bar graph
                # values_counts/sort_index groups by rating and sorts ascending
                rating_counts = pd.DataFrame(reviews)["rating"].value_counts().sort_index()
                fig = px.bar(rating_counts, title="Rating Distribution")
                fig.update_layout(xaxis_title="Rating", yaxis_title="Number of Reviews")
                st.plotly_chart(fig, use_container_width=True)
                st.subheader("Recent Reviews")
                # iterate through reviews, display them
                for review in reviews:
                    with st.expander(f"⭐ {review['rating']} - {review['first_name']} {review['last_name']}"):
                        st.write(f"**Review:** {review['comments']}")
            else:
                st.info("No reviews available for this organizer")
        else:
            st.info("No reviews available for this organizer")
    except Exception as e:
        st.error(f"Error fetching reviews: {str(e)}")
