package com.example.service;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;
import com.example.dao.UserDAO;
import com.example.model.User;
import com.example.exception.ValidationException;
import com.example.exception.DuplicateEmailException;

/**
 * Sample service for testing PRD generation.
 * Demonstrates business logic and transaction management.
 */
@Service
public class UserService {

    @Autowired
    private UserDAO userDAO;

    @Autowired
    private EmailService emailService;

    /**
     * Creates a new user account.
     * Validates email uniqueness and sends welcome email.
     *
     * @param email User email address
     * @param password Plain text password (will be hashed)
     * @param firstName User's first name
     * @param lastName User's last name
     * @return Created user
     * @throws ValidationException if validation fails
     * @throws DuplicateEmailException if email already exists
     */
    @Transactional
    public User createUser(String email, String password, String firstName, String lastName)
            throws ValidationException, DuplicateEmailException {

        // Validate email format
        if (!isValidEmail(email)) {
            throw new ValidationException("Invalid email format");
        }

        // Check for duplicate email
        if (userDAO.findByEmail(email) != null) {
            throw new DuplicateEmailException("Email already exists");
        }

        // Validate password strength
        if (!isStrongPassword(password)) {
            throw new ValidationException("Password must be at least 8 characters");
        }

        // Create user
        User user = new User();
        user.setEmail(email);
        user.setPasswordHash(hashPassword(password));
        user.setFirstName(firstName);
        user.setLastName(lastName);
        user.setCreatedAt(new Date());
        user.setIsActive(true);

        // Save to database
        user = userDAO.save(user);

        // Send welcome email
        emailService.sendWelcomeEmail(user);

        return user;
    }

    /**
     * Authenticates a user by email and password.
     *
     * @param email User email
     * @param password Plain text password
     * @return User if authentication successful
     * @throws AuthenticationException if credentials invalid
     */
    public User authenticate(String email, String password) throws AuthenticationException {
        User user = userDAO.findByEmail(email);

        if (user == null || !user.getIsActive()) {
            throw new AuthenticationException("Invalid credentials");
        }

        if (!verifyPassword(password, user.getPasswordHash())) {
            throw new AuthenticationException("Invalid credentials");
        }

        return user;
    }

    /**
     * Updates user profile information.
     *
     * @param userId User ID
     * @param firstName New first name
     * @param lastName New last name
     * @return Updated user
     */
    @Transactional
    public User updateProfile(Long userId, String firstName, String lastName) {
        User user = userDAO.findById(userId);

        if (user == null) {
            throw new IllegalArgumentException("User not found");
        }

        user.setFirstName(firstName);
        user.setLastName(lastName);
        user.setUpdatedAt(new Date());

        return userDAO.save(user);
    }

    /**
     * Deactivates a user account.
     *
     * @param userId User ID
     */
    @Transactional
    public void deactivateUser(Long userId) {
        User user = userDAO.findById(userId);

        if (user != null) {
            user.setIsActive(false);
            user.setUpdatedAt(new Date());
            userDAO.save(user);
        }
    }

    // Private helper methods
    private boolean isValidEmail(String email) {
        return email != null && email.matches("^[A-Za-z0-9+_.-]+@(.+)$");
    }

    private boolean isStrongPassword(String password) {
        return password != null && password.length() >= 8;
    }

    private String hashPassword(String password) {
        // BCrypt hashing (simplified for example)
        return "hashed_" + password;
    }

    private boolean verifyPassword(String plaintext, String hashed) {
        return hashPassword(plaintext).equals(hashed);
    }
}
