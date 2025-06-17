package com.example.service;

import java.util.List;
import java.util.Optional;
import javax.persistence.EntityNotFoundException;

/**
 * Service class for managing user operations.
 * Handles user creation, authentication, and profile management.
 */
public class UserService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final EmailService emailService;

    public UserService(UserRepository userRepository, 
                      PasswordEncoder passwordEncoder,
                      EmailService emailService) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.emailService = emailService;
    }

    /**
     * Creates a new user account.
     * @param user The user details
     * @return The created user
     * @throws IllegalArgumentException if user already exists
     */
    public User createUser(User user) {
        // Business Rule: Username must be unique
        if (userRepository.findByUsername(user.getUsername()).isPresent()) {
            throw new IllegalArgumentException("Username already exists");
        }

        // Business Rule: Password must be at least 8 characters
        if (user.getPassword().length() < 8) {
            throw new IllegalArgumentException("Password must be at least 8 characters");
        }

        // Encode password before saving
        user.setPassword(passwordEncoder.encode(user.getPassword()));
        
        // Save user
        User savedUser = userRepository.save(user);
        
        // Send welcome email
        emailService.sendWelcomeEmail(user.getEmail());
        
        return savedUser;
    }

    /**
     * Updates user profile information.
     * @param userId The user ID
     * @param updates The profile updates
     * @return The updated user
     * @throws EntityNotFoundException if user not found
     */
    public User updateProfile(Long userId, UserProfileUpdates updates) {
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new EntityNotFoundException("User not found"));
            
        // Update allowed fields
        if (updates.getEmail() != null) {
            user.setEmail(updates.getEmail());
        }
        if (updates.getDisplayName() != null) {
            user.setDisplayName(updates.getDisplayName());
        }
        
        return userRepository.save(user);
    }

    /**
     * Authenticates a user.
     * @param username The username
     * @param password The password
     * @return Optional containing the user if authentication successful
     */
    public Optional<User> authenticate(String username, String password) {
        return userRepository.findByUsername(username)
            .filter(user -> passwordEncoder.matches(password, user.getPassword()));
    }

    /**
     * Retrieves all active users.
     * @return List of active users
     */
    public List<User> getActiveUsers() {
        return userRepository.findByStatus(UserStatus.ACTIVE);
    }

    /**
     * Deactivates a user account.
     * @param userId The user ID
     * @throws EntityNotFoundException if user not found
     */
    public void deactivateUser(Long userId) {
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new EntityNotFoundException("User not found"));
            
        user.setStatus(UserStatus.INACTIVE);
        userRepository.save(user);
        
        // Notify user via email
        emailService.sendAccountDeactivationEmail(user.getEmail());
    }
} 