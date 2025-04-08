-- Sample data for the HBnB database

-- Insert sample users
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES 
    (UUID(), 'John', 'Doe', 'john.doe@example.com', '$2b$12$tM/ArInkI0vfRbLFI8Kzxe5SRX8xHcx4xJ6/T5AvVzkbwrQjWdRHK', FALSE),
    (UUID(), 'Jane', 'Smith', 'jane.smith@example.com', '$2b$12$tM/ArInkI0vfRbLFI8Kzxe5SRX8xHcx4xJ6/T5AvVzkbwrQjWdRHK', FALSE),
    (UUID(), 'Admin', 'User', 'admin@example.com', '$2b$12$tM/ArInkI0vfRbLFI8Kzxe5SRX8xHcx4xJ6/T5AvVzkbwrQjWdRHK', TRUE);

-- Store user IDs for reference in other tables
SET @john_id = (SELECT id FROM users WHERE email = 'john.doe@example.com');
SET @jane_id = (SELECT id FROM users WHERE email = 'jane.smith@example.com');
SET @admin_id = (SELECT id FROM users WHERE email = 'admin@example.com');

-- Insert sample amenities
INSERT INTO amenities (id, name)
VALUES 
    (UUID(), 'WiFi'),
    (UUID(), 'Kitchen'),
    (UUID(), 'Air Conditioning'),
    (UUID(), 'Washer'),
    (UUID(), 'Pool'),
    (UUID(), 'Free Parking');

-- Store amenity IDs for reference
SET @wifi_id = (SELECT id FROM amenities WHERE name = 'WiFi');
SET @kitchen_id = (SELECT id FROM amenities WHERE name = 'Kitchen');
SET @ac_id = (SELECT id FROM amenities WHERE name = 'Air Conditioning');
SET @washer_id = (SELECT id FROM amenities WHERE name = 'Washer');
SET @pool_id = (SELECT id FROM amenities WHERE name = 'Pool');
SET @parking_id = (SELECT id FROM amenities WHERE name = 'Free Parking');

-- Insert sample places
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES 
    (UUID(), 'Cozy Apartment in Downtown', 'A beautiful apartment in the heart of the city with all amenities.', 120.00, 40.7128, -74.0060, @john_id),
    (UUID(), 'Beach House', 'Stunning beach house with ocean view.', 250.00, 34.0522, -118.2437, @jane_id),
    (UUID(), 'Mountain Cabin', 'Peaceful cabin in the mountains with breathtaking views.', 180.00, 39.7392, -104.9903, @john_id),
    (UUID(), 'Luxury Villa', 'Spacious villa with private pool and garden.', 350.00, 37.7749, -122.4194, @admin_id);

-- Store place IDs for reference
SET @apartment_id = (SELECT id FROM places WHERE title = 'Cozy Apartment in Downtown');
SET @beach_house_id = (SELECT id FROM places WHERE title = 'Beach House');
SET @cabin_id = (SELECT id FROM places WHERE title = 'Mountain Cabin');
SET @villa_id = (SELECT id FROM places WHERE title = 'Luxury Villa');

-- Link places with amenities
INSERT INTO place_amenity (place_id, amenity_id)
VALUES 
    (@apartment_id, @wifi_id),
    (@apartment_id, @kitchen_id),
    (@apartment_id, @ac_id),
    (@beach_house_id, @wifi_id),
    (@beach_house_id, @kitchen_id),
    (@beach_house_id, @washer_id),
    (@cabin_id, @wifi_id),
    (@cabin_id, @kitchen_id),
    (@cabin_id, @parking_id),
    (@villa_id, @wifi_id),
    (@villa_id, @kitchen_id),
    (@villa_id, @ac_id),
    (@villa_id, @washer_id),
    (@villa_id, @pool_id),
    (@villa_id, @parking_id);

-- Insert sample reviews
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES 
    (UUID(), 'Great place to stay! Very clean and comfortable.', 5, @jane_id, @apartment_id),
    (UUID(), 'Amazing location and beautiful views.', 4, @john_id, @beach_house_id),
    (UUID(), 'Peaceful and relaxing. Perfect getaway.', 5, @jane_id, @cabin_id),
    (UUID(), 'Luxurious and spacious. Highly recommend!', 5, @john_id, @villa_id),
    (UUID(), 'Good amenities but a bit overpriced.', 3, @admin_id, @beach_house_id);
