

# The User Management System Final Project: Your Epic Coding Adventure Awaits! 🎉✨🔥

## Introduction: Buckle Up for the Ride of a Lifetime 🚀🎬

Welcome to the User Management System project - an epic open-source adventure crafted by the legendary Professor Keith Williams for his rockstar students at NJIT! 🏫👨‍🏫⭐ This project is your gateway to coding glory, providing a bulletproof foundation for a user management system that will blow your mind! 🤯 You'll bridge the gap between the realms of seasoned software pros and aspiring student developers like yourselves. 

# ISSUE: Fix Docker Build Error Related to libc-bin Version Constraint    
## Description:    
The Docker Compose build process failed due to a version constraint on the libc-bin package in the Dockerfile. Specifically, the issue occurred because the specified version of libc-bin conflicted with the system requirements, causing a downgrade without using the --allow-downgrades flag. This led to build errors when running:         
```python
docker compose up --build
```
## Root Cause:         
- The Dockerfile included a hardcoded version constraint for libc-bin (2.36-9+deb12u7).         
- Docker's package management system could not reconcile the specific version during installation.           
- Running without --allow-downgrades caused the build to fail.        

## Key Features of the Fix:          
1. Removal of Specific libc-bin Version Constraint         
- The hardcoded version libc-bin=2.36-9+deb12u7 was removed to allow the latest version of libc-bin to install seamlessly.              

2. Consolidation of Installation Commands         
- Installation of system dependencies and cleanup steps were optimized into a single RUN command, improving efficiency and readability.    

3. Improved Dockerfile Comments            
- Updated comments to ensure clarity about the purpose of each section, aligning with best practices.           

## Benifits:       
- Successful Build: The Docker Compose build process now completes without errors.             
- Future Compatibility: Avoiding a specific version ensures the latest compatible libc-bin version is installed, reducing maintenance overhead.       
- Efficiency: Combining installation commands reduces the number of layers in the Docker image, improving performance and image size.        

## Expected Outcome:      
Users can run the following command to build and run the application successfully:      
```python
docker compose up --build
```
## Files Updated:      
1. Dockerfile         
- Removed the specific version constraint for libc-bin.            
- Combined installation commands for system dependencies and cleanup.          
- Improved inline comments to explain the changes.           

# ISSUE:CI/CD Pipeline Update for GitHub Actions             
## Description:        
This update fixes the GitHub Actions CI/CD pipeline to build and push Docker images to the correct DockerHub repository: mahrokhjozedaemi/final_user_management. It adds multi-platform support (linux/amd64 and linux/arm64) and integrates Trivy for vulnerability scanning with caching to ensure efficient and secure deployments.          

## Enhancements          
1. DockerHub Repository Update
- Updated Docker image repository name to match my DockerHub account:     
mahrokhjozedaemi/final_user_management.          
- The tags and image references now correctly use this repository.      

2. Multi-Platform Build Support             
- Enabled support for linux/amd64 and linux/arm64 platforms using the docker/build-push-action.            
- Ensures the Docker image can run across multiple architectures seamlessly.             

3. Optimized Docker Image Scanning             
- Integrated Trivy vulnerability scanner into the GitHub Actions workflow.          
- Custom installation of Trivy allows greater flexibility, including:
   - Efficient database caching to speed up scans.      
   - Scans configured to identify CRITICAL and HIGH severity vulnerabilities.          
- Ensures the pipeline fails if security vulnerabilities are detected.      
4. Improved Workflow Efficiency              
- Combined installation and runtime commands for optimized performance.          
- Added caching for Trivy databases, reducing scan execution time.       
- Cleaned up redundant configurations for clarity and maintainability.        

## Benefits:       
- Correct Repository Configuration: Docker images are now built and pushed to the correct repository:       
mahrokhjozedaemi/final_user_management.          
- Multi-Platform Compatibility: Supports amd64 and arm64 architectures, increasing image portability.           
- Improved Security: Ensures Docker images are scanned for critical vulnerabilities before deployment.            
- Faster Pipelines: Optimized build, caching, and scanning reduce the overall CI/CD pipeline runtime             

## Expected Outcome        
The GitHub Actions CI/CD pipeline will:
1. Build and push Docker images to the repository:          
mahrokhjozedaemi/final_user_management.
2. Target both linux/amd64 and linux/arm64 platforms.           
3. Scan Docker images for CRITICAL and HIGH vulnerabilities using Trivy.            
4. Fail the workflow if vulnerabilities are detected, ensuring secure production deployments.             

## Files Updated           
- .github/workflows/production.yml          
Updated DockerHub repository name.       
Enabled multi-platform support.         
Added Trivy vulnerability scanning with caching.          

# IISUE: Implement Robust Username Generation and Validation for Enhanced User Management            

## Description:
This section of the project implements robust username management features designed to enhance user experience and ensure data integrity. The implementation supports the automatic generation of unique, URL-safe nicknames for users during creation while allowing users to change their nicknames with validation. It enforces strict uniqueness and format constraints, ensuring compatibility with public-facing identifiers. This functionality improves user anonymity and privacy by assigning meaningful, anonymous nicknames based on a combination of words and numbers.            

## Key Features:
1. Username Generation:          

- Randomly generate nicknames upon user creation.              
- Use a combination of nouns, verbs, and a numeric suffix to ensure meaningful and diverse names.                  

2. Nickname Uniqueness:              
- Validate that no two users share the same nickname.               
- Handle duplicate nickname conflicts during both user creation and updates.
                    
3. URL-Safe Identifier:                  
- Ensure that nicknames are URL-safe, allowing them to be used in public contexts without encoding issues.                      
- Only allow alphanumeric characters, underscores, and hyphens in nicknames.
                          
4. User-Controlled Updates:               
- Allow users to update their nicknames, ensuring the new nickname is both valid and unique.           

5. Privacy and Anonymity:                        
- Assign anonymous nicknames by default to protect user identities.          
- Maintain privacy by validating nicknames against strict rules.          

