-- Active: 1701510427416@@127.0.0.1@3306@puson_db
CREATE DATABASE puson_db;
USE puson_db;

CREATE TABLE PUSKESMAS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE POSYANDU (
    id INT AUTO_INCREMENT PRIMARY KEY,
    puskesmas_id INT,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (puskesmas_id) REFERENCES PUSKESMAS(id) ON DELETE CASCADE
);

CREATE TABLE ROLE (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE USER (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    role_id INT,
    posyandu_id INT,
    reset_token VARCHAR(255),
    reset_token_expiry DATETIME;
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES ROLE(id) ON DELETE SET NULL,
    FOREIGN KEY (posyandu_id) REFERENCES POSYANDU(id) ON DELETE SET NULL
);


CREATE TABLE CHILD (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('male', 'female') NOT NULL,
    weight FLOAT,
    height FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES USER(id) ON DELETE CASCADE
);

CREATE TABLE DATA_CHECKUP (
    id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT,
    user_id INT,
    checkup_date DATE NOT NULL,
    weight FLOAT,
    height FLOAT,
    head_circumference FLOAT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES CHILD(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES USER(id) ON DELETE CASCADE
);

CREATE TABLE STUNTING (
    id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT,
    stunting_status ENUM('normal', 'stunted') NOT NULL,
    date_assessed DATE NOT NULL,
    assessment_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES CHILD(id) ON DELETE CASCADE
);

CREATE TABLE REFRESH_TOKENS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    token VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES USER(id) ON DELETE CASCADE
);


-- Data Dummy

-- Insert default roles into the ROLE table
INSERT INTO ROLE (id, role_name) VALUES 
(1, 'superAdmin'),
(2, 'adminPuskesmas'),
(3, 'adminPosyandu'),
(4, 'parent');

-- Insert sample data into the POSYANDU table
INSERT INTO POSYANDU (id, name, address) VALUES 
(1, 'Posyandu A', '123 Main St, Jakarta'),
(2, 'Posyandu B', '456 Elm St, Jakarta'),
(3, 'Posyandu C', '789 Oak St, Jakarta'),
(4, 'Posyandu D', '101 Pine St, Jakarta'),
(5, 'Posyandu E', '202 Maple St, Jakarta');
