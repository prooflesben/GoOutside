# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

#### ------------------------ Examples for Role of Attendee ------------------------
def AttendeeHomeNav():
    st.sidebar.page_link(
        "pages/00_Attendee_Home.py", label="Attendee Home", icon="👤"
    )

def AttendeeInboxNav():
    st.sidebar.page_link(
        "pages/05_Attendee_Inbox.py", label="Message Inbox", icon="📬"
    ) 


## ------------------------ Examples for Role of Admin ------------------------
def AdminHomeNav():
    st.sidebar.page_link(
        "pages/10_Admin_Home.py", label="Admin Home", icon="👤"
    )

def AdminAnnouncementsNav():
    st.sidebar.page_link(
        "pages/11_Admin_Announcements.py", label="Announcements", icon="📢"
    )

def AdminApproveEventsNav():
    st.sidebar.page_link(
        "pages/12_Admin_Approve_Events.py", label="Approve Events", icon="✅"
    )


#### ------------------------ Sponsor ------------------------
def SponsorHomeNav():
    st.sidebar.page_link(
        "pages/Sponsor_Home.py", label="Sponsor Home", icon="👤"
    )

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """
    
    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=250)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()
        AboutPageNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "attendee":
            AttendeeHomeNav()
            AttendeeInboxNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "admin":
            AdminHomeNav()
            AdminAnnouncementsNav()
            AdminApproveEventsNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "sponsor":
            SponsorHomeNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
