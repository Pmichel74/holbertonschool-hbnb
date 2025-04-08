-- Insert initial data into the HBnB database

-- Insert administrator user with fixed UUID
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES 
    ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$H1NYU2xE5CI/5zwnc7xSLufL/sItm7kGIRPxdqETntTq4bZsvpDXi', TRUE);

-- Insert initial amenities with randomly generated UUIDs
INSERT INTO amenities (id, name)
VALUES 
    ('f25b1b0e-2c91-4b1c-a7e4-72f2d7d0c3e1', 'WiFi'),
    ('a1b2c3d4-e5f6-4a5b-9c8d-7e6f5a4b3c2d', 'Swimming Pool'),
    ('9d8c7b6a-5f4e-3d2c-1b0a-9f8e7d6c5b4a', 'Air Conditioning');

-- Verify the data was inserted correctly
SELECT * FROM users WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
SELECT * FROM amenities;
