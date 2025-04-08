#!/usr/bin/env python3
"""
Script to generate a bcrypt hash for a password
"""
import bcrypt

def hash_password(password):
    """
    Hash a password using bcrypt
    
    Args:
        password (str): The password to hash
        
    Returns:
        str: The hashed password
    """
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')
    
    # Generate a salt and hash the password
    salt = bcrypt.gensalt(12)  # 12 is the work factor, higher is more secure but slower
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return the hash as a string
    return hashed.decode('utf-8')

if __name__ == "__main__":
    # Hash the admin password
    admin_password = "admin1234"
    hashed_password = hash_password(admin_password)
    
    print(f"Original password: {admin_password}")
    print(f"Hashed password: {hashed_password}")
    
    # Verify the hash works
    password_bytes = admin_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    is_valid = bcrypt.checkpw(password_bytes, hashed_bytes)
    print(f"Password verification: {'Success' if is_valid else 'Failed'}")
