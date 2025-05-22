package com.example;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

/**
 * Service class for handling user-related operations
 */
public class UserService {
    private final Map<String, User> users;
    private final PasswordHasher passwordHasher;

    /**
     * Constructor for UserService
     * @param passwordHasher The password hasher to use
     */
    public UserService(PasswordHasher passwordHasher) {
        this.users = new HashMap<>();
        this.passwordHasher = passwordHasher;
    }

    /**
     * Authenticates a user with the given credentials
     * @param username The username to authenticate
     * @param password The password to verify
     * @return Optional containing the authenticated user if successful
     */
    public Optional<User> authenticate(String username, String password) {
        User user = users.get(username);
        if (user != null && passwordHasher.verify(password, user.getPasswordHash())) {
            return Optional.of(user);
        }
        return Optional.empty();
    }

    /**
     * Registers a new user
     * @param username The username for the new user
     * @param password The password for the new user
     * @param email The email for the new user
     * @return The newly created user
     * @throws IllegalArgumentException if the username is already taken
     */
    public User register(String username, String password, String email) {
        if (users.containsKey(username)) {
            throw new IllegalArgumentException("Username already taken");
        }

        String passwordHash = passwordHasher.hash(password);
        User user = new User(username, passwordHash, email);
        users.put(username, user);
        return user;
    }

    /**
     * Updates a user's email address
     * @param username The username of the user to update
     * @param newEmail The new email address
     * @return The updated user
     * @throws IllegalArgumentException if the user is not found
     */
    public User updateEmail(String username, String newEmail) {
        User user = users.get(username);
        if (user == null) {
            throw new IllegalArgumentException("User not found");
        }
        user.setEmail(newEmail);
        return user;
    }
} 