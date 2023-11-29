--check host,user,password and database according to your system
--Create a database
Create database daksh(database name)
--creat the table
CREATE TABLE acc (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    account_no VARCHAR(20) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL,
    pin VARCHAR(4) NOT NULL
);