6. Testing and Verification:                       
- The system includes comprehensive tests to ensure correctness, with plans for additional tests to cover edge cases and rare scenarios.          

## Expected Outcome                
- Users will always have unique nicknames, either system-generated or user-updated.                        
- Nicknames will be compliant with URL-safety standards, ensuring seamless usage in public links.                     
- Conflicts arising from duplicate nicknames during creation or updates will be handled gracefully.                    
- User privacy and anonymity will be safeguarded through anonymous nickname assignments.                       

## Files Update for this issue:                       
The implementation of the nickname management and validation features involved updates to multiple components of the project, reflecting the complexity of the requirements. Below is a detailed explanation of the resolution steps and the specific changes made to each relevant file:

1. app/services/user_service.py                        
Changes Made:                   
Nickname Validation During Creation:                     
- Updated the create method to validate nicknames against database records.       
- Used the generate_nickname() function to generate random nicknames and ensure uniqueness before assigning them to users.            
- Integrated the validate_url_safe_username() function to check the format of nicknames.                      
- Handled duplicate nickname errors gracefully with proper logging and error messages.                       

2. Nickname Validation During Updates:               
- Updated the update method to enforce uniqueness for nicknames during updates.                                 
- Validated that nicknames meet URL-safety standards before saving changes.       

Purpose: Ensure that all nicknames are unique, valid, and compliant with URL-safe standards during user creation and updates.              

3. tests/test_api/test_users_api.py            
Changes Made:             
Test for Duplicate Nickname Creation:
- Added test_create_user_duplicate_nickname to ensure that creating a user with a duplicate nickname fails.                 
- Mocked external email service to focus on nickname validation logic.      

Test for Duplicate Nickname Updates:                          
- Added test_update_user_duplicate_nickname to validate that nickname updates with duplicates are rejected.               
- Used the test client to simulate API calls for creation and updates.          
Purpose: Verify that the API layer correctly handles nickname uniqueness and format validation.            

4. tests/test_services/test_user_service.py              
Changes Made:             
Test for Nickname Creation:           
- Added tests to ensure that generated nicknames are unique and comply with URL-safety rules.             
- Mocked email service to isolate the nickname generation and validation logic.                

Test for Duplicate Nickname Handling:               
- Added test_create_user_duplicate_nickname and test_update_user_duplicate_nickname to validate service-layer logic for handling duplicates.                 

Purpose: Test the internal service logic to ensure correctness and coverage of nickname generation and validation features.                  

5. app/utils/nickname_gen.py                
Changes Made:                  
- Implemented the generate_nickname() function to generate random combinations of nouns, verbs, and numbers.                
- Added utility functions to validate the format and uniqueness of nicknames.                  

- Purpose: Provide a reusable utility to create meaningful and unique nicknames while adhering to project constraints.            

6. app/utils/validators.py          
Changes Made:           
- Added the validate_url_safe_username() function to enforce URL-safe standards for nicknames.               

Purpose: Ensure that nicknames can safely be used as public-facing identifiers in URLs without encoding issues.            

7. tests/conftest.py              
Changes Made:              
- Added new test fixtures to create mock users with unique nicknames for testing.                
- Introduced an admin_user and manager_user fixture for role-based testing of API endpoints.                

Purpose: Facilitate testing of nickname uniqueness and validation in both API and service layers.               

8. app/models/user_model.py            
Changes Made:           
- Updated the User model to enforce uniqueness constraints on the nickname field at the database level.             

Purpose: Add an additional layer of protection against duplicate nicknames, even in concurrent user creation scenarios.             

## Test
Overview
This section outlines the tests implemented to verify the functionalities related to Username Generation and Validation. These tests ensure that the following features are correctly implemented and functional:             

- Username Generation: Automatically generates a random, unique username combining nouns, verbs, and numbers.            
- Uniqueness: Validates that usernames are unique during creation and updates.              
- Validation: Ensures usernames are URL-safe and adhere to format constraints.               
- User Privacy and Anonymity: Keeps usernames secure and private.           
- Edge Case Handling: Handles invalid data gracefully.              

## Pytest        

1. API Tests
File: tests/test_api/test_users_api.py          

Key Tests:          
- test_create_user_duplicate_nickname: Verifies that creating a user with a duplicate nickname fails.             
- test_update_user_duplicate_nickname: Ensures that updating a user to have a duplicate nickname fails.             
- test_create_user_invalid_data: Tests that invalid data (e.g., missing required fields) is handled properly.             


2. Service Tests              
File: tests/test_services/test_user_service.py          

Key Tests:             
- test_create_user_with_valid_data: Ensures valid user data creates a user successfully.                  
- test_create_user_duplicate_email: Confirms duplicate email detection and rejection.               
- test_update_user_duplicate_nickname: Validates that updating to a duplicate nickname is disallowed.                      
- test_update_user_invalid_data: Checks handling of invalid user update data.                     

### Test Results for API Tests
![Test API Results](images/test_api_readme.jpg)

### Test Results for User Service Tests
![Test User Service Results](images/user_service_readme.jpg)


# IISUE: Password Validation and Security Enhancements     
## Enhancement:                  
To ensure the highest level of security for user accounts, we have introduced robust password validation mechanisms. These updates are designed to align with industry standards for secure password practices, minimizing the risk of unauthorized access and protecting user data.          

