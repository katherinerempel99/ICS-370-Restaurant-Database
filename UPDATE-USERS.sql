DROP TABLE if exists StoreStaff
DROP TABLE if exists user_rank
DROP TABLE if exists Users

CREATE table StoreStaff(
    userID int NOT NULL,
    storeID varchar(8) NOT NULL,
    Foreign KEY(userID) REFERENCES auth_user(id),
    Foreign Key(storeID) REFERENCES Store(storeID)
);

INSERT INTO StoreStaff (userID, storeID)
VALUES
('2', 'S101'),
('3', 'S101')
;
