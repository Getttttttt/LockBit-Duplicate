CREATE DATABASE LockBit;
USE LockBit;

CREATE TABLE Record (
    id VARCHAR(255) PRIMARY KEY,
    statement INT
);

CREATE TABLE Files (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Content BLOB
);

CREATE TABLE Account (
    StudentID INT PRIMARY KEY,
    StudentPassword CHAR(50),
);

CREATE TRIGGER update_statement
AFTER UPDATE ON Record
FOR EACH ROW
BEGIN
    IF NEW.statement = 0 THEN
        UPDATE Record SET statement = 1 WHERE id = NEW.id;
    END IF;
END;
