# NetFix Testing Instructions

## 🔧 Functional Testing Requirements

### 📝 User Registration Testing

#### Customer Registration
1. **Register a new Customer account**
   - Verify that the registration form requests all required fields:
     - Username
     - Email address
     - Password
     - Password confirmation
     - Date of birth

#### Company Registration
2. **Register a new Company account (Electricity specialization)**
   - Confirm that the registration form includes:
     - Username
     - Email address
     - Password
     - Password confirmation
     - Field of work selection

3. **Field of Work Validation**
   - Ensure the field of work dropdown is restricted to these specific values:
     - Air Conditioner
     - All in One
     - Carpentry
     - Electricity
     - Gardening
     - Home Machines
     - Housekeeping
     - Interior Design
     - Locks
     - Painting
     - Plumbing
     - Water Heaters

#### Dual User Type Support
4. **Multi-User Type Registration**
   - Verify that the system supports registration of both Customer and Company user types

#### Registration Validation Testing
5. **Username Uniqueness Validation**
   - Attempt to register with an existing username
   - Confirm that an appropriate warning message is displayed

6. **Email Uniqueness Validation**
   - Attempt to register with an existing email address
   - Verify that a proper warning message appears

### 👤 Profile Management Testing

#### Company Profile Verification
7. **Company Profile Display**
   - Log in with a Company account and navigate to the profile page
   - Verify that all user information is visible (excluding password for security)

#### Service Creation Testing
8. **Service Creation Process**
   - While logged in as the Electricity Company, create a new service
   - Set the price per hour to $10.50
   - Confirm that the form requests:
     - Service name
     - Service description
     - Price per hour
     - Service field/category

9. **Service Display on Company Profile**
   - Navigate to the Company profile page
   - Verify that the newly created service appears in the available services list

### 🌐 Service Discovery and Display

#### Service Listing Pages
10. **All Services Page**
    - Confirm there is a page displaying all services from all companies

11. **Category-Specific Service Pages**
    - Verify that each service type has its own dedicated page
    - Check that these pages show only services of that specific category

12. **Individual Service Detail Pages**
    - Ensure each service has its own detailed page displaying:
      - Service name
      - Description
      - Service field/category
      - Price per hour
      - Creation date
      - Company name that created the service

### 🛒 Customer Service Request Testing

#### Customer Profile Verification
13. **Customer Profile Display**
    - Log out from Company account
    - Register and log in with a Customer account
    - Navigate to the Customer profile page
    - Verify all customer information is displayed (excluding password)

#### Service Request Process
14. **Service Request Functionality**
    - Navigate to the previously created service
    - Request the service for a 2-hour duration
    - Confirm the request form asks for:
      - Service address
      - Service duration (in hours)

15. **Customer Request History**
    - Return to the Customer profile page
    - Verify that the requested service appears in the request history

16. **Price Calculation Verification**
    - Confirm that the service request shows the correct total price
    - Expected: $21.00 (2 hours × $10.50 per hour)

### 📊 Service Analytics and Tracking

#### Most Requested Services
17. **Most Requested Services Page**
    - Verify there is a page showing the most popular services across the platform

#### All-in-One Company Testing
18. **All-in-One Company Service Creation**
    - Log out and register a new "All in One" Company
    - Navigate to the service creation page
    - Confirm that all service categories are available for selection

19. **Service Popularity Tracking**
    - Create a new Painting service
    - Log out from Company account and log in as a Customer
    - Request the same Painting service twice
    - Navigate to the most requested services page
    - Verify that the service list updates to reflect the new requests

## ⚡ Basic Code Quality Requirements

### Code Standards
- **Code Quality Compliance**: Ensure the codebase follows established best practices and coding standards

## 🎁 Bonus Features Evaluation

### Additional Functionality
- **Service Rating System**: Check if customers can rate services they have used
- **Pagination System**: Verify if service listing pages implement pagination for better user experience
- **Additional Features**: Identify any extra functionality beyond the core requirements
- **Custom Design Implementation**: Evaluate if the project includes original design and user interface elements