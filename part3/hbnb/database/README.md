# HBnB Database Scripts

This directory contains SQL scripts for setting up and managing the HBnB database.

## Files

- `create_tables.sql`: Creates all the necessary tables for the HBnB application
- `drop_tables.sql`: Drops all tables in the correct order to avoid foreign key constraint issues
- `uuid_functions.sql`: Defines a function to generate UUIDs for the id fields
- `sample_data.sql`: Inserts sample data into the database for testing
- `initial_data.sql`: Inserts the required initial data (admin user and amenities)
- `generate_password_hash.py`: Python script to generate bcrypt hashes for passwords
- `test_crud.sql`: Tests CRUD operations and constraints on the database
- `test_sqlite.py`: Python script to test the SQLite database
- `verify_setup.py`: Python script to verify the database setup

## Database Schema

The database consists of the following tables:

1. `users`: Stores user information
2. `places`: Stores information about rental properties
3. `amenities`: Stores available amenities
4. `place_amenity`: Junction table for the many-to-many relationship between places and amenities
5. `reviews`: Stores user reviews for places

## Usage

### Setting up the database

1. Create the tables:
   ```
   mysql -u username -p database_name < create_tables.sql
   ```

2. Create the UUID function:
   ```
   mysql -u username -p database_name < uuid_functions.sql
   ```

3. Insert initial data:
   ```
   mysql -u username -p database_name < initial_data.sql
   ```

4. (Optional) Insert additional sample data:
   ```
   mysql -u username -p database_name < sample_data.sql
   ```

5. (Optional) Test CRUD operations:
   ```
   mysql -u username -p database_name < test_crud.sql
   ```

### Testing with SQLite

If you're using SQLite instead of MySQL, you can use the `test_sqlite.py` script to test the database:

```
python database/test_sqlite.py
```

This script will:
1. Create all the tables in the SQLite database
2. Insert the initial data (admin user and amenities)
3. Test CRUD operations and constraints
4. Clean up test data

### Verifying the Database Setup

To verify that the database has been set up correctly, you can use the `verify_setup.py` script:

```
python database/verify_setup.py
```

This script will:
1. Verify that all required tables exist
2. Verify that the admin user exists with the correct ID and attributes
3. Verify that the initial amenities exist
4. Verify that all constraints are working correctly
5. Provide a detailed report of the verification results

### Resetting the database

To drop all tables and start fresh:
```
mysql -u username -p database_name < drop_tables.sql
```

## Table Relationships

- **User-Place**: One-to-Many (A user can own many places)
- **Place-Review**: One-to-Many (A place can have many reviews)
- **User-Review**: One-to-Many (A user can write many reviews)
- **Place-Amenity**: Many-to-Many (A place can have many amenities, and an amenity can be in many places)

## Constraints

- Foreign key constraints ensure referential integrity
- Unique constraint on user email ensures no duplicate emails
- Unique constraint on user_id and place_id in reviews ensures a user can only leave one review per place
- Check constraint on rating ensures it's between 1 and 5

## Initial Data

The `initial_data.sql` script inserts:

1. An administrator user with:
   - Fixed UUID: 36c9050e-ddd3-4c3b-9731-9f487208bbc1
   - Email: admin@hbnb.io
   - Password: admin1234 (stored as a bcrypt hash)
   - Admin privileges: TRUE

2. Initial amenities:
   - WiFi
   - Swimming Pool
   - Air Conditioning

## Testing

### MySQL Testing

The `test_crud.sql` script tests:

1. SELECT operations to verify data was inserted correctly
2. INSERT operations for users, places, and relationships
3. UPDATE operations to modify existing data
4. DELETE operations to remove test data
5. Constraint testing to ensure data integrity:
   - Unique constraint on email
   - Foreign key constraints
   - Unique constraint on user_id and place_id in reviews

### SQLite Testing

The `test_sqlite.py` script performs the same tests as the `test_crud.sql` script, but it's adapted for SQLite. It:

1. Creates the tables with SQLite-compatible syntax
2. Inserts the initial data with the required UUIDs
3. Tests all CRUD operations
4. Verifies all constraints are working correctly
5. Provides detailed output of each test step

### Verification

The `verify_setup.py` script provides a comprehensive verification of the database setup:

1. Table verification: Checks that all required tables exist
2. Admin user verification: Confirms the admin user exists with the correct ID and attributes
3. Amenities verification: Ensures all required amenities are present
4. Constraint verification: Tests all constraints to ensure data integrity
5. Overall verification: Provides a summary of the verification results
