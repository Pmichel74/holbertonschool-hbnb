**README - User API (hbnb/part2/api/v1/users.py)**  

### **Description**  
This file contains API routes for managing users. Currently, it only supports read operations (`GET`).  

### **Available Endpoints**  

1. **GET /api/v1/users/**  
   - Returns a list of all users in JSON format.  
   - Response:  
     - **200 OK** → List of users.  

2. **GET /api/v1/users/<user_id>**  
   - Retrieves a specific user based on `user_id`.  
   - Response:  
     - **200 OK** → User details.  
     - **404 Not Found** → User does not exist.  

### **Request Examples**  

- **Retrieve all users**:  
  ```bash
  curl -X GET http://127.0.0.1:5000/api/v1/users/
  ```

- **Retrieve a specific user**:  
  ```bash
  curl -X GET http://127.0.0.1:5000/api/v1/users/1234
  ```

### **Unit Tests**  
Tests for these endpoints are defined in `hbnb/part2/tests/test_user.py`.  
- **Run tests**:  
  ```bash
  python3 -m unittest hbnb/part2/tests/test_user.py
  ```  
