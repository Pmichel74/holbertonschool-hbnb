/**
 * Login Functionality Test
 * This script tests the login functionality including:
 * 1. Valid and invalid credentials
 * 2. JWT token storage in cookies
 * 3. Redirections to the main page
 */

// Mock fetch API for testing
let mockFetchResponse = null;
let mockRedirectCalled = false;
let mockCookieSet = null;

// Store original functions before mocking
const originalFetch = window.fetch;
const originalLocationAssign = window.location.href;
const originalDocumentCookie = document.cookie;

// Setup test environment
function setupTestEnvironment() {
  // Mock fetch API
  window.fetch = (url, options) => {
    console.log(`Mock fetch called with URL: ${url}`);
    console.log('Request body:', options.body);
    return Promise.resolve({
      json: () => Promise.resolve(mockFetchResponse)
    });
  };

  // Mock window.location for redirect testing
  Object.defineProperty(window, 'location', {
    value: {
      href: '',
      set href(url) {
        console.log(`Mock redirect to: ${url}`);
        mockRedirectCalled = true;
        this._href = url;
      },
      get href() {
        return this._href;
      }
    }
  });

  // Mock document.cookie for token storage testing
  Object.defineProperty(document, 'cookie', {
    set(value) {
      console.log(`Mock cookie set: ${value}`);
      mockCookieSet = value;
    },
    get() {
      return mockCookieSet || '';
    }
  });

  // Create mock DOM elements
  document.body.innerHTML = `
    <form id="login-form">
      <input id="email" value="" />
      <input id="password" value="" />
      <button type="submit">Login</button>
    </form>
    <div id="error-message" style="display: none;"></div>
  `;
}

// Reset test environment
function resetTestEnvironment() {
  window.fetch = originalFetch;
  window.location.href = originalLocationAssign;
  document.cookie = originalDocumentCookie;
  mockFetchResponse = null;
  mockRedirectCalled = false;
  mockCookieSet = null;
  document.body.innerHTML = '';
}

// Test functions
async function testValidLogin() {
  console.log('--- Testing Valid Login ---');
  setupTestEnvironment();
  
  // Set valid login response
  mockFetchResponse = { token: 'valid-jwt-token-123' };
  
  // Set form values
  document.getElementById('email').value = 'valid@example.com';
  document.getElementById('password').value = 'correctpassword';
  
  // Import login function from the main script
  await loginUser('valid@example.com', 'correctpassword');
  
  // Check if token was stored in cookie
  console.assert(
    mockCookieSet && mockCookieSet.includes('token=valid-jwt-token-123'), 
    'JWT token should be stored in cookie'
  );
  
  // Check if redirect was called
  console.assert(
    mockRedirectCalled && window.location.href === 'index.html',
    'User should be redirected to the main page'
  );
  
  console.log('Valid login test completed');
  resetTestEnvironment();
}

async function testInvalidLogin() {
  console.log('--- Testing Invalid Login ---');
  setupTestEnvironment();
  
  // Set invalid login response
  mockFetchResponse = { error: 'Invalid credentials' };
  
  // Set form values
  document.getElementById('email').value = 'invalid@example.com';
  document.getElementById('password').value = 'wrongpassword';
  
  // Import login function from the main script
  await loginUser('invalid@example.com', 'wrongpassword');
  
  // Check if error message is displayed
  const errorMessage = document.getElementById('error-message');
  console.assert(
    errorMessage.style.display === 'block',
    'Error message should be displayed'
  );
  
  // Check that no token was stored
  console.assert(
    !mockCookieSet || !mockCookieSet.includes('token='),
    'No JWT token should be stored for invalid login'
  );
  
  // Check that no redirect happened
  console.assert(
    !mockRedirectCalled,
    'No redirect should happen for invalid login'
  );
  
  console.log('Invalid login test completed');
  resetTestEnvironment();
}

// Run all tests
async function runAllTests() {
  console.log('Starting login functionality tests...');
  
  await testValidLogin();
  await testInvalidLogin();
  
  console.log('All tests completed!');
}

// Import login function
function importLoginUser() {
  // In a real environment, you would properly import the login function
  // For test purposes, make sure this function exists in your global scope
  if (typeof loginUser !== 'function') {
    console.error('loginUser function not found! Make sure it is globally available');
  }
}

// Run tests when this script is executed
document.addEventListener('DOMContentLoaded', () => {
  importLoginUser();
  runAllTests();
});