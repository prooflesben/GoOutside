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

def AttendeeSearchEventsNav():
    st.sidebar.page_link(
        'pages/Search_New_Events.py', label="Search for New Events", icon="🔍"
    ) 

def AttendeeBookMarksNav():
    st.sidebar.page_link(
        'pages/Attendee_Bookmarks.py', label="View Bookmarks", icon="🔖"
    ) 

def AttendeeRSVPSNav():
    st.sidebar.page_link(
        'pages/Attendee_Rsvps.py', label="View RSVPs", icon="📅"
    ) 

def AttendeeReviewOrganizerNav():
    st.sidebar.page_link(
        'pages/Review_Organizer.py', label="Review Organizer", icon="🧑‍💼"
    ) 


## ------------------------ Examples for Role of Admin ------------------------
def AdminHomeNav():
    st.sidebar.page_link(
        "pages/20_Admin_Home.py", label="Admin Home", icon="👤"
    )

def AdminAnnouncementsNav():
    st.sidebar.page_link(
        "pages/Admin_Announcement.py", label="Announcements", icon="📢"
    )

def AdminApproveEventsNav():
    st.sidebar.page_link(
        "pages/Admin_Approve_Event.py", label="Approve Events", icon="✅"
    )

def AdminViewEditCategoriesNav():
    st.sidebar.page_link(
        'pages/Admin_View_Category.py', label="View/Edit Categories", icon="🏷️"
    )




#### ------------------------ Sponsor ------------------------
def SponsorHomeNav():
    st.sidebar.page_link(
        "pages/Sponsor_Home.py", label="Sponsor Home", icon="👤"
    )

def SponsorEnterChatRoomNav():
    st.sidebar.page_link(
        'pages/Chat_Room.py', label="Chat Room", icon="💬"
    )

def SponsorStasticsNav():
    st.sidebar.page_link(
        'pages/Sponsor_Stats.py', label="Statistics", icon="📊"
    )

def SponsorEventsNav():
    st.sidebar.page_link(
        'pages/Sponsor_Events.py', label="Sponsor Events", icon="📅"
    )

#### ------------------------ Organizer ------------------------
def OrganizerHomeNav():
    st.sidebar.page_link(
        "pages/Organizer_Home.py", label="Organizer Home", icon="👤"
    )

def OrganizerEnterChatRoomNav():
    st.sidebar.page_link(
        'pages/Chat_Room.py', label="Chat Room", icon="💬"
    )

def OrganizerCreateEventNav():
    st.sidebar.page_link(
        'pages/Create_Event.py', label="Create Event", icon="📅"
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
            AttendeeSearchEventsNav()
            AttendeeBookMarksNav()
            AttendeeRSVPSNav()
            AttendeeReviewOrganizerNav()


        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminHomeNav()
            AdminAnnouncementsNav()
            AdminApproveEventsNav()
            AdminViewEditCategoriesNav()
          

        # If the user is an sponsor, give them access to the sponsor pages
        if st.session_state["role"] == "sponsor":
            SponsorHomeNav()
            SponsorEnterChatRoomNav()
            SponsorStasticsNav()
            SponsorEventsNav()
        
        # If the user is a organizer, give them access to the organizer pages
        if st.session_state["role"] == "organizer":
            OrganizerHomeNav()
            OrganizerEnterChatRoomNav()
            OrganizerCreateEventNav()


    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
