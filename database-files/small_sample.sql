USE GoOutside;

-- Admin
INSERT INTO Admin (first, last, email, phone) VALUES
('Alice', 'Smith', 'alice.smith@gooutside.com', '5551111111'),
('Bob', 'Johnson', 'bob.johnson@gooutside.com', '5552222222'),
('Carol', 'Williams', 'carol.williams@gooutside.com', '5553333333'),
('David', 'Brown', 'david.brown@gooutside.com', '5554444444'),
('Eva', 'Jones', 'eva.jones@gooutside.com', '5555555555'),
('Frank', 'Garcia', 'frank.garcia@gooutside.com', '5556666666'),
('Grace', 'Martinez', 'grace.martinez@gooutside.com', '5557777777'),
('Henry', 'Lee', 'henry.lee@gooutside.com', '5558888888'),
('Ivy', 'Walker', 'ivy.walker@gooutside.com', '5559999999'),
('Jack', 'Hall', 'jack.hall@gooutside.com', '5551010101');

-- Event_Categories
INSERT INTO Event_Categories (name, description) VALUES
('Hiking', 'Outdoor hiking events'),
('Yoga', 'Yoga and wellness sessions'),
('Concert', 'Live music events'),
('Workshop', 'Educational workshops'),
('Festival', 'Seasonal festivals'),
('Sports', 'Team and solo sports'),
('Art', 'Art exhibitions'),
('Food', 'Food tasting events'),
('Tech', 'Tech meetups'),
('Charity', 'Charity fundraisers');

-- Attendees
INSERT INTO Attendees (first_name, last_name, email, phone, fav_category) VALUES
('Liam', 'Nguyen', 'liam.nguyen@email.com', '5552011001', 'Hiking'),
('Mia', 'Kim', 'mia.kim@email.com', '5552011002', 'Yoga'),
('Noah', 'Chen', 'noah.chen@email.com', '5552011003', 'Concert'),
('Olivia', 'Patel', 'olivia.patel@email.com', '5552011004', 'Workshop'),
('Paul', 'Clark', 'paul.clark@email.com', '5552011005', 'Festival'),
('Quinn', 'Lewis', 'quinn.lewis@email.com', '5552011006', 'Sports'),
('Ruby', 'Young', 'ruby.young@email.com', '5552011007', 'Art'),
('Sophie', 'King', 'sophie.king@email.com', '5552011008', 'Food'),
('Tom', 'Scott', 'tom.scott@email.com', '5552011009', 'Tech'),
('Uma', 'Green', 'uma.green@email.com', '5552011010', 'Charity');

-- Organizer (approved_by references Admin.admin_id 1-10)
INSERT INTO Organizer (name, email, phone, bio, approved_by) VALUES
('HikeMasters', 'hike@org.com', '5553011001', 'Expert hiking organizers', 1),
('ZenYoga', 'zenyoga@org.com', '5553011002', 'Yoga for all levels', 2),
('LiveBeats', 'livebeats@org.com', '5553011003', 'Concert event pros', 3),
('SkillUp', 'skillup@org.com', '5553011004', 'Workshop facilitators', 4),
('Festify', 'festify@org.com', '5553011005', 'Festival planners', 5),
('Sportify', 'sportify@org.com', '5553011006', 'Sports event managers', 6),
('Artify', 'artify@org.com', '5553011007', 'Art event curators', 7),
('Foodies', 'foodies@org.com', '5553011008', 'Food event experts', 8),
('Techies', 'techies@org.com', '5553011009', 'Tech meetup hosts', 9),
('CharityWorks', 'charityworks@org.com', '5553011010', 'Charity event leaders', 10);

-- Sponsors (approved_by references Admin.admin_id 1-10)
INSERT INTO Sponsors (name, email, phone, approved_by) VALUES
('PeakGear', 'peakgear@sponsor.com', '5554011001', 1),
('MatZen', 'matzen@sponsor.com', '5554011002', 2),
('SoundWave', 'soundwave@sponsor.com', '5554011003', 3),
('SkillShare', 'skillshare@sponsor.com', '5554011004', 4),
('FestCorp', 'festcorp@sponsor.com', '5554011005', 5),
('SportCo', 'sportco@sponsor.com', '5554011006', 6),
('ArtHouse', 'arthouse@sponsor.com', '5554011007', 7),
('FoodInc', 'foodinc@sponsor.com', '5554011008', 8),
('TechPlus', 'techplus@sponsor.com', '5554011009', 9),
('CharityAid', 'charityaid@sponsor.com', '5554011010', 10);

-- Events (organized_by: 1-10, category_name: from Event_Categories, sponsor_by: 1-10, approved_by: 1-10)
INSERT INTO Events (name, cost, start_time, end_time, location, description, category_name, organized_by, sponsor_by, approved_by, sponsor_cost) VALUES
('Spring Hike', 20.00, '2025-04-20 09:00:00', '2025-04-20 12:00:00', 'Mountain Trail', 'Enjoy spring hiking.', 'Hiking', 1, 1, 1, 500),
('Sunrise Yoga', 15.00, '2025-04-21 06:30:00', '2025-04-21 08:00:00', 'City Park', 'Morning yoga session.', 'Yoga', 2, 2, 2, 300),
('Rock Fest', 50.00, '2025-04-22 18:00:00', '2025-04-22 22:00:00', 'Open Arena', 'Live rock music.', 'Concert', 3, 3, 3, 1000),
('Coding 101', 0.00, '2025-04-23 14:00:00', '2025-04-23 16:00:00', 'Tech Hub', 'Beginner coding workshop.', 'Workshop', 4, NULL, 4, 0),
('Spring Fest', 10.00, '2025-04-24 10:00:00', '2025-04-24 18:00:00', 'Town Square', 'Celebrate spring.', 'Festival', 5, 5, 5, 200),
('Soccer Cup', 25.00, '2025-04-25 10:00:00', '2025-04-25 16:00:00', 'Sports Field', 'Soccer tournament.', 'Sports', 6, NULL, 6, 600),
('Art Expo', 12.00, '2025-04-26 11:00:00', '2025-04-26 17:00:00', 'Art Gallery', 'Modern art displays.', 'Art', 7, 7, 7, 150),
('Food Carnival', 8.00, '2025-04-27 12:00:00', '2025-04-27 20:00:00', 'Food Street', 'Food tasting.', 'Food', 8, 8, 8, 400),
('Tech Meetup', 0.00, '2025-04-28 17:00:00', '2025-04-28 19:00:00', 'Innovation Lab', 'Tech networking.', 'Tech', 9, 9, 9, 0),
('Charity Run', 30.00, '2025-04-29 08:00:00', '2025-04-29 12:00:00', 'River Park', 'Run for charity.', 'Charity', 10, 10, 10, 700);

