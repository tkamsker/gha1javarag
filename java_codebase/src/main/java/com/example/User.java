package com.example;

/**
 * Represents a user in the system
 */
public class User {
    private final String username;
    private final String passwordHash;
    private String email;

    /**
     * Constructor for User
     * @param username The username
     * @param passwordHash The hashed password
     * @param email The email address
     */
    public User(String username, String passwordHash, String email) {
        this.username = username;
        this.passwordHash = passwordHash;
        this.email = email;
    }

    /**
     * Gets the username
     * @return The username
     */
    public String getUsername() {
        return username;
    }

    /**
     * Gets the password hash
     * @return The password hash
     */
    public String getPasswordHash() {
        return passwordHash;
    }

    /**
     * Gets the email address
     * @return The email address
     */
    public String getEmail() {
        return email;
    }

    /**
     * Sets the email address
     * @param email The new email address
     */
    public void setEmail(String email) {
        this.email = email;
    }
} 