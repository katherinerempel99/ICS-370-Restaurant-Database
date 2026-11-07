-- ICS 370 Restaurant Management
-- Store insert statements
-- Store ID's use S101, excell had S00101

INSERT INTO Store (storeID, address, hours, phone, storeEmail)
VALUES
('S101', '123 Apple Street', '8 AM - 10 PM', NULL, 'applest@store.com'),
('S102', '456 17th Lane', '9 AM - 5 PM', NULL, '17th@store.com'),
('S103', '789 Turtle Dr', '11 AM - 11 PM', NULL, 'turtledr@store.com');


-- Users INSERT Statements
-- authLevel uses user_rank IDs: 1 Staff, 2 Manager, 3 Owner

INSERT INTO Users (userID, password, authLevel, firstName, lastName, storeID)
VALUES
('U101', 'P101', 3, 'James', 'Bond', 'S101'),
('U102', 'P102', 2, 'Muhammed', 'Ali', 'S101'),
('U103', 'P103', 1, 'Rowan', 'Palmer', 'S101'),
('U104', 'P104', 1, 'Sammy-Jo', 'Murray', 'S101'),
('U105', 'P105', 3, 'Yeon-Jae', 'Kim', 'S102'),
('U106', 'P106', 2, 'Sandro', 'Pesce', 'S102'),
('U107', 'P107', 1, 'Hakan', 'Bodur', 'S102'),
('U108', 'P108', 1, 'Emile', 'Grondin', 'S102'),
('U109', 'P109', 3, 'Sigrid', 'Hoek', 'S103'),
('U110', 'P110', 2, 'Naomi', 'Yoshizaki', 'S103'),
('U111', 'P111', 1, 'Hong-Yi', 'Lang', 'S103'),
('U112', 'P112', 1, 'Grigori', 'Lyubochka', 'S103'),
('U113', 'P113', 1, 'Daniela', 'Charitou', 'S103');


-- StoreStaff INSERT Statements


INSERT INTO StoreStaff (userID, storeID)
VALUES
('U101', 'S101'),
('U102', 'S101'),
('U103', 'S101'),
('U104', 'S101'),
('U105', 'S102'),
('U106', 'S102'),
('U107', 'S102'),
('U108', 'S102'),
('U109', 'S103'),
('U110', 'S103'),
('U111', 'S103'),
('U112', 'S103'),
('U113', 'S103');
