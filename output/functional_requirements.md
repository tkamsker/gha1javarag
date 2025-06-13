# Functional Requirements

## Overview
This section describes the functional requirements of the system, organized by feature categories.


### USERMANAGEMENT Requirements

| Feature ID | Title | Description | Priority |
|------------|-------|-------------|----------|
| FR-UserManagement-001 | Comprehensive User and Staff Management Functionality | The system must provide secure interfaces and workflows to support registration, authentication, and profile management for all user and staff types, including doctors, patients, receptionists, and workers. Administrators must have the ability to register and log in, while regular users (patients, staff) can create accounts, log in, and update their profiles (where applicable). | High |

#### FR-UserManagement-001: Comprehensive User and Staff Management Functionality

**Description:** The system must provide secure interfaces and workflows to support registration, authentication, and profile management for all user and staff types, including doctors, patients, receptionists, and workers. Administrators must have the ability to register and log in, while regular users (patients, staff) can create accounts, log in, and update their profiles (where applicable).

**Acceptance Criteria:**
- The system must allow an administrator to register a new account using valid credentials, with successful registration confirmed by a message and database record.
- An administrator must be able to log in with credentials tied to the Admin role. Invalid credentials must return an appropriate error message.
- System must allow patients to register and create new accounts, requiring valid personal information.
- Patients must be able to update their profile information, with all changes saved and reflected in their next login session.
- The system must provide interfaces for adding new doctors, receptionists, and workers, each with validation for data fields specific to their roles.
- All user types (staff and patients) must be able to log in securely. On failed authentication attempts, users receive descriptive error feedback.
- New account registration, login, and worker/staff addition must include input validation and prevent duplicate accounts based on unique identifiers.
- Sessions must be securely managed for all user types post-login.

**Dependencies:**
- FR-Security-001 (Authentication System)
- FR-Database-001 (User Data Storage and Retrieval)
- FR-Validation-001 (Input Validation and Sanitization)

**Source:** ['Controller::AddDoctor', 'Controller::AddPatient', 'Controller::AddRecp', 'Controller::AddWorker', 'Controller::AdminLogin', 'Controller::AdminRegister', 'Controller::updatePatient', 'Controller::UserLogin', 'Controller::UserRegister']


### AUTHENTICATION Requirements

| Feature ID | Title | Description | Priority |
|------------|-------|-------------|----------|
| FR-Authentication-001 | Unified User Management and Authentication for Healthcare System | Implement robust HTTP POST endpoints to manage the registration, login, and profile updating of multiple user roles in the healthcare system, including doctors, patients, receptionists, workers, and administrators. Each endpoint should securely handle incoming requests, validate input data, manage user sessions, and interact with the backend database to persist or update user information. The system must ensure data integrity and role-based access control throughout authentication and registration processes. | High |

#### FR-Authentication-001: Unified User Management and Authentication for Healthcare System

**Description:** Implement robust HTTP POST endpoints to manage the registration, login, and profile updating of multiple user roles in the healthcare system, including doctors, patients, receptionists, workers, and administrators. Each endpoint should securely handle incoming requests, validate input data, manage user sessions, and interact with the backend database to persist or update user information. The system must ensure data integrity and role-based access control throughout authentication and registration processes.

**Acceptance Criteria:**
- All roles (doctor, patient, receptionist, worker, admin) can register via dedicated POST endpoints with valid data.
- All roles can log in using validated credentials and obtain a new session/token.
- Patient profiles can be updated via POST with data validation and confirmation.
- User password fields are always stored securely (e.g., hashed, salted) in the database.
- System responds with appropriate error codes and messages for invalid registration, login, or update attempts.
- Users cannot register with duplicate unique identifiers (e.g., usernames, emails).
- Role-based access is enforced for registration, login, and profile update endpoints.

**Dependencies:**
- FR-Database-001: Backend Database Schema for User Roles and Credentials
- FR-Security-001: Password Hashing and Session Management
- FR-Validation-001: Server-side Validation for User Input

**Source:** Controller (Controller::AddDoctor.doPost, Controller::AddPatient.doPost, Controller::AddRecp.doPost, Controller::AddWorker.doPost, Controller::AdminLogin.doPost, Controller::AdminRegister.doPost, Controller::updatePatient.doPost, Controller::UserLogin.doPost, Controller::UserRegister.doPost)

