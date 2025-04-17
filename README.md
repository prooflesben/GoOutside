# Go Outside!

Go Outside! is a web-based event management system designed to help users discover, RSVP to, and bookmark events. It also provides administrators with tools to manage events, announcements, and categories.

The system is built using **Streamlit** for the frontend, **Flask** for the backend API, and **MySQL** for the database.

This project was created by: Ben Ahrednts, Hannah Piersol, Ryaken Nakamoto, Colin Wong, and Mia Yim

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
git clone <link to the repository accessible via the green Code dropdown button>
cd GoOutside
```
### 2. Set Up the Environment
Copy the .env.template file in the api directory to your own .env file.
```
cp api/.env.template api/.env
```
In this file, set your own, secure password that will not be shared with anyone under SECRET_KEY. 

### 3. Start the Containers
Use Docker Compose to build and run all components:
```
docker-compose up --build
```
This will start:
- MySQL database
- Flask backend server on port 4000
- Streamlit frontend on port 8501

### 4. Access the Application
Once the containers are running:

Open your browser and visit http://localhost:8501 to access the Streamlit app

The Flask API will be available at http://localhost:4000

## 🔌 API Endpoints
## 🔌 API Endpoints

### For Attendees

#### RSVP Management

- `GET /attendee/<id>/rsvps`  
  Fetch all events an attendee has RSVPd to.

- `POST /attendee/<id>/rsvps/<eventId>`  
  RSVP to an event.

- `DELETE /attendee/<id>/rsvps/<eventId>`  
  Un-RSVP from an event.

#### Bookmark Management

- `GET /attendee/<id>/bookmarks`  
  Fetch all bookmarked events for an attendee.

- `POST /attendee/<id>/bookmarks/<eventId>`  
  Bookmark an event.

- `DELETE /attendee/<id>/bookmarks/<eventId>`  
  Remove a bookmark.

#### Recommendations

- `GET /attendee/<id>/recommendations`  
  Fetch recommended events based on attendee preferences.

#### Event Announcements

- `GET /attendee/<id>/event_announcments`  
  Fetch event-specific announcements.

- `GET /attendee/<id>/admin_announcments`  
  Fetch admin announcements.

#### Organizer Interaction

- `GET /attendee/<id>/organizers`  
  Fetch all event organizers of events an attendee has attended.

#### Reviews

- `POST /attendee/<attendee_id>/review/organizer/<organizer_id>`  
  Submit a review for an organizer.

- `DELETE /attendee/<attendee_id>/reviews/<review_id>`  
  Delete a review.

#### Calendar Integration

- `PUT /attendee/<id>/calendar/<eventId>`  
  Generate a calendar entry for an event.

---

### For Administrators

#### Event Management

- `GET /admin/announcements`  
  Fetch all admin announcements.

- `POST /admin/announcement`  
  Create an admin announcement.

- `PUT /admin/<admin_id>/event/<event_id>`  
  Approve an event.

- `DELETE /admin/<admin_id>/event/<event_id>`  
  Delete an event.

#### Sponsor Reviews

- `PUT /admin/sponsor-reviews`  
  Flag sponsor reviews.

---

### For Event Organizers

#### Event Management

- `GET /organizer/<organizer_id>/events`  
  Fetch all events created by an organizer.

- `POST /organizer/<organizer_id>/events`  
  Create a new event.

#### Announcements

- `POST /organizer/announcement`  
  Create an event announcement.

- `GET /organizer/announcements`  
  Fetch all event announcements.

#### Reviews

- `POST /organizer/<organizer_id>/reviews/<sponsor_id>`  
  Submit a review for a sponsor.

- `DELETE /organizer/<organizer_id>/reviews/<sponsor_id>`  
  Delete a sponsor review.

#### Statistics

- `GET /organizer/<id>/highest-engagement`  
  Fetch the event with the highest engagement for an organizer.

- `GET /organizer/<int:id>/stats/average-rating`  
  Fetch the average rating for an organizer.

---

### For Sponsors

#### Event Sponsorship

- `PUT /sponsors/<sponsor_id>/events/<event_id>`  
  Sponsor an event.

- `DELETE /sponsors/<sponsor_id>/events/<event_id>`  
  Remove sponsorship from an event.

#### Reviews

- `GET /sponsors/<sponsor_id>/reviews`  
  Fetch all reviews for a sponsor.

#### Statistics

- `GET /sponsors/<sponsor_id>/events/stats`  
  Fetch engagement statistics for sponsored events.

---

### General Event Endpoints

#### Event Details

- `GET /events`  
  Fetch all events.

- `GET /events/<event_id>`  
  Fetch details for a specific event.

- `DELETE /events/<event_id>`  
  Delete an event.

#### Event Announcements

- `GET /events/<event_id>/announcement`  
  Fetch announcements for a specific event.

- `POST /events/<event_id>/announcement`  
  Create an announcement for a specific event.

#### Event Statistics

- `GET /events/<event_id>/stats`  
  Fetch statistics for a specific event.

- `GET /events/<event_id>/attendance`  
  Fetch attendees for a specific event.

#### Event Search

- `GET /events/search/<location>/<category>/<date>`  
  Search for events by location, category, and date.


