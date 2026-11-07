-- ICS 370 Restaurant Management
-- Menu Data
-- Recipe INSERT Statements
-- Based on the team's data

INSERT INTO Recipe (recipeID, recipeName)
VALUES
('R101', 'Chicken Tortellini with Alfredo'),
('R102', 'Chicken Alfredo'),
('R103', 'Spaghetti & Meatballs'),
('R104', 'Chicken Parmesan'),
('R105', 'Breadsticks'),
('R106', 'Roasted Ravioli'),
('R107', 'Strawberry cream cake'),
('R108', 'Spinach Artichoke Dip'),
('R109', NULL),
('R110', NULL),
('R111', 'Omelet'),
('R112', 'Pancakes'),
('R113', 'Red Wine'),
('R114', 'Ice Tea'),
('R115', 'fries'),
('R116', 'Margherita Pizza'),
('R117', 'Pumpkin Soup'),
('R118', 'Meatball Sub'),
('R119', 'Pumpkin Butter Cheesecake');

-- Item INSERT Statements
-- Items are shared between Menu and Inventory

INSERT INTO Item (itemID, itemName, allergyInfo)
VALUES
('I101', 'chairs', NULL),
('I102', 'tomato', 'tomato'),
('I103', 'chicken breast', 'chicken');

-- Menu INSERT Statements
-- Categories reference MenuCategory IDs

INSERT INTO Menu (menuID, category, servingSize)
VALUES
('M101', 3, NULL),
('M102', 3, NULL),
('M103', 3, NULL),
('M104', 2, NULL),
('M105', 5, NULL),
('M106', 5, '9'),
('M107', 4, '10'),
('M108', 5, NULL),
('M111', 1, '2'),
('M112', 1, '10'),
('M113', 6, '1'),
('M114', 6, '1'),
('M115', 7, '1'),
('M116', 8, NULL),
('M117', 9, '10'),
('M118', 2, '1'),
('M119', 8, NULL);
