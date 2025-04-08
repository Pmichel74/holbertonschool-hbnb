#!/usr/bin/env python3
"""
Script to test the SQLite database using the SQL scripts
"""
import sqlite3
import os
import uuid
import bcrypt
from datetime import datetime

# Path to the SQLite database
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'instance', 'development.db')

def execute_sql_file(cursor, file_path):
    """
    Execute SQL statements from a file
    
    Args:
        cursor: SQLite cursor
        file_path: Path to the SQL file
    """
    with open(file_path, 'r') as f:
        sql = f.read()
    
    # Split the SQL file into individual statements
    statements = sql.split(';')
    
    for statement in statements:
        # Skip empty statements
        if statement.strip():
            # Replace MySQL-specific syntax with SQLite syntax
            statement = statement.replace('CHAR(36)', 'TEXT')
            statement = statement.replace('BOOLEAN', 'INTEGER')
            statement = statement.replace('DECIMAL(10, 2)', 'REAL')
            statement = statement.replace('FLOAT', 'REAL')
            statement = statement.replace('TEXT', 'TEXT')
            statement = statement.replace('UUID()', 'hex(randomblob(16))')
            statement = statement.replace('DEFAULT CURRENT_TIMESTAMP', "DEFAULT (datetime('now'))")
            statement = statement.replace('ON UPDATE CURRENT_TIMESTAMP', '')
            
            try:
                cursor.execute(statement)
            except sqlite3.Error as e:
                print(f"Error executing statement: {statement}")
                print(f"Error message: {e}")

def create_tables(cursor):
    """Create the tables in the database"""
    print("Creating tables...")
    
    # Drop existing tables if they exist
    cursor.execute("DROP TABLE IF EXISTS place_amenity")
    cursor.execute("DROP TABLE IF EXISTS reviews")
    cursor.execute("DROP TABLE IF EXISTS places")
    cursor.execute("DROP TABLE IF EXISTS amenities")
    cursor.execute("DROP TABLE IF EXISTS users")
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create places table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS places (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        owner_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')
    
    # Create amenities table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS amenities (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create place_amenity table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS place_amenity (
        place_id TEXT NOT NULL,
        amenity_id TEXT NOT NULL,
        PRIMARY KEY (place_id, amenity_id),
        FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
        FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
    )
    ''')
    
    # Create reviews table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id TEXT PRIMARY KEY,
        text TEXT NOT NULL,
        rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
        user_id TEXT NOT NULL,
        place_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
        UNIQUE (user_id, place_id)
    )
    ''')
    
    print("Tables created successfully!")

