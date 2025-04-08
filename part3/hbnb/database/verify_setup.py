#!/usr/bin/env python3
"""
Script to verify that the database has been properly set up with the initial data
"""
import sqlite3
import os
import sys

# Path to the SQLite database
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'instance', 'development.db')

def verify_admin_user(cursor):
    """Verify that the admin user exists"""
    print("Verifying admin user...")
    
    cursor.execute("SELECT * FROM users WHERE id = ?", ('36c9050e-ddd3-4c3b-9731-9f487208bbc1',))
    admin_user = cursor.fetchone()
    
    if admin_user:
        print("✅ Admin user exists with ID: 36c9050e-ddd3-4c3b-9731-9f487208bbc1")
        print(f"   Email: {admin_user[3]}")
        print(f"   Name: {admin_user[1]} {admin_user[2]}")
        print(f"   Is Admin: {'Yes' if admin_user[5] else 'No'}")
        return True
    else:
        print("❌ Admin user does not exist!")
        return False

def verify_amenities(cursor):
    """Verify that the initial amenities exist"""
    print("\nVerifying initial amenities...")
    
    cursor.execute("SELECT * FROM amenities")
    amenities = cursor.fetchall()
    
    required_amenities = ['WiFi', 'Swimming Pool', 'Air Conditioning']
    found_amenities = [amenity[1] for amenity in amenities]
    
    all_found = True
    for amenity in required_amenities:
        if amenity in found_amenities:
            print(f"✅ Amenity '{amenity}' exists")
        else:
            print(f"❌ Amenity '{amenity}' does not exist!")
            all_found = False
    
    return all_found

def verify_tables(cursor):
    """Verify that all required tables exist"""
    print("\nVerifying database tables...")
    
    # Get all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [table[0] for table in cursor.fetchall()]
    
    required_tables = ['users', 'places', 'amenities', 'reviews', 'place_amenity']
    
    all_found = True
    for table in required_tables:
        if table in tables:
            print(f"✅ Table '{table}' exists")
        else:
            print(f"❌ Table '{table}' does not exist!")
            all_found = False
    
    return all_found

def verify_constraints(cursor):
    """Verify that constraints are working"""
    print("\nVerifying database constraints...")
    
    # Test unique constraint on email
    try:
        cursor.execute('''
        INSERT INTO users (id, first_name, last_name, email, password, is_admin)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', ('test-uuid', 'Test', 'User', 'admin@hbnb.io', 'password', 0))
        print("❌ Unique constraint on email failed!")
        return False
    except sqlite3.IntegrityError:
        print("✅ Unique constraint on email works")
    
    # Test foreign key constraint
    try:
        cursor.execute('''
        INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ('test-uuid', 'Test Place', 'Test description', 100.00, 40.7128, -74.0060, 'invalid-uuid'))
        print("❌ Foreign key constraint failed!")
        return False
    except sqlite3.IntegrityError:
        print("✅ Foreign key constraint works")
    
    # Test check constraint on rating
    try:
        # First, create a valid user and place
        user_id = 'test-user-id'
        place_id = 'test-place-id'
        
        cursor.execute('''
        INSERT INTO users (id, first_name, last_name, email, password, is_admin)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, 'Test', 'User', 'test.user@example.com', 'password', 0))
        
        cursor.execute('''
        INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (place_id, 'Test Place', 'Test description', 100.00, 40.7128, -74.0060, '36c9050e-ddd3-4c3b-9731-9f487208bbc1'))
        
        # Try to insert a review with an invalid rating
        cursor.execute('''
        INSERT INTO reviews (id, text, rating, user_id, place_id)
        VALUES (?, ?, ?, ?, ?)
        ''', ('test-review-id', 'Test review', 6, user_id, place_id))
        
        # Clean up
        cursor.execute("DELETE FROM reviews WHERE id = ?", ('test-review-id',))
        cursor.execute("DELETE FROM places WHERE id = ?", (place_id,))
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        print("❌ Check constraint on rating failed!")
        return False
    except sqlite3.IntegrityError:
        # Clean up
        try:
            cursor.execute("DELETE FROM places WHERE id = ?", (place_id,))
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        except:
            pass
        
        print("✅ Check constraint on rating works")
    
    return True

def main():
    """Main function to verify the database setup"""
    print(f"Verifying SQLite database at: {DB_PATH}")
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database file does not exist at: {DB_PATH}")
        return False
    
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
    cursor = conn.cursor()
    
    try:
        # Verify tables
        tables_ok = verify_tables(cursor)
        
        # Verify admin user
        admin_ok = verify_admin_user(cursor)
        
        # Verify amenities
        amenities_ok = verify_amenities(cursor)
        
        # Verify constraints
        constraints_ok = verify_constraints(cursor)
        
        # Overall verification result
        print("\nOverall verification result:")
        if tables_ok and admin_ok and amenities_ok and constraints_ok:
            print("✅ Database setup is correct!")
            return True
        else:
            print("❌ Database setup has issues!")
            return False
    
    except Exception as e:
        print(f"Error during verification: {e}")
        return False
    
    finally:
        # Close the connection
        conn.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
