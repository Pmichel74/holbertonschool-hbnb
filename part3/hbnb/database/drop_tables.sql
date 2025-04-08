-- Drop tables in reverse order of creation to avoid foreign key constraint issues

-- Drop the place_amenity table (many-to-many relationship)
DROP TABLE IF EXISTS place_amenity;

-- Drop the reviews table
DROP TABLE IF EXISTS reviews;

-- Drop the places table
DROP TABLE IF EXISTS places;

-- Drop the amenities table
DROP TABLE IF EXISTS amenities;

-- Drop the users table
DROP TABLE IF EXISTS users;
