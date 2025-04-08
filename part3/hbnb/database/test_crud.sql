-- Test CRUD operations on the HBnB database

-- 1. SELECT operations
-- Test selecting the admin user
SELECT * FROM users WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- Test selecting all amenities
SELECT * FROM amenities;

-- 2. INSERT operations
-- Test inserting a new user
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES 
    (UUID(), 'Test', 'User', 'test.user@example.com', '$2b$12$H1NYU2xE5CI/5zwnc7xSLufL/sItm7kGIRPxdqETntTq4bZsvpDXi', FALSE);

-- Verify the new user was inserted
SELECT * FROM users WHERE email = 'test.user@example.com';

-- Test inserting a new place
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES 
    (UUID(), 'Test Place', 'A test place for CRUD operations', 100.00, 40.7128, -74.0060, '36c9050e-ddd3-4c3b-9731-9f487208bbc1');

-- Verify the new place was inserted
SELECT * FROM places WHERE title = 'Test Place';

-- Store the place ID for later use
SET @test_place_id = (SELECT id FROM places WHERE title = 'Test Place');

-- Test inserting a place-amenity relationship
INSERT INTO place_amenity (place_id, amenity_id)
VALUES 
    (@test_place_id, 'f25b1b0e-2c91-4b1c-a7e4-72f2d7d0c3e1');

-- Verify the place-amenity relationship was inserted
SELECT p.title, a.name 
FROM places p
JOIN place_amenity pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id
WHERE p.title = 'Test Place';

-- 3. UPDATE operations
-- Test updating a user
UPDATE users 
SET first_name = 'Updated', last_name = 'Name' 
WHERE email = 'test.user@example.com';

-- Verify the user was updated
SELECT * FROM users WHERE email = 'test.user@example.com';

-- Test updating a place
UPDATE places 
SET price = 150.00, description = 'Updated description' 
WHERE title = 'Test Place';

-- Verify the place was updated
SELECT * FROM places WHERE title = 'Test Place';

-- 4. DELETE operations
-- Test deleting a place-amenity relationship
DELETE FROM place_amenity 
WHERE place_id = @test_place_id AND amenity_id = 'f25b1b0e-2c91-4b1c-a7e4-72f2d7d0c3e1';

-- Verify the place-amenity relationship was deleted
SELECT COUNT(*) FROM place_amenity WHERE place_id = @test_place_id;

-- Test deleting a place
DELETE FROM places WHERE title = 'Test Place';

-- Verify the place was deleted
SELECT COUNT(*) FROM places WHERE title = 'Test Place';

-- Test deleting a user
DELETE FROM users WHERE email = 'test.user@example.com';

-- Verify the user was deleted
SELECT COUNT(*) FROM users WHERE email = 'test.user@example.com';

-- 5. Test constraints
-- Test unique constraint on email
-- This should fail with a duplicate key error
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES 
    (UUID(), 'Duplicate', 'Email', 'admin@hbnb.io', 'password', FALSE);

-- Test foreign key constraint
-- This should fail with a foreign key constraint error
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES 
    (UUID(), 'Invalid Place', 'A place with an invalid owner_id', 100.00, 40.7128, -74.0060, 'invalid-uuid');

-- Test unique constraint on user_id and place_id in reviews
-- First, create a test place and a test user
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES 
    (UUID(), 'Review', 'User', 'review.user@example.com', '$2b$12$H1NYU2xE5CI/5zwnc7xSLufL/sItm7kGIRPxdqETntTq4bZsvpDXi', FALSE);

SET @review_user_id = (SELECT id FROM users WHERE email = 'review.user@example.com');

INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES 
    (UUID(), 'Review Place', 'A place for testing review constraints', 100.00, 40.7128, -74.0060, '36c9050e-ddd3-4c3b-9731-9f487208bbc1');

SET @review_place_id = (SELECT id FROM places WHERE title = 'Review Place');

-- Insert a review
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES 
    (UUID(), 'Test review', 5, @review_user_id, @review_place_id);

-- Try to insert another review for the same user and place
-- This should fail with a unique constraint error
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES 
    (UUID(), 'Duplicate review', 4, @review_user_id, @review_place_id);

-- Clean up test data
DELETE FROM reviews WHERE place_id = @review_place_id;
DELETE FROM places WHERE id = @review_place_id;
DELETE FROM users WHERE id = @review_user_id;
