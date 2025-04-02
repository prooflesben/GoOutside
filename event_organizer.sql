USE GoOutside;

-- As an Event Organizer, I want to be able to promote my event by paying for targeted advertisements, so that I can reach the right audience and increase attendance.
SELECT a.fav_category, COUNT(a.attendee_id) AS audience_count
FROM Attendees a
JOIN Event_Attendance ea ON a.attendee_id = ea.attendee_id
JOIN Events e ON ea.event_id = e.event_id
WHERE e.organized_by = 1 -- put organizer id here
GROUP BY a.fav_category
ORDER BY audience_count DESC;

-- As an Event Organizer, I want to have a feature that matches my event with potential sponsors, so that I can secure funding and advertisement opportunities efficiently.
SELECT e.name AS event_name, s.clicks, s.impressions, (s.clicks / s.impressions * 100) AS click_rate
FROM Events e
JOIN Stats s ON e.event_id = s.event_id
WHERE e.organized_by = 1; -- put organizer id here


-- As an Event Organizer, I want to be able to rate businesses I’ve worked with, so that other organizers can make informed decisions and businesses can improve their services.
INSERT INTO SponsorReviews(being_reviewed, rating, comments)
VALUES (1, 4, 'Great staff and support!'); -- put sponsor id here


-- As an Event Organizer, I want to be able to send out event updates to attendees, so that I can keep them informed about schedule changes, important notices, and other key information.
INSERT INTO Event_Announcement (event_id, description)
VALUES (1, 'The event has been rescheduled to next monday.');


-- As an Event Organizer, I want to be able to work with businesses that are highly rated.
SELECT s.name AS sponsor_name, AVG(sr.rating) AS avg_rating
FROM Sponsors s
JOIN SponsorReviews sr ON s.sponsor_id = sr.being_reviewed
GROUP BY s.sponsor_id
HAVING AVG(sr.rating) >= 4
ORDER BY avg_rating DESC;

-- As an Event Organizer, I want to be able to find events organized by me that are the highest engagement
SELECT e.name AS event_name,
       COUNT(ea.attendee_id) AS total_attendees,
       COUNT(eb.attendee_id) AS total_bookmarks
FROM Events e
LEFT JOIN Event_Attendance ea ON e.event_id = ea.event_id
LEFT JOIN Event_Bookmarks eb ON e.event_id = eb.event_id
WHERE e.organized_by = 1 -- put organizer id here
GROUP BY e.event_id
ORDER BY total_attendees DESC, total_bookmarks DESC;


