-- ICS 370 Restaurant Database

INSERT INTO Inquiry (inquiryID, iTime, iDate, storeID)
VALUES
('Q101', '20:30', '2026-09-20', 'S101'),
('Q102', '10:30', '2026-10-17', 'S102'),
('Q103', '14:00', '2026-06-24', 'S103'),
('Q104', '11:15', '2026-10-05', 'S102');

-- InquiryDescription insert statements
-- NULL for phones for now

INSERT INTO InquiryDescription (inquiryID, phoneNumber, firstName, lastName, IEmail, iDescription)
VALUES
('Q101', NULL, 'Jeong', 'Alayah', 'jeongalayah@hotmail.com', 'Wedding, requested 12/21/2026, 101 Church St, Minneapolis, MN'),
('Q102', NULL, 'Miguel', 'Santiago', 'msantiago@hotmail.com', 'Funeral, requested 11/23/2026, 99 Example St, Saint Paul, MN'),
('Q103', NULL, 'Abbey', 'Orna', 'aorna19@yahoo.com', 'General, requested 6/24/2026, 100 Grand Park, Edina, MN'),
('Q104', NULL, 'Shawnda', 'Ruuben', 'shanda_ruuben@generalmills.com', 'Business, Golden Valley, MN');

-- InquiryEvents insert statements

INSERT INTO InquiryEvents (eventID, inquiryID)
VALUES
('E101', 'Q101'),
('E103', 'Q102'),
('E102', 'Q103');