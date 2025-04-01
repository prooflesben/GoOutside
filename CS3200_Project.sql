-- SQLBook: Code
-- Dropping in case it still exists 
DROP DATABASE IF EXISTS GoOutside;CREATE DATABASE GoOutside;

USE GoOutside;--  Entities


CREATE TABLE Admin(
    admin_id int PRIMARY KEY,
    first    varchar(40)        NOT NULL,
    last     varchar(40)        NOT NULL,
    email    varchar(50) UNIQUE NOT NULL,
    phone VARCHAR(11) NOT NULL
);

CREATE TABLE EventCategory(
	name varchar(40) PRIMARY KEY
);

CREATE TABLE Attendees (
	attendee_id int PRIMARY KEY,
	first_name varchar(40) NOT NULL,
	last_name varchar(40) NOT NULL,
	email varchar(50),
	phone varchar(12),
	fav_category TEXT NOT NULL,
    CONSTRAINT FOREIGN KEY (fav_category)
        REFERENCES EventCategory(name)
);

CREATE TABLE Organizer (
	organizer_id INT NOT NULL PRIMARY KEY,
	name varchar(40) NOT NULL,
	email varchar(50) UNIQUE,
    phone varchar(11),
    bio TEXT NOT NULL DEFAULT '',
	approved_by INT NOT NULL,
    CONSTRAINT FOREIGN KEY (approved_by)
        REFERENCES Admin(admin_id)
);

CREATE TABLE Sponsors (
	sponsor_id int PRIMARY KEY,
	name varchar(40) NOT NULL,
	email varchar(50) UNIQUE NOT NULL,
	phone varchar(11),
	approved_by int NOT NULL,
    CONSTRAINT FOREIGN KEY (approved_by)
        REFERENCES Admin(admin_id)
);

CREATE TABLE Events (
	event_id int PRIMARY KEY,
	name varchar(40) NOT NULL,
	cost DECIMAL (10, 2) UNSIGNED,
	start_time DATETIME NOT NULL,
	end_time DATETIME NOT NULL,
	location varchar(100) NOT NULL,
	description TEXT DEFAULT '',
	category_name TEXT NOT NULL,
    organized_by INT NOT NULL,
	sponsor_by INT NOT NULL,
	approved_by INT NOT NULL,
    CONSTRAINT FOREIGN KEY (organized_by)
        REFERENCES Organizer(organizer_id),
    CONSTRAINT FOREIGN KEY (category_name)
        REFERENCES EventCategory(`name`),
    CONSTRAINT FOREIGN KEY (sponsor_by)
        REFERENCES Sponsors(sponsor_id),
    CONSTRAINT FOREIGN KEY (approved_by)
        REFERENCES Admin(admin_id)
);




-- Relationships




CREATE TABLE Event_Categories (
    name varchar(20) NOT NULL PRIMARY KEY,
    event_id int NOT NULL,
    CONSTRAINT FOREIGN KEY (event_id)
        REFERENCES Events(event_id)
);

CREATE TABLE Event_Announcement (
	event_announcement_id INT PRIMARY KEY,
	event_id INT NOT NULL,
	description TEXT NOT NULL,
    CONSTRAINT FOREIGN KEY (event_id)
        REFERENCES Events(event_id)
);

CREATE TABLE Admin_Announcement (
	admin_announcement_i int PRIMARY KEY,
	event_id INT NOT NULL,
	description TEXT NOT NULL DEFAULT '',
    CONSTRAINT FOREIGN KEY (event_id)
        REFERENCES Events(event_id)
);


CREATE TABLE Stats (
	stat_id INT PRIMARY KEY,
	clicks INT UNSIGNED DEFAULT 0,
	impressions INT UNSIGNED DEFAULT 0,
	event_id INT NOT NULL,
    CONSTRAINT FOREIGN KEY (event_id)
        REFERENCES Events(event_id)
);

CREATE TABLE OrganizerReviews (
	rating ENUM('1','2','3','4','5') NOT NULL,
	comments TEXT,
	written_by INT NOT NULL,
	reviewing_id INT NOT NULL,
	flagged_by INT DEFAULT NULL,
    CONSTRAINT FOREIGN KEY (written_by)
        REFERENCES Sponsors(sponsor_id),
    CONSTRAINT FOREIGN KEY (reviewing_id)
        REFERENCES Organizer(organizer_id),
    CONSTRAINT FOREIGN KEY (flagged_by)
        REFERENCES Admin(admin_id)
);


CREATE TABLE SponsorReviews (
	rating ENUM('1','2','3','4','5') NOT NULL,
	comments TEXT,
	written_by INT NOT NULL, -- organizer id
	reviewing_id INT NOT NULL, -- the id of the sponsor
	flagged_by INT DEFAULT NULL,
    CONSTRAINT FOREIGN KEY (written_by)
        REFERENCES Organizer(organizer_id),
    CONSTRAINT FOREIGN KEY (reviewing_id)
        REFERENCES Sponsors(sponsor_id),
    CONSTRAINT FOREIGN KEY (flagged_by)
        REFERENCES Admin(admin_id)

);

CREATE TABLE ChatRooms (
	organizer_id int NOT NULL,
	sponsor_id int NOT NULL,
	PRIMARY KEY (organizer_id, sponsor_id),
    CONSTRAINT FOREIGN KEY (organizer_id)
        REFERENCES Organizer(organizer_id),
    CONSTRAINT FOREIGN KEY (sponsor_id)
        REFERENCES Sponsors(sponsor_id)
);

CREATE TABLE Messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    organizer_id int NOT NULL,
    sponsor_id int NOT NULL,
	sender enum('sponsor', 'organizer') NOT NULL,
    CONSTRAINT FOREIGN KEY (organizer_id, sponsor_id)
        REFERENCES ChatRooms(organizer_id, sponsor_id)
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
    event_id INT NOT NULL,
    attendee_id INT NOT NULL,
    PRIMARY KEY (event_id, attendee_id),
    CONSTRAINT FOREIGN KEY (event_id)
        REFERENCES Events (event_id),
    CONSTRAINT FOREIGN KEY (attendee_id)
        REFERENCES Attendees (attendee_id)
);