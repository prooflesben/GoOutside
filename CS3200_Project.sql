


CREATE DATABASE GoOutside;

USE GoOutside;

-- Entities

CREATE TABLE Admin (
	admin_id int PRIMARY KEY,
	first varchar(40) NOT NULL,
	last varchar(40) NOT NULL,
	email varchar(50),
	phone varchar(15)
);

CREATE TABLE EventCategory (
	category_id int PRIMARY KEY,
	name varchar(40) NOT NULL
);

CREATE TABLE Attendees (
	attendee_id int PRIMARY KEY,
	first_name varchar(40) NOT NULL,
	last_name varchar(40) NOT NULL,
	email varchar(50),
	phone varchar(12),
	fav_category INT NOT NULL,
    CONSTRAINT FOREIGN KEY (fav_category)
        REFERENCES EventCategory(category_id)
);

CREATE TABLE Organizer (
	organizer_id INT NOT NULL,
	name varchar(40) NOT NULL,
	email varchar(50),
	phone varchar(15),
	bio TEXT,
	PRIMARY KEY(organizer_id),
	approved_by int NOT NULL,
    CONSTRAINT FOREIGN KEY (approved_by)
        REFERENCES Admin(admin_id)
);

CREATE TABLE Sponsors (
	sponsor_id int PRIMARY KEY,
	name varchar(40) NOT NULL,
	email varchar(50),
	phone varchar(15),
	approved_by int NOT NULL,
    CONSTRAINT FOREIGN KEY (approved_by)
        REFERENCES Admin(admin_id)
);

CREATE TABLE Events (
	event_id int PRIMARY KEY,
	name varchar(40) NOT NULL,
	email varchar(50),
	cost DECIMAL (10, 2) UNSIGNED,
	start_time DATETIME NOT NULL,
	end_time DATETIME NOT NULL,
	location varchar(100) NOT NULL,
	description TEXT,
	organized_by INT NOT NULL,
	category_id INT NOT NULL,
	sponsor_by INT NOT NULL,
	approved_by INT NOT NULL,
    CONSTRAINT FOREIGN KEY (organized_by)
        REFERENCES Organizer(organizer_id),
    CONSTRAINT FOREIGN KEY (category_id)
        REFERENCES EventCategory(category_id),
    CONSTRAINT FOREIGN KEY (sponsor_by)
        REFERENCES Sponsors(sponsor_id),
    CONSTRAINT FOREIGN KEY (approved_by)
        REFERENCES Admin(admin_id)
);




-- Relationships

CREATE TABLE Event_Announcement (
	event_announcement_id INT PRIMARY KEY,
	event_id INT NOT NULL,
	description TEXT NOT NULL,
    CONSTRAINT FOREIGN KEY (event_id)
        REFERENCES Events(event_id)
);

CREATE TABLE Admin_Announcement (
	admin_announcement_id INT PRIMARY KEY,
	event_id INT NOT NULL,
	description TEXT NOT NULL,
    CONSTRAINT FOREIGN KEY (event_id)
        REFERENCES Events(event_id)
);


CREATE TABLE Analytics (
	analytics_id int PRIMARY KEY,
	clicks INT UNSIGNED DEFAULT 0,
	impressions INT UNSIGNED DEFAULT 0,
	event_id INT NOT NULL,
    CONSTRAINT FOREIGN KEY (event_id)
        REFERENCES Events(event_id)
);

CREATE TABLE OrganizerReviews (
	rating ENUM('0','1','2','3','4','5') NOT NULL,
	comments TEXT,
	written_by INT NOT NULL,
	reviewing_id INT NOT NULL,
	approved_by INT NOT NULL,
    CONSTRAINT FOREIGN KEY (written_by)
        REFERENCES Sponsors(sponsor_id),
    CONSTRAINT FOREIGN KEY (reviewing_id)
        REFERENCES Organizer(organizer_id),
    CONSTRAINT FOREIGN KEY (approved_by)
        REFERENCES Admin(admin_id)
);


CREATE TABLE SponsorReviews (
	rating ENUM('0','1','2','3','4','5') NOT NULL,
	comments TEXT,
	written_by INT NOT NULL, -- organizer id
	reviewing_id INT NOT NULL, -- the id of the sponsor
	approved_by INT NOT NULL,
    CONSTRAINT FOREIGN KEY (written_by)
        REFERENCES Organizer(organizer_id),
    CONSTRAINT FOREIGN KEY (reviewing_id)
        REFERENCES Sponsors(sponsor_id),
    CONSTRAINT FOREIGN KEY (approved_by)
        REFERENCES Admin(admin_id)

);

CREATE TABLE ChatRooms (
	organizer_id int NOT NULL,
	sponsor_id int NOT NULL,
	chat_room_id int PRIMARY KEY,
    CONSTRAINT FOREIGN KEY (organizer_id)
        REFERENCES Organizer(organizer_id),
    CONSTRAINT FOREIGN KEY (sponsor_id)
        REFERENCES Sponsors(sponsor_id)
);

CREATE TABLE Notifications (
	message TEXT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE Event_Attendance (
  event_id int NOT NULL,
  attendee_id int NOT NULL,
  PRIMARY KEY (event_id, attendee_id),
  CONSTRAINT FOREIGN KEY (event_id)
      REFERENCES Events(event_id),
    CONSTRAINT FOREIGN KEY (attendee_id)
        REFERENCES Attendees(attendee_id)
);

CREATE TABLE Event_Bookmarks (
    event_id    int NOT NULL,
    attendee_id int NOT NULL,
    PRIMARY KEY (event_id, attendee_id),
    CONSTRAINT FOREIGN KEY (event_id)
        REFERENCES Events (event_id),
    CONSTRAINT FOREIGN KEY (attendee_id)
        REFERENCES Attendees (attendee_id)
);