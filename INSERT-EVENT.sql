-- ICS 370 Restaurant Database
-- Event insert statements
-- eTime is the start time (column is time, Excel had ranges like 10AM-10PM)
-- storeID NULL where Excel was blank, E103 S00102 = S102

INSERT INTO Event (eventID, eventName, eDate, eTime, category, storeID)
VALUES
('E101', 'J. Alayah''s Wedding', '2026-12-21', '10:00', 'Wedding', 'S101'),
('E102', 'A. Orna Reunion', '2026-06-24', '12:00', 'Business', 'S103'),
('E103', 'Santiago Family Funeral', '2026-11-23', '11:00', 'Funeral', 'S102');

-- EventDescription insert statements
-- E102 location from Abbey Orna's inquiry (same date)

INSERT INTO EventDescription (eventID, eDescription, eventName, eLocation)
VALUES
('E101', 'Wedding Catering', 'J. Alayah''s Wedding', '101 Church St, Minneapolis, MN'),
('E102', 'Reunion Catering', 'A. Orna Reunion', '100 Grand Park, Edina, MN'),
('E103', 'Funeral Private Party', 'Santiago Family Funeral', '99 Example St, Saint Paul, MN');

-- EventItems insert statements
-- I00101 = chairs, I00102 = tomato, I00103 = chicken breast

INSERT INTO EventItems (eventID, itemID, quantityNeeded)
VALUES
('E101', 'I00101', 50),
('E101', 'I00102', 20),
('E101', 'I00103', 40),
('E102', 'I00101', 30),
('E102', 'I00102', 10),
('E102', 'I00103', 15),
('E103', 'I00101', 40),
('E103', 'I00103', 20);