## Key Features of Password Validation           
1. Minimum Length Requirement              
Passwords must be sufficiently long to enhance resistance to brute-force attacks. A password must contain at least 8 characters to be accepted.             
2. Complexity Requirements          
To ensure passwords are not easily guessable, they must include a mix of different character types:           
- Uppercase Letters: At least one uppercase letter (e.g., A-Z) to strengthen the password.            
- Lowercase Letters: At least one lowercase letter (e.g., a-z) to improve complexity.             
- Numbers: At least one numeric character (e.g., 0-9) is required.           
- Special Characters: To add further complexity, the password must include at least one special character (e.g., !@#$%^&*()_+-=<>?).             
3. Restrictions on Spaces               
Passwords should not contain whitespace characters to maintain consistency and avoid unexpected formatting issues during user input.                
4. Secure Password Storage                
Passwords are securely hashed before being stored in the database using modern cryptographic algorithms. This ensures that even in the unlikely event of a data breach, user passwords remain protected.           
5. Clear Error Messaging              
Validation errors provide users with actionable feedback, ensuring clarity while maintaining security best practices.      

## Benefits of Enhanced Password Validation          
- Improved User Security: The updated validation rules significantly reduce the risk of weak passwords, enhancing the security of user accounts.                 
- Compliance with Best Practices: By requiring a mix of character types and enforcing a minimum length, this approach aligns with established security standards.                
- Anonymized and Protected Data: Proper password hashing ensures that passwords are never stored in plain text, protecting user privacy and data integrity.       

## Expected Outcomes             
These password validation enhancements ensure that all users create strong, secure passwords, mitigating risks associated with weak or compromised credentials. In addition to protecting user accounts, the system provides clear guidelines and helpful error messages, making it user-friendly while maintaining a high level of security.              

All tests related to these features are included and verified to ensure compliance with the updated validation rules.                

## Files Updated for Password Validation Implementation        
To introduce robust password validation mechanisms and enhance user account security, several files were updated in the project. Here’s a summary of the changes:          

1. User Schemas           
Enhanced to include validation rules that enforce minimum password length and complexity requirements. These updates ensure that all user input is thoroughly validated before reaching the database.         

2. User Service          
Modified to handle password validation during user creation and updates. The service ensures proper feedback is provided for invalid passwords and implements secure password hashing before storage.        

3. ecurity Utilities                
Updated to define the core password validation logic. This includes the criteria for password complexity and hashing algorithms for secure storage.                   

4. Configuration File                
Introduced configurable password validation parameters, such as minimum length and complexity requirements, allowing for easier updates and adjustments in the future.                   

5. Test Suite                          
Enhanced to include new test cases that validate the updated password rules. These tests ensure the functionality works as expected under various scenarios, including invalid and valid password inputs.

## Pytest    
![Password Validation Output](images/output%20for%20password%20validation.jpg)

# IISUE:User Uniqueness Validation         
## Enhancement:         
In modern systems, user uniqueness is a cornerstone of both security and usability. This enhancement ensures that users cannot share the same identifiers, such as nicknames or email addresses, providing a more secure, reliable, and seamless experience across the platform.           

## Key Features of User Uniqueness         
This enhancement introduces critical mechanisms to enforce user uniqueness in the system:        

1. Nickname Uniqueness:           
- Validates that each user has a unique nickname during both account creation and updates.         
- Implements a validation layer at the service level to query existing nicknames in the database.        
- Ensures nicknames meet formatting rules while being distinct.          

2. Email Address Uniqueness:            
- Guarantees that every email address is unique and associated with only one user.           
- Prevents duplicate registrations using the same email for multiple accounts.           

3. Error Handling and Messaging:           
- Provides clear, meaningful error messages when a duplicate nickname or email is encountered.       
- Ensures smooth communication between the client and server regarding validation issues.           

## Benefits of User Uniqueness          
The addition of user uniqueness validation delivers several benefits to the platform:            

1. Improved User Experience:             
- Avoids confusion or conflicts caused by duplicate identifiers.              
- Streamlines user interactions by ensuring that all nicknames and emails are distinct.             
- Prevents frustration during registration or profile updates by clearly communicating issues.          

2. Enhanced Security:            
- Eliminates risks of impersonation or unauthorized duplication of accounts.         
- Enforces stricter validation at multiple levels, including schemas and service layers.          

3. Data Integrity:                 
- Prevents inconsistencies in the database caused by duplicate entries.            
- Facilitates faster and more efficient database querying, as unique constraints optimize search operations.                  

4. Scalability:             
- Prepares the system for handling a growing number of users by enforcing strict uniqueness constraints.              
- Avoids bottlenecks in user authentication or management by maintaining clean and distinct data records.             

## Expected Outcome          
The implementation of user uniqueness validation ensures that:          

- Account Creation: Users cannot create an account with a nickname or email already registered in the system. Such attempts will result in a 400 Bad Request error with a detailed message explaining the issue.            
- Account Updates: Users cannot update their profile to use a nickname or email already in use by another account.                   
- Error Clarity: Validation errors are communicated through precise and user-friendly error messages, improving the overall user experience.         
Additionally, these improvements enhance the system’s ability to scale and integrate with other components or services securely and effectively.        

## Files Updated for User Uniqueness          
To implement and test this feature, the following files were updated and enhanced:        

1. Application Layer:          
- app/services/user_service.py:         

  - Added methods is_nickname_unique and is_email_unique to validate uniqueness in the database.         
  - Ensured these methods integrate seamlessly with existing account creation and update functionalities.           

- app/routers/user_routes.py:             
   - Integrated uniqueness checks into the create_user and update_user endpoints.            
   - Ensured API routes properly handle validation errors and communicate these errors to clients.        

2. Schema Layer:               
- app/schemas/user_schemas.py:      
  - Updated validation rules for nicknames and email addresses.        
  - Included constraints for unique identifiers and formatted error messages for better communication.       

3. Testing Layer:           
- tests/test_services/test_user_service.py:         
  - Added unit tests for is_nickname_unique and is_email_unique methods.         
 - Verified service-layer logic handles various scenarios, such as duplicates and valid unique entries.           

- tests/test_routes/test_user_routes.py:
  - Ensured endpoints return appropriate HTTP status codes and error messages for duplicate nicknames and emails.         
  - Tested both positive (valid data) and negative (duplicate or invalid data) scenarios.     

- tests/test_schemas/test_user_schemas.py:        
  - Verified schema validation prevents duplicate nicknames and email addresses.       
  - Included tests for proper error messages and invalid formatting.       

## Summary
This enhancement is a pivotal step forward in ensuring the robustness and reliability of our user management system. By enforcing strict uniqueness constraints at multiple levels, this feature delivers a secure, scalable, and user-friendly experience.         
For more details, review the specific files and tests updated as part of this enhancement.        

## Pytest:      
![User Uniqueness Output](images/user_uniquness.jpg)


# IISUE: Automatically Assign Admin Role to First Registered User        
## Enhancement:        
This enhancement ensures that the first user to register in the application is automatically assigned the ADMIN role. This functionality streamlines the initialization process by eliminating the need for manual configuration or updates to grant admin privileges for the first user.           

## Key Features of This Issue         
1. Automatic Role Assignment: The first user created in the system is assigned the ADMIN role by default, while all subsequent users retain the AUTHENTICATED role.              
2. Database Integrity: Ensures that roles are correctly assigned and persisted in the database with no manual intervention.          
3. Customizable Roles: Utilizes existing role definitions (UserRole) to handle both ADMIN and AUTHENTICATED roles seamlessly.        
4. Backward Compatibility: Maintains existing functionality for user creation, allowing customization and additional roles in the future.           

## Benefits:       
1. Simplified Setup: Reduces the manual steps needed during the initial configuration of the application by automatically assigning the administrator role.          
2. Secure Role Management: Ensures the first user always has the required administrative privileges, improving role integrity.          
3. Improved Developer Experience: Offers clarity and consistency when managing user roles during the development and testing phases.            
4. Ease of Use: For end-users and administrators, the setup is straightforward, reducing the chance of misconfiguration.           

## Expected Outcome       
1. Upon registering the first user, the application will automatically assign the ADMIN role to that user.         
2. All subsequent users will have the default role AUTHENTICATED, unless explicitly updated later.          
3. Role assignment logic is encapsulated within the UserService.create method, ensuring consistent behavior across all user creation pathways.      
4. Updated unit tests validate this behavior, guaranteeing that the logic works as expected during all edge cases.             

## Files Updated for Implementing This Issue          
1. user_service.py           
- Added logic in the UserService.create method to check if the user is the first in the database using the is_first_user method.          
- Updated role assignment logic to assign ADMIN to the first user.          
2. user_model.py          
- Ensured the role column uses an Enum to define roles (ADMIN and AUTHENTICATED) with a default value of AUTHENTICATED.             
3. test_user_service.py          
- Added/Updated tests to validate the following scenarios:
   - The first user is assigned the ADMIN role.         
   - All subsequent users are assigned the AUTHENTICATED role           

## Pytest:      
![First Auto Admin Output](images/first-auto-admin.jpg)


# IISUE: User Bio Update Validation and Error Handling          

## Enhancement:           
This enhancement focuses on improving the validation and error handling mechanisms for the update_user_bio functionality in the user management system. It ensures that API responses are clear, consistent, and informative, making the feature more user-friendly and robust. Validation checks are introduced to verify the presence of the bio field and enforce a maximum length constraint of 500 characters. Additionally, error messages are standardized to provide actionable feedback to API consumers. Comprehensive tests are added to validate the functionality and edge cases, ensuring a reliable and seamless experience for both developers and users.          

## Key Features:          
1. Consistent Error Messages:            
- Error messages for missing or invalid bio fields are now clear, descriptive, and follow consistent capitalization rules.             
- For example: "Field required" and "Bio exceeds maximum length".       

2. Improved Validation Feedback:                
- The API now provides detailed error responses when validation fails, including information about constraints like maximum length.            

3. Comprehensive Test Coverage:                 
- Added and updated test cases to verify validation for missing or invalid bio fields, ensuring robustness and reliability.           

## Benefits:        
1. Improved API Usability:            
- Developers integrating with the API receive clearer, actionable feedback for invalid requests.             
- Error messages include specific details about validation rules, reducing debugging time.              
2. Enhanced User Experience:           
- Clients are less likely to encounter unclear or ambiguous error messages when updating user bios.              
3. Increased Reliability:              
- Comprehensive test coverage ensures that updates to the bio validation logic function as expected across various scenarios.          

## Expected Outcome         
- Clearer Error Responses: Error messages for validation failures are consistent and provide detailed feedback.           
- Seamless Integration: API clients can easily integrate and debug issues related to bio updates.            
- Higher Test Coverage: Robust test cases ensure reliable behavior and prevent regressions in future updates.          

## Files Updated for Implementing This Issue           
1. user_routes.py:           
- Updated the update_user_bio endpoint to include improved error messages and validation logic.           
2. user_schemas.py:            
- Enhanced validation rules for the UpdateBioRequest schema, ensuring clearer error feedback.           
3. user_service.py:          
- Added specific validation checks for the bio field within the update method, ensuring consistent handling across services.            
4. test_user_routes.py:               
- Revised test cases for the update_user_bio endpoint to cover:        
   - Missing bio field.                
   - bio field exceeding the maximum length.          
   - Valid and invalid scenarios for unauthorized requests.            
5. test_user_service.py:            
- Added test cases for service-level validation of the bio field.            
- Verified behavior for valid, missing, and excessively long bio values.      

## Pytest:        
![Description of Image](images/issue_update_field1.jpg)

# IISUE: Ensure Admin User Exists and Streamline /login Authentication Logic     

## Enhancement:       
The /login logic in user_routes.py was repeated multiple times, making the code redundant and harder to maintain. Additionally, authenticating as an admin user through Swagger (using the Authorize button) was not functioning as expected. This issue ensures the admin user (admin@example.com) is dynamically seeded into the database during migrations or tests, reducing code duplication and enabling secure and consistent authentication.           

## Benefits         
- Test Reliability: Ensures that tests for the /login endpoint consistently pass by dynamically creating the required admin user during test setup or database migrations.            
- Streamlined Logic: Removes redundancy in the /login logic, making the code more maintainable and easier to extend.           
- Secure API Testing: Allows successful admin authentication in Swagger, enhancing the ability to test and use the API securely.            
- Improved Accuracy: Reflects real-world scenarios for authenticating users via the /login endpoint, including robust password validation.           

## Expected Outcome         
- Swagger Authorization: Admin users should successfully authenticate using the Swagger Authorize button, improving the API testing experience.      
- Login Endpoint: The /login endpoint will securely and consistently handle authentication without redundant code.          
- Test Success: Tests for the /login endpoint, including test_login_success, will succeed and reliably validate endpoint behavior.           

## Files Updated for Implementing This Issue          
1. user_routes.py:           
- Refactored /login logic to eliminate redundancy while maintaining secure and consistent authentication.            

2. tests/test_routes/test_user_routes.py:        
- Updated the test_login_success test to ensure the admin user (admin@example.com) is fetched dynamically from the database and authenticated securely.             

3. alembic/versions/25d814bc83ed_initial_migration.py:            
- Modified the Alembic migration to seed the admin@example.com user during database migrations, ensuring it exists for both development and test environments.               
4. conftest.py:               
- Verified and maintained fixtures to support dynamic seeding of the admin user during test execution.

## Implementation Summary         
This update addresses challenges in the /login logic, improves the Swagger authentication experience, and ensures all tests for the endpoint pass by dynamically seeding the admin user during migrations or tests. This streamlining of logic reduces redundancy and enhances the maintainability of the codebase.         

## Pyest:       
![Description of Image](images/issue-fix%20Swagger%20Authorization-2.jpg)


# FEATURE: Search and Filtering Capabilities for User Management           
## Description:        
This feature allows administrators to search and filter users based on various criteria, such as username, email, role, account status (locked/unlocked), and registration date range. The system supports both basic search using query parameters and advanced search using dynamic JSON filters. Results are paginated for efficient navigation, and dynamic pagination links (next, prev, first, last) are provided to enhance usability.           

The implementation adheres to RESTful principles and offers clean, discoverable API responses. It also lays the groundwork for future enhancements like full-text search using ElasticSearch and user-friendly frontend integration.                         

## User Story:       
As an administrator, I want to be able to:           

1. Search for users by username, email, or role.          
2. Filter users based on account status or registration date range.        
3. Navigate through filtered results using pagination.       
4. Perform advanced searches with multiple dynamic filters for flexibility.       


## Viable Features:        
1. Search Functionality: Search for users using username, email, and role.         
2. Filtering Options: Filter users based on account status and registration date range.    
3. Advanced Search: Allow dynamic filter combinations with JSON input.        
4. Pagination: Integrate offset-based pagination with navigation links (next, prev, first, last).        
5. Clean API Responses: Return user-friendly and discoverable API responses.           

1. # Routes (user_routes.py)      
## Title:               
Define the Search and Filtering Endpoint.           

## Description:        
Two endpoints are introduced in user_routes.py for user search and filtering:
1. /users-basic (GET): Supports simple searches using query parameters.           
2. /users-advanced (POST): Provides advanced search capabilities by accepting a JSON request body for multiple filters.              
These endpoints leverage schemas for input validation, dynamic filtering logic, and pagination utilities to return efficient and clean responses.        

## Expected outcome:          
1. Basic Search (/users-basic):         
- Accepts query parameters like username, email, role, is_locked, and pagination (skip, limit).    
- Returns paginated user data with dynamic pagination links.         

2. Advanced Search (/users-advanced):         
- Accepts a JSON body with filters: created_from, created_to, role, is_locked, etc.       
- Dynamically applies multiple filters to query users efficiently.                  
- Returns paginated results with metadata and the original filters for clarity.                

## Resolution Steps:        
- Added the /users endpoint with the necessary query parameters.            
- Integrated the UserService.search_and_filter_users method for filtering.         
- Included generate_pagination_links to support paginated responses.         

Purpose: Define the API endpoint for search and filtering functionality.        

```python 
@router.get("/users", response_model=UserListResponse, tags=["User Management Requires (Admin or Manager Roles)"])
async def search_users(
    request: Request,
    username: Optional[str] = None,
    email: Optional[str] = None,
    role: Optional[str] = None,
    account_status: Optional[bool] = None,
    registration_date_start: Optional[datetime] = None,
    registration_date_end: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))
):
    """
    Endpoint to search and filter users based on various criteria.
    """
    filters = {
        "username": username,
        "email": email,
        "role": role,
        "account_status": account_status,
        "registration_date_start": registration_date_start,
        "registration_date_end": registration_date_end,
    }
    users, total_users = await UserService.search_and_filter_users(db, filters, skip, limit)
    user_responses = [UserResponse.model_validate(user) for user in users]
    pagination_links = generate_pagination_links(request, skip, limit, total_users)

    return UserListResponse(
        items=user_responses,
        total=total_users,
        page=skip // limit + 1,
        size=len(user_responses),
        links=pagination_links
    )
```
## Tests:      
Covered by API tests in tests/test_api/test_users_api.py.



2. # Service Layer (user_service.py)
## Title:       
Implement Filtering Logic.         

## Description         
This section defines the logic for filtering users based on criteria provided via the API. It interacts with the database and applies filters dynamically.           

## Expected Outcome          
The UserService.search_and_filter_users method should:

1. Apply all filters, including username, email, role, account status, and date range.             
2. Return paginated results along with the total count of users.            

## Resolution Steps          
- Implemented dynamic filtering using SQLAlchemy's query-building capabilities.               
- Added support for pagination using offset and limit.           
- Handled edge cases, such as missing or invalid filter values.           

Purpose: Add the logic to perform filtering and querying of users from the database.          

```python
@staticmethod
async def search_and_filter_users(
    session: AsyncSession, 
    filters: Dict[str, Optional[str]], 
    skip: int, 
    limit: int
) -> Tuple[List[User], int]:
    """
    Search and filter users based on the given criteria.
    """
    query = select(User)

    # Apply filters
    if filters.get("username"):
        query = query.filter(User.nickname.ilike(f"%{filters['username']}%"))
    if filters.get("email"):
        query = query.filter(User.email.ilike(f"%{filters['email']}%"))
    if filters.get("role"):
        query = query.filter(User.role == filters["role"])
    if filters.get("account_status") is not None:
        query = query.filter(User.email_verified == filters["account_status"])
    if filters.get("registration_date_start") and filters.get("registration_date_end"):
        query = query.filter(
            User.created_at.between(filters["registration_date_start"], filters["registration_date_end"])
        )

    # Add pagination
    query = query.offset(skip).limit(limit)

    # Execute the query and count total users
    result = await session.execute(query)
    users = result.scalars().all()

    total_query = select(func.count()).select_from(User)
    total_result = await session.execute(total_query)
    total_users = total_result.scalar()

    return users, total_users
```

## Tests           
Covered by service layer tests in tests/test_service/test_user_service.py.        



3. # Schemas (user_schemas.py)          
## Title:         
Define Request Validation Model.             

## Description           
This section introduces the UserSearchParams schema to validate the query parameters sent to the /users endpoint.              

## Expected Outcome          
The schema should:           
1. Ensure that all query parameters adhere to the expected data types.       
2. Provide example values for API documentation purposes.          

## Resolution Steps            
- Defined the UserSearchParams model using Pydantic.              
- Included fields for username, email, role, account_status, and date range.               

Purpose: Define the models for query parameters and response structure.         

```python
class UserSearchParams(BaseModel):
    username: Optional[str] = Field(None, example="john_doe")
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    role: Optional[UserRole] = Field(None, example="ADMIN")
    account_status: Optional[bool] = Field(None, example=True)
    registration_date_start: Optional[datetime] = Field(None, example="2023-01-01T00:00:00Z")
    registration_date_end: Optional[datetime] = Field(None, example="2023-12-31T23:59:59Z")
```

## Tests              
Implicitly tested via API endpoint tests in tests/test_api/test_users_api.py.          

# Pagination Helper (utils/pagination.py)        
## Title
Generate Pagination Links.           

## Description           
This section adds a helper function, generate_pagination_links, to create navigation links for paginated results.              

## Expected Outcome         
The helper function should:
1. Return next, prev, first, and last page links based on the current pagination state.                
2. Ensure compatibility with query parameters.          

## Resolution Steps          
- Implemented the generate_pagination_links function.             
- Calculated page links dynamically based on skip, limit, and total_items.       

Purpose: Generate pagination links for the API response.          

```python
from typing import Any, Dict
from urllib.parse import urlencode


def generate_pagination_links(
    request: Any, skip: int, limit: int, total_items: int
) -> Dict[str, str]:
    """
    Generate pagination links for API responses.
    """
    base_url = str(request.url).split("?")[0]
    query_params = dict(request.query_params)

    # Calculate the next page link
    if skip + limit < total_items:
        query_params["skip"] = skip + limit
        query_params["limit"] = limit
        next_link = f"{base_url}?{urlencode(query_params)}"
    else:
        next_link = None

    # Calculate the previous page link
    if skip - limit >= 0:
        query_params["skip"] = max(skip - limit, 0)
        query_params["limit"] = limit
        prev_link = f"{base_url}?{urlencode(query_params)}"
    else:
        prev_link = None

    # Calculate the first and last page links
    query_params["skip"] = 0
    first_link = f"{base_url}?{urlencode(query_params)}"

    last_page_skip = (total_items - 1) // limit * limit
    query_params["skip"] = last_page_skip
    last_link = f"{base_url}?{urlencode(query_params)}"

    return {
        "next": next_link,
        "prev": prev_link,
        "first": first_link,
        "last": last_link,
    }
```

5. # Test for Pagination Helper            
## Title           
Validate Pagination Links.           

## Description           
This section tests the behavior of the pagination helper to ensure correct link generation.             

## Expected Outcome         
The test should validate:               
- Correctness of next, prev, first, and last links.            
- Edge cases like the first and last pages.             

## Resolution Steps               
- Created a test for generate_pagination_links with various scenarios.           
- Used a mocked Request object to simulate API requests.            

Purpose: Validate the behavior of the pagination helper.           

```python
import pytest
from starlette.datastructures import QueryParams, URL
from utils.pagination import generate_pagination_links


@pytest.mark.asyncio
async def test_generate_pagination_links():
    class MockRequest:
        def __init__(self, base_url):
            self.url = URL(base_url)
            self.query_params = QueryParams()

    request = MockRequest("http://localhost:8000/users")

    skip = 0
    limit = 10
    total_users = 45

    links = generate_pagination_links(request, skip, limit, total_users)

    assert links["next"] == "http://localhost:8000/users?skip=10&limit=10"
    assert links["prev"] is None
    assert links["first"] == "http://localhost:8000/users?skip=0&limit=10"
    assert links["last"] == "http://localhost:8000/users?skip=40&limit=10"
```

## Tests
Executed the test using pytest.             

6. # Test API Endpoint           
## Title
Validate Search and Filtering Endpoint.              

## Description              
This section tests the /users endpoint to ensure it correctly handles search and filtering requests.              

## Expected Outcome             
The test should:
1. Verify that query parameters are correctly processed.            
2. Ensure the endpoint returns the expected results and pagination links.          

## Resolution Steps              
- Created a test for the /users endpoint with different query parameters.            
- Validated the structure and correctness of the response.              

Purpose: Test the /users endpoint with various search and filter criteria.           

```python
@pytest.mark.asyncio
async def test_search_users_api(async_client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    query_params = {
        "username": "john",
        "role": "ADMIN",
        "account_status": True,
    }

    response = await async_client.get(
        f"/users?{urlencode(query_params)}", headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
```

7. # Test Service Layer           
## Title            
Validate Filtering Logic.          

## Description              
This section tests the filtering logic implemented in UserService.           search_and_filter_users.

## Expected Outcome               
The test should:             
1. Ensure that filters are correctly applied.               
2. Validate that pagination returns the expected number of results.           

## Resolution Steps              
- Created a test for UserService.search_and_filter_users with various filter combinations.            
- Used a fixture to set up mock data.              

Purpose: Test the filtering logic in the service layer.         

```python
@pytest.mark.asyncio
async def test_search_and_filter_users(users_with_same_role_50_users, db_session):
    filters = {"role": "ADMIN"}
    users, total = await UserService.search_and_filter_users(
        db_session, filters, skip=0, limit=10
    )
    assert len(users) == 10
    assert total == 50
```
8. # Test Fixture (tests/conftest.py)             
## Title
Set Up Mock Data.           

## Description             
This section creates mock user data for testing purposes.           

## Expected Outcome         
The fixture should:              
1. Create a predefined set of mock users.             
2. Ensure that the test environment has consistent data.              

## Resolution Steps             
- Defined a fixture to create 50 mock users with the same role.           
- Committed the data to the database session.          

Purpose: Set up data for testing.          

```python
@pytest.fixture(scope="function")
async def users_with_same_role_50_users(db_session: AsyncSession):
    users = []
    for i in range(50):
        user_data = {
            "nickname": f"user_{i}",
            "email": f"user{i}@example.com",
            "role": "ADMIN",
        }
        user = User(**user_data)
        db_session.add(user)
        users.append(user)
    await db_session.commit()
    return users
```
## Tests
Used by service layer tests in tests/test_service/test_user_service.py.       

## Conclusion
The above updates comprehensively implement the feature, meeting all requirements. The code now supports search and filtering by multiple criteria, provides paginated responses, and includes extensive tests to ensure reliability.            



# Tests for User Search and Filtering Feature      
## Overview         
The user search and filtering functionality is tested extensively to ensure it meets the defined requirements and behaves as expected under various conditions. These tests validate the API endpoint, service layer, pagination, and filtering mechanisms. Below is a detailed explanation of each test and its purpose.              

1. ## test_empty_filters_api     

- Purpose:      
Tests the behavior of the API when no filters are provided.            
- Description:         
Simulates an API call with no query parameters. This validates the default behavior of returning all users with pagination applied.             
- Expected Outcome:         
The API should return the default list of users paginated according to the specified limit and skip values.           
- Importance:          
Ensures that the endpoint works even without filters and that pagination is correctly applied by default.          

2. # test_search_users_api          

- Purpose:         
Validates the core functionality of searching for users based on specific criteria like username, role, and account status.         
- Description:           
Sends a request with valid search filters and verifies that the API correctly filters the users.           
- Expected Outcome:           
Only users matching the specified filters should be returned.             
- Importance:            
Verifies that the API handles search parameters correctly and filters the user list as expected.             

3. # test_combination_of_filters:

- Purpose:
Ensures that multiple filters applied together work correctly.         
- Description:          
Combines filters like username, role, and account status in a single request and verifies the response.          
- Expected Outcome:  Only users matching all specified filters should be returned.       
- Importance:        
Validates the API's ability to handle complex queries with multiple filters applied simultaneously.        
4. # test_filter_users_by_email        

- Purpose:          
Tests filtering users based on their email addresses.         
- Description:     
Sends a request with an email filter to ensure the API correctly returns users matching the email criteria.        
- Expected Outcome:        
Users with the specified email should be returned, and no additional users should be included.           
- Importance:       
Verifies that the API accurately handles email-based filters.         

5. # test_filter_users_by_registration_date   

- Purpose:       
Validates filtering users based on their registration date range.      
- Description:         
Uses registration_date_start and registration_date_end to filter users registered within a specific date range.      
- Expected Outcome:        
Only users who registered within the specified range should be included in the response.         
- Importance:          
Ensures that the API supports date-based filtering and that the implementation is accurate.         

6. # test_filter_users_by_account_status     

- Purpose:      
Tests filtering users based on their account status (e.g., verified or unverified).      
- Description:        
Filters users based on their account verification status and validates the API response.       
- Expected Outcome:       
The response should only include users with the specified account status.        
- Importance:       
Verifies that account status filtering is functioning correctly.       

7. # test_filter_users_by_role       
 
 - Purpose:         
 Ensures users can be filtered based on their role (e.g., ADMIN, USER, MANAGER).      
 - Description:      
 Sends a request with a role filter and validates the response.       
 - Expected Outcome:      
 The API should return only users with the specified role.       
 - Importance:       
 Confirms that role-based filtering works as expected.         

 8. # test_search_users_by_username        

 - Purpose:      
 Validates searching for users by their username.        
 - Description:        
 Tests the username search filter to ensure partial matches (using ilike) return the correct users.        
 - Expected Outcome:      
 Users whose usernames match the search string (partially or fully) should be returned.       
 - Importance:       
 Ensures that username-based search functionality is accurate.       

 9. # test_generate_pagination_links       

 - Purpose:        
 Tests the generate_pagination_links helper function.      
 - Description:       
 Verifies that the pagination links for next, prev, first, and last pages are generated correctly based on the total number of users and the current offset.        
 - Expected Outcome:      
 Correct pagination links should be returned for various scenarios.       
 - Importance:        
 Validates the correctness of pagination link generation, ensuring smooth navigation across pages.         

 10. # test_pagination_boundary       

 - Purpose:       
 Ensures the API handles edge cases for pagination correctly.       
 - Description:       
 Tests scenarios like requesting a page beyond the total number of users or when the number of users is less than the page size.        
 - Expected Outcome:        
 The API should handle these scenarios gracefully without errors and return appropriate results (e.g., an empty list for out-of-bound pages).         
 - Importance:        
 Validates that pagination edge cases are handled correctly, ensuring a robust implementation.         

11. # test_filter_users_case_insensitive      

- purpose:         
Verify Case-Insensitive Filtering of Users       
- Description       
The purpose of this test is to ensure that the user search and filtering functionality works correctly regardless of the case of the input provided. User data in the database might have mixed-case values, but administrators or users should be able to search for them without worrying about capitalization. This test verifies that the filtering mechanism is case-insensitive for key fields such as usernames, emails, and roles.       
- Expected Outcome:       
The system should match and return user data even when the case of the search query does not exactly match the case stored in the database.          
- Test Scenario:       
1. A database is preloaded with mock user data that includes usernames, emails, and roles in mixed cases.         
2. The test performs searches using different cases (e.g., all lowercase, all uppercase, mixed case) for:       
- Usernames      
- Emails       
- Roles         
The test validates that the correct user records are returned regardless of the case of the search query.       
- Test Steps:        
- Define filters with varying cases for username, email, and role.          
- Call the search_and_filter_users service with these filters.          
- Assert that the returned results match the expected users, confirming case-insensitive behavior.            

- Results:         
- If the test passes, it confirms that the filtering logic is case-insensitive.       
- If the test fails, it indicates that the service or database query needs to be updated to handle case-insensitive comparisons correctly.              

- Why It’s Important:           
 This test ensures that the application is user-friendly and robust. Users might not always input the exact case when searching for data, and failing to account for this could result in missed results or user frustration. Implementing and validating case-insensitivity improves usability and avoids such pitfalls.        

 12. # test_fetch_all_users       
 - purpose:       
 Verify Fetching All Users Without Filters.    
 - Expected Outcome:       
- The API should return a list of users with proper pagination when no filters are applied.        
- The response should include the total count of users and an array of user items.      
- Test Scenario:          
1. The test sends a GET request to the /users endpoint without any filters, specifying only basic pagination parameters (skip and limit).        
2. It verifies that the response:        
- Has a status code of 200 OK.        
- Contains a key called items representing the list of users.          
- Contains a key called total representing the total number of users in the system.      
- Ensures that items is a list.        
- Test Steps:         
1. Set up the required authorization headers using an admin token.          
2. Specify basic pagination parameters (skip and limit).           
3. Send a GET request to the /users endpoint with these parameters.         
3. Validate the response by asserting:
The status code is 200.          
4. The response includes the items key, and it contains a list.            
5. The total key exists and is a non-negative integer.         
- Results:          
If the test passes:         
- It confirms that the /users endpoint     correctly handles requests without filters.      
- It ensures that the response includes essential data such as the list of users and the total user count.         
If the test fails:      
- It indicates an issue with the endpoint's ability to fetch unfiltered user data or manage pagination.                 
- Why It’s Important:            
 This test validates the core functionality of the /users endpoint. Being able to fetch all users without filters is a fundamental feature that administrators rely on for user management. Ensuring the API can handle this scenario correctly, including providing accurate pagination details, is critical for usability and reliability.         

 13. # test_pagination_edge_cases      
 - purpose:        
 Verify Pagination Utility Handles Edge Cases        
 - Description:          
  This test ensures that the pagination utility (generate_pagination_links) handles edge cases correctly. It validates the behavior of pagination links under specific conditions, ensuring the utility functions as expected in less common scenarios.      
  - Expected Outcome:             
1. The utility should correctly calculate pagination links when the total number of items is less than the specified limit.       
2. The utility should generate correct links when the total number of items is an exact multiple of the limit.               
- Test Scenario:           
1. Case 1: Total items are fewer than the pagination limit.            
- There should be no "next" or "previous" links because all items fit on the first page.           
2. Case 2: Total items are an exact multiple of the pagination limit.              
- The "last" link should correctly point to the last page, ensuring accurate boundary handling.          
- Test Steps:          
 1. Setup: Create a mock request object simulating the API's base URL and query parameters.                  
2. Case 1:
- Generate pagination links with a total number of items less than the limit.       
- Verify that "next" and "prev" links are None.                
3. Case 2:
- Generate pagination links with the total number of items being a multiple of the limit.           
- Verify that the "last" link points to the last page with the correct skip and limit parameters.       
- Results:        
If the test passes:        
It confirms that the pagination utility correctly handles edge cases, ensuring accurate and reliable pagination links.      
If the test fails:          
It indicates issues in the pagination utility, particularly in handling edge scenarios like small datasets or perfectly divisible totals.        
- Why It’s Important:           
Pagination is essential for efficiently navigating large datasets. Edge cases like small datasets or exact multiples of the limit can expose hidden bugs in the pagination logic. This test ensures the utility can handle such scenarios gracefully, providing a consistent user experience.     

14. # test_search_users_pagination       
- purpose:      
 Verifies that the API correctly applies pagination when fetching users.       
 - Description:          
1. This test validates the proper implementation of pagination functionality in the /users API endpoint. It ensures that:           
- The endpoint correctly returns a subset of users based on the skip and limit parameters.        
- The pagination system is working as expected by retrieving different pages of results.       
- Steps Taken:       
1. Headers Setup: The test sets up the Authorization headers with an admin token to access the endpoint.             
2. First Page Test:          
- It sends a request to fetch the first page of users with a skip of 0 and a limit of 5.        
- The test validates that the response returns exactly 5 users and that these users are in the expected range.         
- Second Page Test:         
It sends another request to fetch the next page with a skip of 5 and the same limit of 5.           
The test ensures that the results are different from the first page and validates the count.          
- Expected Outcomes:           
1. The /users endpoint returns users in chunks based on the skip and limit values.      
- The total number of items in the first page matches the limit.         
- The second page results do not overlap with the first page.            
- The test ensures the total key in the response correctly reflects the total count of users in the database.           
- What This Test Verifies:         
1. The endpoint handles skip and limit parameters correctly.         
2. Pagination works seamlessly and doesn't repeat or omit records between pages.         
3. The API provides accurate metadata about the total number of users.            























## Why These Tests Are Important       
- Coverage: These tests collectively ensure that all aspects of user search, filtering, and pagination are thoroughly validated.      
- Error Handling: They confirm the API can gracefully handle invalid inputs and edge cases.            
- Reliability: Ensures the API behaves predictably under different conditions and filters.               
- Scalability: Validates pagination to handle large datasets effectively.           

## Results and Learnings          
From these tests, we verify:         
- The API filters users accurately based on the specified criteria.           
- Pagination works seamlessly, even at boundaries or edge cases.            
- The implementation adheres to the feature requirements, supporting all necessary filters and use cases.            











 







 





































       






















