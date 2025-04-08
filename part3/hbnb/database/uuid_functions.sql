-- Function to generate a UUID in the format required by the application
DELIMITER //

-- Drop the function if it exists to avoid errors
DROP FUNCTION IF EXISTS generate_uuid //

-- Create a function to generate a UUID
CREATE FUNCTION generate_uuid() 
RETURNS CHAR(36)
BEGIN
    -- Generate a UUID using UUID() function and return it as a string
    RETURN UUID();
END //

DELIMITER ;

-- Example usage:
-- INSERT INTO users (id, first_name, last_name, email, password)
-- VALUES (generate_uuid(), 'John', 'Doe', 'john.doe@example.com', 'hashed_password');
