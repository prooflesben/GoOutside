import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    Everyone hates the feeling of seeing a great event, imagining yourself going, thinking about the amazing time you could have, the food you’d eat, the sights you’d see,  only to realize the event happened last week.

Go Outside makes sure that never happens.

With Go Outside, you always stay in the loop. Beyond just browsing upcoming events, the app helps you discover new ones that match your interests. Whether you’re looking for something spontaneous or planning ahead, Go Outside makes it easy.

Event hosts also get the visibility they need, with features that help them connect directly with potential sponsors. Go Outside isn’t just about finding events; it’s a data-driven platform for event discovery and promotion, making attendance and event organization simpler and smarter.

The app uses intelligent recommendations based on your preferences, past ratings, and attendance history. You get real-time notifications for upcoming events near you, so you never miss out. For organizers, Go Outside tracks interest, monitors attendance, and highlights sponsorship opportunities, making every event easier to plan and more likely to succeed.
    """
        )


if st.button("Return to Home"):
    st.switch_page('Home.py')