-- Event_Announcement (event_id: 1-10)
INSERT INTO Event_Announcement (event_id, description) VALUES
(1, 'Trail conditions are excellent!'),
(2, 'Bring your own mat.'),
(3, 'Gates open at 5:30pm.'),
(4, 'Laptops provided.'),
(5, 'Don’t miss the parade at noon!'),
(6, 'Teams must check in by 9:30am.'),
(7, 'Artist Q&A at 2pm.'),
(8, 'Vegetarian options available.'),
(9, 'Keynote at 5:30pm.'),
(10, 'Water stations every mile.');

-- Admin_Announcement (event_id: 1-10)
INSERT INTO Admin_Announcement (event_id, description) VALUES
(1, 'Parking is limited.'),
(2, 'Event will proceed rain or shine.'),
(3, 'Security checks at entrance.'),
(4, 'WiFi available throughout venue.'),
(5, 'Lost & found at info booth.'),
(6, 'First aid tent near main gate.'),
(7, 'No flash photography allowed.'),
(8, 'Pets must be leashed.'),
(9, 'Charging stations available.'),
(10, 'Donations accepted onsite.');

-- Stats (event_id: 1-10)
INSERT INTO Stats (event_id, clicks, impressions) VALUES
(1, 120, 300),
(2, 90, 210),
(3, 250, 700),
(4, 60, 100),
(5, 180, 400),
(6, 140, 350),
(7, 110, 200),
(8, 170, 380),
(9, 200, 600),
(10, 80, 150);

-- OrganizerReviews (written_by: Attendees 1-10, being_reviewed: Organizer 1-10, flagged_by: Admin 1-5 or NULL)
INSERT INTO OrganizerReviews (rating, comments, written_by, being_reviewed, flagged_by) VALUES
('5', 'Fantastic event!', 1, 1, NULL),
('4', 'Very well organized.', 2, 2, 1),
('3', 'Good, but could be better.', 3, 3, NULL),
('5', 'Loved it!', 4, 4, NULL),
('2', 'Not as expected.', 5, 5, 2),
('4', 'Enjoyed the activities.', 6, 6, NULL),
('3', 'Average experience.', 7, 7, NULL),
('5', 'Superb!', 8, 8, 3),
('4', 'Would attend again.', 9, 9, NULL),
('5', 'Highly recommend.', 10, 10, NULL);

-- SponsorReviews (written_by: Organizer 1-10, being_reviewed: Sponsor 1-10, flagged_by: Admin 1-5 or NULL)
INSERT INTO SponsorReviews (rating, comments, written_by, being_reviewed, flagged_by) VALUES
('5', 'Great support!', 1, 1, NULL),
('4', 'Helpful sponsor.', 2, 2, 1),
('3', 'Average experience.', 3, 3, NULL),
('5', 'Very generous.', 4, 4, NULL),
('2', 'Could be better.', 5, 5, 2),
('4', 'Responsive team.', 6, 6, NULL),
('3', 'Met expectations.', 7, 7, NULL),
('5', 'Excellent!', 8, 8, 3),
('4', 'Would partner again.', 9, 9, NULL),
('5', 'Outstanding.', 10, 10, NULL);

-- ChatRooms (organizer_id: 1-10, sponsor_id: 1-10)
INSERT INTO ChatRooms (organizer_id, sponsor_id) VALUES
(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10);

-- Messages (organizer_id, sponsor_id must match ChatRooms)
INSERT INTO Messages (content, organizer_id, sponsor_id, sender) VALUES
('Hello, looking forward to working with you!', 1, 1, 'organizer'),
('Thank you for sponsoring.', 2, 2, 'organizer'),
('Let us know your requirements.', 3, 3, 'sponsor'),
('Can we get banners for the event?', 4, 4, 'organizer'),
('Sure, we will send them.', 5, 5, 'sponsor'),
('Do you need volunteers?', 6, 6, 'organizer'),
('Yes, we can provide some.', 7, 7, 'sponsor'),
('Please share your logo.', 8, 8, 'organizer'),
('Logo sent, check your email.', 9, 9, 'sponsor'),
('Looking forward to the event!', 10, 10, 'organizer');

-- Event_Attendance (event_id: 1-10, attendee_id: 1-10)
INSERT INTO Event_Attendance (event_id, attendee_id) VALUES
(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10);

-- Event_Bookmarks (event_id: 1-10, attendee_id: 10-1)
INSERT INTO Event_Bookmarks (event_id, attendee_id) VALUES
(1,10),(2,9),(3,8),(4,7),(5,6),(6,5),(7,4),(8,3),(9,2),(10,1);
