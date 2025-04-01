USE GoOutside;

-- Populate Admin table
INSERT INTO Admin (first, last, email, phone)
VALUES
('Alice', 'Smith', 'alice.smith@example.com', '12345678901'),
('Bob', 'Johnson', 'bob.johnson@example.com', '12345678902');

-- Populate Event_Categories table
INSERT INTO Event_Categories (name, description)
VALUES
('Music', 'Events related to music and concerts'),
('Sports', 'Sports-related events and activities'),
('Technology', 'Tech conferences and meetups'),
('Art', 'Art exhibitions and workshops');

-- Populate Attendees table
INSERT INTO Attendees (first_name, last_name, email, phone, fav_category)
VALUES
('John', 'Doe', 'john.doe@example.com', '12345678903', 'Music'),
('Jane', 'Doe', 'jane.doe@example.com', '12345678904', 'Art');

-- Populate Organizer table
INSERT INTO Organizer (name, email, phone, bio, approved_by)
VALUES
('Eventify', 'contact@eventify.com', '12345678905', 'We organize amazing events!', 1),
('TechMeet', 'info@techmeet.com', '12345678906', 'Connecting tech enthusiasts.', 2);

-- Populate Sponsors table
INSERT INTO Sponsors (name, email, phone, approved_by)
VALUES
('SponsorCo', 'sponsorco@example.com', '12345678907', 1),
('EventBoost', 'eventboost@example.com', '12345678908', 2);

-- Populate Events table
INSERT INTO Events (name, cost, start_time, end_time, location, description, category_name, organized_by, sponsor_by, approved_by)
VALUES
('Music Fest', 50.00, '2025-05-01 18:00:00', '2025-05-01 23:00:00', 'Central Park', 'A night of great music.', 'Music', 1, 1, 1),
('Tech Conference', 100.00, '2025-06-15 09:00:00', '2025-06-15 17:00:00', 'Convention Center', 'Explore the latest in tech.', 'Technology', 2, 2, 2);

-- Populate Event_Announcement table
INSERT INTO Event_Announcement (event_id, description)
VALUES
(1, 'Don’t miss the biggest music event of the year!'),
(2, 'Join us for an exciting day of tech talks and networking.');

-- Populate Admin_Announcement table
INSERT INTO Admin_Announcement (event_id, description)
VALUES
(1, 'Admin-approved: Music Fest is happening soon!'),
(2, 'Admin-approved: Tech Conference is now live!');

-- Populate Stats table
INSERT INTO Stats (clicks, impressions, event_id)
VALUES
(100, 500, 1),
(200, 1000, 2);

-- Populate OrganizerReviews table
INSERT INTO OrganizerReviews (rating, comments, written_by, being_reviewed, flagged_by)
VALUES
('5', 'Great organizer!', 1, 1, NULL),
('4', 'Good communication.', 2, 2, NULL);

-- Populate SponsorReviews table
INSERT INTO SponsorReviews (rating, comments, written_by, being_reviewed, flagged_by)
VALUES
('5', 'Excellent sponsor!', 1, 1, NULL),
('3', 'Could improve support.', 2, 2, NULL);

-- Populate ChatRooms table
INSERT INTO ChatRooms (organizer_id, sponsor_id)
VALUES
(1, 1),
(2, 2);

-- Populate Messages table
INSERT INTO Messages (content, organizer_id, sponsor_id, sender)
VALUES
('Looking forward to the event!', 1, 1, 'organizer'),
('We’re excited to sponsor this!', 1, 1, 'sponsor');

-- Populate Event_Attendance table
INSERT INTO Event_Attendance (event_id, attendee_id)
VALUES
(1, 1),
(2, 2);

-- Populate Event_Bookmarks table
INSERT INTO Event_Bookmarks (event_id, attendee_id)
VALUES
(1, 2),
(2, 1);