def insert_initial_data(cursor):
    """Insert initial data into the database"""
    print("Inserting initial data...")
    
    # Insert administrator user with fixed UUID
    admin_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
    admin_password = '$2b$12$H1NYU2xE5CI/5zwnc7xSLufL/sItm7kGIRPxdqETntTq4bZsvpDXi'  # bcrypt hash of 'admin1234'
    
    cursor.execute('''
    INSERT INTO users (id, first_name, last_name, email, password, is_admin)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (admin_id, 'Admin', 'HBnB', 'admin@hbnb.io', admin_password, 1))
    
    # Insert initial amenities with randomly generated UUIDs
    wifi_id = str(uuid.uuid4())
    pool_id = str(uuid.uuid4())
    ac_id = str(uuid.uuid4())
    
    cursor.execute('''
    INSERT INTO amenities (id, name)
    VALUES (?, ?)
    ''', (wifi_id, 'WiFi'))
    
    cursor.execute('''
    INSERT INTO amenities (id, name)
    VALUES (?, ?)
    ''', (pool_id, 'Swimming Pool'))
    
    cursor.execute('''
    INSERT INTO amenities (id, name)
    VALUES (?, ?)
    ''', (ac_id, 'Air Conditioning'))
    
    print("Initial data inserted successfully!")
    
    return admin_id, wifi_id, pool_id, ac_id

def test_crud_operations(cursor, admin_id, wifi_id):
    """Test CRUD operations on the database"""
    print("Testing CRUD operations...")
    
    # Test SELECT operations
    print("\nTesting SELECT operations...")
    cursor.execute("SELECT * FROM users WHERE id = ?", (admin_id,))
    admin_user = cursor.fetchone()
    print(f"Admin user: {admin_user}")
    
    cursor.execute("SELECT * FROM amenities")
    amenities = cursor.fetchall()
    print(f"Amenities: {amenities}")
    
    # Test INSERT operations
    print("\nTesting INSERT operations...")
    test_user_id = str(uuid.uuid4())
    cursor.execute('''
    INSERT INTO users (id, first_name, last_name, email, password, is_admin)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (test_user_id, 'Test', 'User', 'test.user@example.com', '$2b$12$H1NYU2xE5CI/5zwnc7xSLufL/sItm7kGIRPxdqETntTq4bZsvpDXi', 0))
    
    cursor.execute("SELECT * FROM users WHERE email = ?", ('test.user@example.com',))
    test_user = cursor.fetchone()
    print(f"Test user: {test_user}")
    
    test_place_id = str(uuid.uuid4())
    cursor.execute('''
    INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (test_place_id, 'Test Place', 'A test place for CRUD operations', 100.00, 40.7128, -74.0060, admin_id))
    
    cursor.execute("SELECT * FROM places WHERE title = ?", ('Test Place',))
    test_place = cursor.fetchone()
    print(f"Test place: {test_place}")
    
    cursor.execute('''
    INSERT INTO place_amenity (place_id, amenity_id)
    VALUES (?, ?)
    ''', (test_place_id, wifi_id))
    
    cursor.execute('''
    SELECT p.title, a.name 
    FROM places p
    JOIN place_amenity pa ON p.id = pa.place_id
    JOIN amenities a ON pa.amenity_id = a.id
    WHERE p.title = ?
    ''', ('Test Place',))
    place_amenity = cursor.fetchone()
    print(f"Place-amenity relationship: {place_amenity}")
    
    # Test UPDATE operations
    print("\nTesting UPDATE operations...")
    cursor.execute('''
    UPDATE users 
    SET first_name = ?, last_name = ? 
    WHERE email = ?
    ''', ('Updated', 'Name', 'test.user@example.com'))
    
    cursor.execute("SELECT * FROM users WHERE email = ?", ('test.user@example.com',))
    updated_user = cursor.fetchone()
    print(f"Updated user: {updated_user}")
    
    cursor.execute('''
    UPDATE places 
    SET price = ?, description = ? 
    WHERE title = ?
    ''', (150.00, 'Updated description', 'Test Place'))
    
    cursor.execute("SELECT * FROM places WHERE title = ?", ('Test Place',))
    updated_place = cursor.fetchone()
    print(f"Updated place: {updated_place}")
    
    # Test DELETE operations
    print("\nTesting DELETE operations...")
    cursor.execute('''
    DELETE FROM place_amenity 
    WHERE place_id = ? AND amenity_id = ?
    ''', (test_place_id, wifi_id))
    
    cursor.execute("SELECT COUNT(*) FROM place_amenity WHERE place_id = ?", (test_place_id,))
    count = cursor.fetchone()[0]
    print(f"Place-amenity relationships for test place: {count}")
    
    cursor.execute("DELETE FROM places WHERE title = ?", ('Test Place',))
    
    cursor.execute("SELECT COUNT(*) FROM places WHERE title = ?", ('Test Place',))
    count = cursor.fetchone()[0]
    print(f"Places with title 'Test Place': {count}")
    
    cursor.execute("DELETE FROM users WHERE email = ?", ('test.user@example.com',))
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", ('test.user@example.com',))
    count = cursor.fetchone()[0]
    print(f"Users with email 'test.user@example.com': {count}")
    
    # Test constraints
    print("\nTesting constraints...")
    try:
        cursor.execute('''
        INSERT INTO users (id, first_name, last_name, email, password, is_admin)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (str(uuid.uuid4()), 'Duplicate', 'Email', 'admin@hbnb.io', 'password', 0))
        print("Unique constraint on email failed!")
    except sqlite3.IntegrityError as e:
        print(f"Unique constraint on email works: {e}")
    
    try:
        cursor.execute('''
        INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (str(uuid.uuid4()), 'Invalid Place', 'A place with an invalid owner_id', 100.00, 40.7128, -74.0060, 'invalid-uuid'))
        print("Foreign key constraint failed!")
    except sqlite3.IntegrityError as e:
        print(f"Foreign key constraint works: {e}")
    
    # Test unique constraint on user_id and place_id in reviews
    review_user_id = str(uuid.uuid4())
    cursor.execute('''
    INSERT INTO users (id, first_name, last_name, email, password, is_admin)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (review_user_id, 'Review', 'User', 'review.user@example.com', '$2b$12$H1NYU2xE5CI/5zwnc7xSLufL/sItm7kGIRPxdqETntTq4bZsvpDXi', 0))
    
    review_place_id = str(uuid.uuid4())
    cursor.execute('''
    INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (review_place_id, 'Review Place', 'A place for testing review constraints', 100.00, 40.7128, -74.0060, admin_id))
    
    cursor.execute('''
    INSERT INTO reviews (id, text, rating, user_id, place_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (str(uuid.uuid4()), 'Test review', 5, review_user_id, review_place_id))
    
    try:
        cursor.execute('''
        INSERT INTO reviews (id, text, rating, user_id, place_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (str(uuid.uuid4()), 'Duplicate review', 4, review_user_id, review_place_id))
        print("Unique constraint on user_id and place_id in reviews failed!")
    except sqlite3.IntegrityError as e:
        print(f"Unique constraint on user_id and place_id in reviews works: {e}")
    
    # Clean up test data
    cursor.execute("DELETE FROM reviews WHERE place_id = ?", (review_place_id,))
    cursor.execute("DELETE FROM places WHERE id = ?", (review_place_id,))
    cursor.execute("DELETE FROM users WHERE id = ?", (review_user_id,))
    
    print("\nCRUD operations tested successfully!")

def main():
    """Main function to test the database"""
    print(f"Testing SQLite database at: {DB_PATH}")
    
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
    cursor = conn.cursor()
    
    try:
        # Create tables
        create_tables(cursor)
        
        # Insert initial data
        admin_id, wifi_id, pool_id, ac_id = insert_initial_data(cursor)
        
        # Test CRUD operations
        test_crud_operations(cursor, admin_id, wifi_id)
        
        # Commit changes
        conn.commit()
        
        print("\nAll tests completed successfully!")
    
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    
    finally:
        # Close the connection
        conn.close()

if __name__ == "__main__":
    main()
