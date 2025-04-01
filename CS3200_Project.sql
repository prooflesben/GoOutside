-- SQLBook: Code
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
    cost          DECIMAL(10, 2) UNSIGNED,
    start_time    DATETIME     NOT NULL,
    end_time      DATETIME     NOT NULL,
    location      varchar(100) NOT NULL,
    description   TEXT NOT NULL,
    category_name VARCHAR(20)  NOT NULL,
    organized_by  INT          NOT NULL,
    sponsor_by    INT          NOT NULL,
    approved_by   INT          NOT NULL,
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
        REFERENCES Attendees (attendee_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT FOREIGN KEY (being_reviewed)
        REFERENCES Organizer (organizer_id) ON UPDATE CASCADE ON DELETE CASCADE,
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