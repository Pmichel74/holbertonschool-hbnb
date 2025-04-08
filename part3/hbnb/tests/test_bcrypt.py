from flask_bcrypt import Bcrypt

def test_bcrypt():
    """Test that bcrypt password hashing works correctly"""
    # Create a bcrypt instance
    bcrypt = Bcrypt()
    
    # Hash a password
    password = "password123"
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # Check that the password is hashed
    print("Password is hashed:", hashed_password != password)
    print("Hashed password:", hashed_password)
    
    # Verify that the password verification works
    print("Correct password verification:", bcrypt.check_password_hash(hashed_password, password))
    print("Incorrect password verification:", bcrypt.check_password_hash(hashed_password, "wrongpassword"))

if __name__ == "__main__":
    test_bcrypt()
