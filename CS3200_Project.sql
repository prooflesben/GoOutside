-- Dropping in case it still exists
DROP DATABASE IF EXISTS GoOutside;
CREATE DATABASE GoOutside;

USE GoOutside;

--  Entities

CREATE TABLE Admin
(
    admin_id int PRIMARY KEY AUTO_INCREMENT,
    first    varchar(40)        NOT NULL,
    last     varchar(40)        NOT NULL,
    email    varchar(50) UNIQUE NOT NULL,
    phone    VARCHAR(11)        NOT NULL
);

CREATE TABLE Event_Categories
(
    name        varchar(20) PRIMARY KEY,
    description TEXT        NOT NULL
);


CREATE TABLE Attendees
(
    attendee_id  int PRIMARY KEY AUTO_INCREMENT,
    first_name   varchar(40) NOT NULL,
    last_name    varchar(40) NOT NULL,
    email        varchar(50),
    phone        varchar(12),
    fav_category varchar(20) NOT NULL,
    CONSTRAINT FOREIGN KEY (fav_category)
        REFERENCES Event_Categories(`name`) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE Organizer
(
    organizer_id INT         NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name         varchar(40) NOT NULL,
    email        varchar(50) UNIQUE,
    phone        varchar(11),
    bio          TEXT        NOT NULL,
    approved_by  INT         NOT NULL,
    CONSTRAINT FOREIGN KEY (approved_by)
        REFERENCES Admin (admin_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE Sponsors
(
    sponsor_id  int PRIMARY KEY AUTO_INCREMENT,
    name        varchar(40)        NOT NULL,
    email       varchar(50) UNIQUE NOT NULL,
    phone       varchar(11),
    approved_by int                NOT NULL,
    CONSTRAINT FOREIGN KEY (approved_by)
        REFERENCES Admin (admin_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE Events
(
    event_id      int PRIMARY KEY AUTO_INCREMENT,
    name          varchar(40)  NOT NULL,
    cost          DECIMAL(10, 2) UNSIGNED NOT NULL,
    start_time    DATETIME     NOT NULL,
    end_time      DATETIME     NOT NULL,
    location      varchar(100) NOT NULL,
    description   TEXT NOT NULL,
    category_name VARCHAR(20)  NOT NULL,
    organized_by  INT          NOT NULL,
    sponsor_by    INT          DEFAULT NULL,
    approved_by   INT          DEFAULT NULL,
    sponsor_cost  INT          DEFAULT NULL,
    CONSTRAINT FOREIGN KEY (organized_by)
        REFERENCES Organizer (organizer_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FOREIGN KEY (category_name)
        REFERENCES Event_Categories (`name`) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FOREIGN KEY (sponsor_by)
        REFERENCES Sponsors (sponsor_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FOREIGN KEY (approved_by)
        REFERENCES Admin (admin_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX (start_time, category_name,end_time)
);


-- Relationships

CREATE TABLE Event_Announcement
(
    event_announcement_id INT PRIMARY KEY AUTO_INCREMENT,
    event_id              INT  NOT NULL,
    description           TEXT NOT NULL,
    CONSTRAINT FOREIGN KEY (event_id)
        REFERENCES Events (event_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE Admin_Announcement
(
    admin_announcement_id INT PRIMARY KEY AUTO_INCREMENT,
    event_id             INT  NOT NULL,
    description          TEXT NOT NULL,
    CONSTRAINT FOREIGN KEY (event_id)
        REFERENCES Events (event_id) ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE Stats
(
    stat_id     INT PRIMARY KEY AUTO_INCREMENT,
    clicks      INT UNSIGNED DEFAULT 0,
    impressions INT UNSIGNED DEFAULT 0,
    event_id    INT NOT NULL,
    CONSTRAINT FOREIGN KEY (event_id)
        REFERENCES Events (event_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE OrganizerReviews
(
    org_review_id  INT PRIMARY KEY AUTO_INCREMENT,
    rating         ENUM ('1','2','3','4','5') NOT NULL,
    comments       TEXT,
    written_by     INT,
    being_reviewed INT                        NOT NULL,
    flagged_by     INT DEFAULT NULL,
    # When the written by is null the program can just say anon/ when someone wants to review anon written_by can be anon
    CONSTRAINT FOREIGN KEY (written_by)
        REFERENCES Attendees (attendee_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT FOREIGN KEY (being_reviewed)
        REFERENCES Organizer (organizer_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (flagged_by)
        REFERENCES Admin (admin_id) ON UPDATE CASCADE ON DELETE NO ACTION,
    INDEX (rating, written_by, being_reviewed,flagged_by)
);


CREATE TABLE SponsorReviews
(
    sponsor_review_id INT PRIMARY KEY AUTO_INCREMENT,
    rating            ENUM ('1','2','3','4','5') NOT NULL,
    comments          TEXT,
    written_by        INT,                                 -- organizer id
    being_reviewed    INT                        NOT NULL, -- the id of the sponsor
    flagged_by        INT DEFAULT NULL,
    # When the written by is null the program can just say anon/ when someone wants to review anon written_by can be anon
    CONSTRAINT FOREIGN KEY (written_by)
        REFERENCES Organizer (organizer_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT FOREIGN KEY (being_reviewed)
        REFERENCES Sponsors (sponsor_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (flagged_by)
        REFERENCES Admin (admin_id) ON UPDATE CASCADE ON DELETE NO ACTION,
    INDEX (rating, written_by, being_reviewed, flagged_by)
);

CREATE TABLE ChatRooms
(
    organizer_id INT NOT NULL,
    sponsor_id   INT NOT NULL,
    PRIMARY KEY (organizer_id, sponsor_id),
    CONSTRAINT FOREIGN KEY (organizer_id)
        REFERENCES Organizer (organizer_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (sponsor_id)
        REFERENCES Sponsors (sponsor_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Messages
(
    message_id   INT AUTO_INCREMENT PRIMARY KEY,
    content      TEXT                          NOT NULL,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    organizer_id INT                           NOT NULL,
    sponsor_id   INT                           NOT NULL,
    sender       enum ('sponsor', 'organizer') NOT NULL,
    CONSTRAINT FOREIGN KEY (organizer_id, sponsor_id)
        REFERENCES ChatRooms (organizer_id, sponsor_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Event_Attendance
(
    event_id    INT NOT NULL,
    attendee_id INT NOT NULL,
    PRIMARY KEY (event_id, attendee_id),
    CONSTRAINT FOREIGN KEY (event_id)
        REFERENCES Events (event_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (attendee_id)
        REFERENCES Attendees (attendee_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Event_Bookmarks
(
    event_id    INT NOT NULL,
    attendee_id INT NOT NULL,
    PRIMARY KEY (event_id, attendee_id),
    CONSTRAINT FOREIGN KEY (event_id)
        REFERENCES Events (event_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (attendee_id)
        REFERENCES Attendees (attendee_id) ON UPDATE CASCADE ON DELETE CASCADE
);

USE GoOutside;

INSERT INTO Admin (first, last, email, phone)
VALUES
('Alice', 'Smith', 'alice.smith@example.com', '12345678901'),
('Bob', 'Johnson', 'bob.johnson@example.com', '12345678902');

INSERT INTO Event_Categories (name, description)
VALUES
('Music', 'Events related to music and concerts'),
('Sports', 'Sports-related events and activities'),
('Technology', 'Tech conferences and meetups'),
('Art', 'Art exhibitions and workshops');

INSERT INTO Attendees (first_name, last_name, email, phone, fav_category)
VALUES
('John', 'Doe', 'john.doe@example.com', '12345678903', 'Music'),
('Jane', 'Doe', 'jane.doe@example.com', '12345678904', 'Art');

INSERT INTO Organizer (name, email, phone, bio, approved_by)
VALUES
('Eventify', 'contact@eventify.com', '12345678905', 'We organize amazing events!', 1),
('TechMeet', 'info@techmeet.com', '12345678906', 'Connecting tech enthusiasts.', 2);

INSERT INTO Sponsors (name, email, phone, approved_by)
VALUES
('SponsorCo', 'sponsorco@example.com', '12345678907', 1),
('EventBoost', 'eventboost@example.com', '12345678908', 2);

INSERT INTO Events (name, cost, start_time, end_time, location, description, category_name, organized_by, sponsor_by, approved_by, sponsor_cost)
VALUES
('Music Fest', 50.00, '2025-05-01 18:00:00', '2025-05-01 23:00:00', 'Central Park', 'A night of great music.', 'Music', 1, NULL, 1, 6000),
('Tech Conference', 100.00, '2025-06-15 09:00:00', '2025-06-15 17:00:00', 'Convention Center', 'Explore the latest in tech.', 'Technology', 2, 2, 2, 500);

INSERT INTO Event_Announcement (event_id, description)
VALUES
(1, 'Don’t miss the biggest music event of the year!'),
(2, 'Join us for an exciting day of tech talks and networking.');

INSERT INTO Admin_Announcement (event_id, description)
VALUES
(1, 'Admin-approved: Music Fest is happening soon!'),
(2, 'Admin-approved: Tech Conference is now live!');

INSERT INTO Stats (clicks, impressions, event_id)
VALUES
(100, 500, 1),
(200, 1000, 2);

INSERT INTO OrganizerReviews (rating, comments, written_by, being_reviewed, flagged_by)
VALUES
('5', 'Great organizer!', 1, 1, NULL),
('4', 'Good communication.', 2, 2, 1);

INSERT INTO SponsorReviews (rating, comments, written_by, being_reviewed, flagged_by)
VALUES
('5', 'Excellent sponsor!', 1, 1, 2),
('3', 'Could improve support.', 2, 2, NULL);

INSERT INTO ChatRooms (organizer_id, sponsor_id)
VALUES
(1, 1),
(2, 2);

INSERT INTO Messages (content, organizer_id, sponsor_id, sender)
VALUES
('Looking forward to the event!', 1, 1, 'organizer'),
('We’re excited to sponsor this!', 1, 1, 'sponsor');

INSERT INTO Event_Attendance (event_id, attendee_id)
VALUES
(1, 1),
(2, 2);

INSERT INTO Event_Bookmarks (event_id, attendee_id)
VALUES
(1, 2),
(2, 1);


-- Persona 1: Attendee CRUD statements
-- Attendee - 1.1
SELECT * FROM Events
WHERE category_name = 'Music';

-- Attendee - 1.2
SELECT * FROM Event_Bookmarks
WHERE attendee_id = 1;

-- Attendee - 1.3
INSERT INTO Event_Attendance(event_id, attendee_id)
VALUES (2, 1);

-- Attendee - 1.4
INSERT INTO OrganizerReviews(org_review_id, rating, comments, written_by, being_reviewed, flagged_by)
VALUES (3, 2, 'Event was boring', 1, 2, NULL);

-- Attendee - 1.5
SELECT * FROM Events
WHERE category_name = 'Music';

-- Attendee - 1.6
SELECT e.name, e.start_time, e.end_time
FROM Events e;


-- Persona 2: Organizer CRUD statements
-- Organizer - 2.1
SELECT a.fav_category, COUNT(a.attendee_id) AS audience_count
FROM Attendees a
JOIN Event_Attendance ea ON a.attendee_id = ea.attendee_id
JOIN Events e ON ea.event_id = e.event_id
WHERE e.organized_by = 1 -- put organizer id here
GROUP BY a.fav_category
ORDER BY audience_count DESC;

-- Organizer - 2.2
SELECT e.name AS event_name, s.clicks, s.impressions, (s.clicks / s.impressions * 100) AS click_rate
FROM Events e
JOIN Stats s ON e.event_id = s.event_id
WHERE e.organized_by = 1; -- put organizer id here


-- Organizer - 2.3
INSERT INTO SponsorReviews(being_reviewed, rating, comments)
VALUES (1, 4, 'Great staff and support!'); -- put sponsor id here


-- Organizer - 2.4
INSERT INTO Event_Announcement (event_id, description)
VALUES (1, 'The event has been rescheduled to next monday.');

-- Organizer - 2.5
SELECT s.name AS sponsor_name, AVG(sr.rating) AS avg_rating
FROM Sponsors s
JOIN SponsorReviews sr ON s.sponsor_id = sr.being_reviewed
GROUP BY s.sponsor_id
HAVING AVG(sr.rating) >= 4
ORDER BY avg_rating DESC;

-- Organizer - 2.6
SELECT e.name AS event_name,
       COUNT(ea.attendee_id) AS total_attendees,
       COUNT(eb.attendee_id) AS total_bookmarks
FROM Events e
LEFT JOIN Event_Attendance ea ON e.event_id = ea.event_id
LEFT JOIN Event_Bookmarks eb ON e.event_id = eb.event_id
WHERE e.organized_by = 1 -- put organizer id here
GROUP BY e.event_id
ORDER BY total_attendees DESC, total_bookmarks DESC;

-- Persona 3: Sponsor CRUD statements
-- Sponsor - 3.1
SELECT e.name, count(eb.attendee_id) as 'Num Bookmarked'
FROM Event_Bookmarks eb JOIN `Events` e ON e.event_id = eb.event_id
GROUP BY eb.event_id
HAVING count(eb.attendee_id > 0)
ORDER BY count(attendee_id) DESC

-- Sponsor - 3.2
SELECT o.name, avg(orgRev.rating) as 'Average Rating'
FROM Organizer o JOIN OrganizerReviews orgRev ON orgRev.being_reviewed = o.organizer_id
GROUP BY orgRev.being_reviewed
ORDER BY avg(orgRev.rating) DESC

-- Sponsor - 3.3
SELECT e.name, o.email, o.phone
FROM Events e JOIN Organizer o ON e.organized_by = organizer_id
ORDER BY e.name ASC

-- Sponsor - 3.4
UPDATE Events e
SET e.sponsor_by = 1
WHERE event_id = 1

-- Sponsor 3.5
INSERT INTO Messages (content, organizer_id, sponsor_id, sender)
VALUES ('Excited to work together!', 1, 1, 'sponsor');

-- Sponsor - 3.6
SELECT e.name, es.clicks, es.impressions
FROM Events e JOIN Stats es ON e.event_id = es.event_id
ORDER BY es.clicks DESC


-- Persona 4: Admin CRUD statements
-- Admin - 4.1
INSERT INTO Events (name, cost, start_time, end_time, location, description, category_name, organized_by, sponsor_by, approved_by)
VALUES
('Dance Rave', 75.00, '2025-07-20 10:00:00', '2025-07-20 16:00:00', 'Downtown Exhibition Hall', 'Discover the best in health, wellness, and fitness.', 'Music', 1, 1, 1);

-- Admin - 4.2
SELECT * FROM SponsorReviews
WHERE flagged_by is NULL;

-- Admin - 4.3
INSERT INTO Event_Categories(name, description)
VALUES ('Outdoors', 'related to events happening outdoors');

-- Admin - 4.4
SELECT * FROM SponsorReviews;

-- Admin - 4.5
SELECT * FROM Stats;

-- Admin - 4.6
SELECT * from Admin_Announcement;
INSERT INTO Admin_Announcement(admin_announcement_id, event_id, description)
VALUES (3, 3, 'Location has changed for the Dance Rave');
