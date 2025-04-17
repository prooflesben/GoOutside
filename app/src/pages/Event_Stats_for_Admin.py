import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests
from modules.nav import SideBarLinks


st.set_page_config(page_title="Organizer Reviews", layout="wide")

SideBarLinks()

# Get organizer_id and event_id from session state, defaults to 1 if not set
organizer_id = st.session_state.get('organizer_id', 1)  
event_id = st.session_state.get('event_id', 1)  

st.title("Organizer Reviews and Statistics")


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
