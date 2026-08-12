-- Table: member
CREATE TABLE member (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    membership_type VARCHAR(50) NOT NULL,
    membership_end_date DATE NOT NULL
);

-- Table: class
CREATE TABLE class (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    trainer_name VARCHAR(100) NOT NULL,
    day_time VARCHAR(50) NOT NULL,
    capacity INTEGER NOT NULL
);

-- Table: booking
CREATE TABLE booking (
    id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES member(id),
    class_id INTEGER NOT NULL REFERENCES class(id),
    booking_date DATE NOT NULL
);

--Seed data
INSERT INTO member (name, phone, membership_type, membership_end_date) VALUES
('Ali Hasan', '0791234567', 'Monthly', '2026-12-08'),
('Sara Q.', '0782345678', 'Yearly', '2027-06-01');

INSERT INTO class (name, trainer_name, day_time, capacity) VALUES
('Yoga', 'Sara', 'Tue 18:00', 10),
('Cardio', 'Omar', 'Thu 17:00', 15);

INSERT INTO booking (member_id, class_id, booking_date) VALUES
(1, 1, '2026-08-04'),
(2, 1, '2026-08-04');
