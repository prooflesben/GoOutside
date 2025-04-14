import streamlit as st
import datetime

# Set page configuration
st.set_page_config(page_title="Event Approval", layout="wide")

def get_event_details():
    # In a real application, this would fetch data from your database or API
    # This is a mock function for demonstration
    return {
        "event_name": "Tech Conference 2025",
        "organizer": "Tech Solutions Inc.",
        "organizer_rating": 4.5,
        "location": "123 Main St, New York, NY 10001",
        "date": datetime.date(2025, 6, 15),
        "start_time": datetime.time(12, 0),
        "end_time": datetime.time(13, 0),
        "is_sponsored": True,
        "sponsors": ["Paws", "NEU", "Gojo"],
        "capacity": 50,
        "description": "A cutting-edge conference featuring the latest in technology innovations and networking opportunities for professionals in the tech industry."
    }

def approve_event():
    # In a real application, this would update the database
    st.success("Event has been approved!")
    # You could add API calls here:
    # requests.post("your-flask-api/events/approve", json={"event_id": event_id})

def deny_event():
    # In a real application, this would update the database
    st.error("Event has been denied!")
    # You could add API calls here:
    # requests.post("your-flask-api/events/deny", json={"event_id": event_id})

# Get event details
event = get_event_details()

# Add custom CSS
st.markdown("""
<style>
.main-container {
    border: 2px solid #ccc;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
}
.event-title {
    background-color: #ffaaa5;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
    font-size: 24px;
    margin-bottom: 20px;
}
.description-box {
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 5px;
    min-height: 150px;
    margin: 15px 0;
}
.approve-btn {
    background-color: #a8e6cf;
    padding: 10px 20px;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
}
.deny-btn {
    background-color: #ffaaa5;
    padding: 10px 20px;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Event title
st.markdown(f'<div class="event-title">{event["event_name"]}</div>', unsafe_allow_html=True)

# Display event details
col1, col2 = st.columns([1, 2])
    
with col1:
    st.markdown("**Organizer:**")
    st.markdown("**Average Organizer Rating:**")
    st.markdown("**Location:**")
    st.markdown("**Date:**")
    st.markdown("**Start time:**")
    st.markdown("**End time:**")
    st.markdown("**Sponsored?:**")
    if event["is_sponsored"]:
        st.markdown("**Sponsor Names:**")
    st.markdown("**Event Capacity:**")

with col2:
    st.markdown(event["organizer"])
    st.markdown(f"{event['organizer_rating']}/5")
    st.markdown(event["location"])
    st.markdown(event["date"].strftime("%m/%d/%Y"))
    st.markdown(event["start_time"].strftime("%I:%M %p"))
    st.markdown(event["end_time"].strftime("%I:%M %p"))
    st.markdown("Yes" if event["is_sponsored"] else "No")
    if event["is_sponsored"]:
        st.markdown(", ".join(event["sponsors"]))
    st.markdown(str(event["capacity"]))

# Description section with proper formatting
st.markdown(f'''
<div class="description-box">
    <strong>Description:</strong><br>
    {event["description"]}
</div>
''', unsafe_allow_html=True)

# Close the main container div
st.markdown('</div>', unsafe_allow_html=True)

# Approval buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    approve_button = st.button("Approve ✓", key="approve")
    if approve_button:
        approve_event()

with col3:
    deny_button = st.button("Deny ✗", key="deny")
    if deny_button:
        deny_event()