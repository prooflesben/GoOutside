import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

# getting some metadata
sponsor_id = st.session_state.get('sponsor_id', 1)
organizer_id = st.session_state.get('organizer_id', 1)
first_name = st.session_state.get('first_name', 'Sponsor')
sender = st.session_state['role']

# Function to fetch available organizers
def fetch_organizers():
    try:
        resp = requests.get("http://web-api:4000/organizer")
        if resp.ok:
            return resp.json()
        else:
            st.error("Failed to fetch organizers.")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []

# Function to fetch available sponsors
def fetch_sponsors():
    try:
        resp = requests.get("http://web-api:4000/sponsor")
        if resp.ok:
            return resp.json()
        else:
            st.error("Failed to fetch sponsors.")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []

# Display organizer selection if user is a sponsor
if sender == 'sponsor':
    organizers = fetch_organizers()
    # iterate and display
    if organizers:
        organizer_options = {org['name']: org['organizer_id'] for org in organizers}
        # allow user to select w/ selectbox
        selected_organizer_name = st.selectbox(
            "Select an organizer to chat with:",
            options=list(organizer_options.keys())
        )
        # after selection extract the id
        organizer_id = organizer_options[selected_organizer_name]
    else:
        st.error("No organizers available to chat with.")
        st.stop()
# Display sponsor selection if user is an organizer
elif sender == 'organizer':
    sponsors = fetch_sponsors()
    # iterate and display
    if sponsors:
        sponsor_options = {sponsor['name']: sponsor['sponsor_id'] for sponsor in sponsors}
        # allow user to select w/ selectbox
        selected_sponsor_name = st.selectbox(
            "Select a sponsor to chat with:",
            options=list(sponsor_options.keys())
        )
        # after selection extract the id
        sponsor_id = sponsor_options[selected_sponsor_name]
    else:
        st.error("No sponsors available to chat with.")
        st.stop()

st.title(f"Chatroom, {first_name}")
st.write("### Welcome to the Chatroom")

# gets the fetch history, returns as JSON
def fetch_chat_history():
    try:
        resp = requests.get(f"http://web-api:4000/chatroom/{sponsor_id}/{organizer_id}/messages")
        if resp.ok:
            return resp.json() 
        else:
            st.error("Failed to fetch chat history.")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []

# will POST a message, then clear the chatbox
def send_message():
    if st.session_state.message_input.strip():
        payload = {"content": st.session_state.message_input, "sender": sender}
        resp = requests.post(f"http://web-api:4000/chatroom/{sponsor_id}/{organizer_id}/messages", json=payload)
        # if the msg went thru, we can clear the textbox
        if resp.ok:
            st.session_state.message_input = "" 
            # and then refresh
            st.session_state.chat_history = fetch_chat_history()
        else:
            st.error("Failed to send message.")
    else:
        st.warning("Please type a message before sending.")

# refresh the chat history
chat_history = st.session_state.get('chat_history', fetch_chat_history())
if st.button("Refresh Chat"):
    chat_history = fetch_chat_history()
    st.session_state['chat_history'] = chat_history

# display chat history
st.markdown("#### Chat History")
if chat_history:
    for msg in chat_history:
        # format: sender: content (timestamp)
        st.write(f"**{msg['sender']}**: {msg['content']}  *({msg['created_at']})*")
else:
    st.write("No messages yet. Start the conversation!")

# textbox
st.text_area("Type your message below:", height=100, key="message_input")

# will send msg
st.button("Send Message", on_click=send_message)

# exit button
if st.button('Back To Main', type='primary', use_container_width=True):
    if sender == 'sponsor':
        st.switch_page('pages/Sponsor_Home.py')
    elif sender == 'organizer':
        st.switch_page('pages/Organizer_Home.py')
