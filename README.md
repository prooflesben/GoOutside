# GoOutside: Event Management System

GoOutside is a web-based event management system designed to help users discover, RSVP to, and bookmark events. It also provides administrators with tools to manage events, announcements, and categories.

The system is built using **Streamlit** for the frontend, **Flask** for the backend API, and **MySQL** for the database.

---

## 🛠 Prerequisites

To run this project, ensure you have the following:

- A GitHub Account  
- A terminal-based Git client or GUI Git client (e.g., GitHub Desktop or the Git plugin for VSCode)  
- VSCode with the Python Plugin  
- A distribution of Python (Anaconda or Miniconda recommended)  
- Docker (for containerized deployment)  

---

## 📦 Project Components

This project consists of three main components, each running in its own Docker container:

- **Streamlit App**: Located in the `app` directory — the frontend.
- **Flask REST API**: Located in the `api` directory — handles backend logic and database interaction.
- **MySQL Database**: Initialized using SQL scripts from the `database-files` directory.

---

## ✨ Features

### For Attendees

- **Search Events**: Filter events by category, cost, and name.
- **RSVP to Events**: RSVP and manage your RSVPs.
- **Bookmark Events**: Save events for easy access.
- **Recommended Events**: Get personalized suggestions based on RSVPs and bookmarks.

### For Administrators

- **Event Management**: Approve or reject events submitted by organizers.
- **Category Management**: View and add new event categories.
- **Announcements**: Post event-related announcements.
- **Event Statistics**: View statistics by organizer.

### For Event Organizers

- **Create Events**: Organizers can create new events with details such as name, cost, location, and description.
- **Promote Events**: Promote events to increase visibility and attendance.
- **View Event Statistics**: Access detailed statistics for events, including RSVPs and bookmarks.
- **Manage Announcements**: Post announcements to keep attendees informed about event updates.

### For Sponsors

- **Sponsor Events**: Choose events to sponsor and provide financial or logistical support.
- **View Sponsored Events**: Access a list of events you are sponsoring.
- **Engagement Metrics**: View metrics such as clicks and impressions for sponsored events.
- **Collaborate with Organizers**: Work closely with event organizers to ensure successful sponsorships.

---

## ⚙️ Setting Up the Project

### 1. Clone the Repository

```
git clone https://github.com/your-username/gooutside.git
cd gooutside
```