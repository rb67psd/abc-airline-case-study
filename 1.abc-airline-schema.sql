CREATE DATABASE abc;

USE abc;

CREATE TABLE members (
    ffp_number VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE,
    nationality VARCHAR(50),
    passport_number VARCHAR(20),
    verified TINYINT DEFAULT 0 -- 0 for Unverified, 1 for Verified
);

CREATE TABLE member_details (
    detail_id INT PRIMARY KEY AUTO_INCREMENT,
    ffp_number VARCHAR(20),
    email VARCHAR(150),
    phone_number VARCHAR(50),
    country VARCHAR(100),
    enrollment_date DATETIME,
    FOREIGN KEY (ffp_number) REFERENCES members(ffp_number)
);

CREATE TABLE enrolment (
    enrolment_id INT PRIMARY KEY AUTO_INCREMENT,
    ffp_number VARCHAR(20),
    enrolment_date DATETIME,
    enrolment_ip VARCHAR(45),
    device VARCHAR(255),
    channel VARCHAR(50),
    status VARCHAR(20) DEFAULT 'Active',
    FOREIGN KEY (ffp_number) REFERENCES members(ffp_number)
);

CREATE TABLE claims (
    claim_id INT PRIMARY KEY AUTO_INCREMENT,
    ffp_number VARCHAR(20),
    date_submitted DATETIME,
    ticket_number VARCHAR(20),
    flight_number VARCHAR(10),
    departure_date DATE,
    status VARCHAR(20) DEFAULT 'Accepted',
    FOREIGN KEY (ffp_number) REFERENCES members(ffp_number)
);

CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    ffp_number VARCHAR(20),
    type VARCHAR(50), -- 'Accrual', 'Redemption - One Way Flight', etc.
    transaction_date DATETIME,
    processing_date DATETIME,
    status VARCHAR(20) DEFAULT 'Accepted',
    miles_amount INT,
    FOREIGN KEY (ffp_number) REFERENCES members(ffp_number)
);

CREATE TABLE tier (
    tier_id INT PRIMARY KEY AUTO_INCREMENT,
    ffp_number VARCHAR(20),
    tier_level VARCHAR(20) DEFAULT 'Basic',
    status VARCHAR(20) DEFAULT 'Active',
    start_date DATE,
    end_date DATE,
    qualification_method VARCHAR(50),
    FOREIGN KEY (ffp_number) REFERENCES members(ffp_number)
);

CREATE TABLE cs_contacts (
    contact_id INT PRIMARY KEY AUTO_INCREMENT,
    ffp_number VARCHAR(20),
    contact_time DATETIME,
    reason VARCHAR(100), -- reason for the contact/call
    channel VARCHAR(50),
    case_status VARCHAR(50),
    FOREIGN KEY (ffp_number) REFERENCES members(ffp_number)
);