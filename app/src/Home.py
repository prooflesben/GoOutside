##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
import requests

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of Go Outside!")
st.title('Go Outside!')
st.write('\n\n')
st.write('### Hi! As which user would you like to log in?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

# Popover for Attendee Selection
with st.expander("Attendee"):
    st.write("Select an attendee from the list below to log in as an attendee.")
    try:
        # Fetch attendee data from the backend
        response = requests.get("http://web-api:4000/attendee")
        if response.status_code == 200:
            attendees = response.json()
            attendee_names = {f"{attendee['first_name']} {attendee['last_name']}": attendee['attendee_id'] for attendee in attendees}

            # Dropdown to select an attendee
            selected_attendee_name = st.selectbox("Select an Attendee", options=list(attendee_names.keys()))

            # Submit button
            if st.button("Act as Attendee"):
                # Set session state for the selected attendee
                st.session_state['authenticated'] = True
                st.session_state['role'] = 'attendee'
                st.session_state['first_name'] = selected_attendee_name.split()[0]
                st.session_state['last_name'] = selected_attendee_name.split()[1]
                st.session_state['attendee_id'] = attendee_names[selected_attendee_name]

                logger.info(f"Logging in as Attendee: {selected_attendee_name}")
                st.success(f"Logged in as Attendee: {selected_attendee_name}")
                st.switch_page('pages/00_Attendee_Home.py')
        else:
            st.error("Failed to fetch attendees. Please try again later.")
    except Exception as e:
        st.error(f"An error occurred while fetching attendees: {e}")

# Popover for Administrator Selection
with st.expander("Administrator"):
    st.write("Select an administrator from the list below to log in as an administrator.")
    try:
        # Fetch administrator data from the backend
        response = requests.get("http://web-api:4000/admin")
        if response.status_code == 200:
            administrators = response.json()
            admin_names = {f"{admin['first']} {admin['last']}": admin['admin_id'] for admin in administrators}

            # Dropdown to select an administrator
            selected_admin_name = st.selectbox("Select an Administrator", options=list(admin_names.keys()))

            # Submit button
            if st.button("Act as Admin"):
                # Set session state for the selected administrator
                st.session_state['authenticated'] = True
                st.session_state['role'] = 'administrator'
                st.session_state['first_name'] = selected_admin_name.split()[0]
                st.session_state['last_name'] = selected_admin_name.split()[1]
                st.session_state['admin_id'] = admin_names[selected_admin_name]

                logger.info(f"Logging in as Administrator: {selected_admin_name}")
                st.success(f"Logged in as Administrator: {selected_admin_name}")
                st.switch_page('pages/20_Admin_Home.py')
        else:
            st.error("Failed to fetch administrators. Please try again later.")
    except Exception as e:
        st.error(f"An error occurred while fetching administrators: {e}")

# Popover for Sponsor Selection
with st.expander("Sponsor"):
    st.write("Select a sponsor from the list below to log in as a sponsor.")
    try:
        # Fetch sponsor data from the backend
        response = requests.get("http://web-api:4000/sponsor")
        if response.status_code == 200:
            sponsors = response.json()
            sponsor_names = {sponsor['name']: sponsor['sponsor_id'] for sponsor in sponsors}

            # Dropdown to select a sponsor
            selected_sponsor_name = st.selectbox("Select a Sponsor", options=list(sponsor_names.keys()))

            # Submit button
            if st.button("Act as Sponsor"):
                # Set session state for the selected sponsor
                st.session_state['authenticated'] = True
                st.session_state['role'] = 'sponsor'
                st.session_state['first_name'] = selected_sponsor_name
                st.session_state['sponsor_id'] = sponsor_names[selected_sponsor_name]

                logger.info(f"Logging in as Sponsor: {selected_sponsor_name}")
                st.success(f"Logged in as Sponsor: {selected_sponsor_name}")
                st.switch_page('pages/Sponsor_Home.py')
        else:
            st.error("Failed to fetch sponsors. Please try again later.")
    except Exception as e:
        st.error(f"An error occurred while fetching sponsors: {e}")
        
# Popover for Organizer Selection
with st.expander("Organizer"):
    st.write("Select an organizer from the list below to log in as an organizer.")
    try:
        # Fetch organizer data from the backend
        response = requests.get("http://web-api:4000/organizer")
        if response.status_code == 200:
            organizers = response.json()
            organizer_names = {organizer['name']: organizer['organizer_id'] for organizer in organizers}

            # Dropdown to select an organizer
            selected_organizer_name = st.selectbox("Select an Organizer", options=list(organizer_names.keys()))

            # Submit button
            if st.button("Act as Organizer"):
                # Set session state for the selected organizer
                st.session_state['authenticated'] = True
                st.session_state['role'] = 'organizer'
                st.session_state['first_name'] = selected_organizer_name
                st.session_state['organizer_id'] = organizer_names[selected_organizer_name]

                logger.info(f"Logging in as Organizer: {selected_organizer_name}")
                st.success(f"Logged in as Organizer: {selected_organizer_name}")
                st.switch_page('pages/Organizer_Home.py')
        else:
            st.error("Failed to fetch organizers. Please try again later.")
            st.error("Error: " + response.text)
    except Exception as e:
        st.error(f"An error occurred while fetching organizers: {e}")