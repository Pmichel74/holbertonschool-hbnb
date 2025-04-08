# HBnB API Tests

This directory contains test scripts for the HBnB API.

## Admin Endpoints Test

The `test_admin_endpoints.py` script demonstrates different strategies to test admin endpoints and provides curl commands for testing.

### Running the Test Script

```bash
cd /home/jbn/holbertonschool-hbnb/part3/hbnb
python3 tests/test_admin_endpoints.py
```

### Testing Strategies

The script presents three strategies for testing admin endpoints:

1. **Create an admin user directly in the database**
   - This approach bypasses the API's normal user creation flow
   - Directly insert a user with `is_admin=True` in the database
   - Use the admin credentials to obtain a JWT token

2. **Modify the authentication logic temporarily for testing**
   - Temporarily modify the login endpoint in auth.py to grant admin privileges
   - Create a special case for a test user to receive admin privileges
   - Revert changes after testing

3. **Create a special test endpoint**
   - Create a special endpoint that is only available in development/test environments
   - This endpoint returns a JWT token with admin privileges
   - Secure it by only enabling in non-production environments

### Testing Admin Endpoints

Once you have an admin token using one of the strategies above, you can test the admin endpoints using the curl commands provided by the script:

1. Create a new user as an admin
2. Modify another user's data as an admin
3. Add a new amenity as an admin
4. Modify an amenity as an admin
5. Modify a place that doesn't belong to the admin
6. Modify a review that doesn't belong to the admin
7. Delete a review that doesn't belong to the admin

### Important Notes

- Replace `<user_id>`, `<amenity_id>`, `<place_id>`, and `<review_id>` with actual IDs from your database
- Make sure the API server is running before testing
- For security reasons, do not use these testing strategies in production
