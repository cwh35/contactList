-- Create the contact table
CREATE TABLE IF NOT EXISTS contact (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone BIGINT NOT NULL UNIQUE,
    address VARCHAR(100) NOT NULL
);

-- Insert initial data into the contact table
INSERT INTO contact (id, first_name, last_name, email, phone, address)
VALUES (1, 'cam', 'henning', 'camhen@gmail.com', 551023102, 'W High Street');
