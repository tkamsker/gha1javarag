package com.example;

/**
 * Interface for password hashing operations
 */
public interface PasswordHasher {
    /**
     * Hashes a password
     * @param password The password to hash
     * @return The hashed password
     */
    String hash(String password);

    /**
     * Verifies a password against a hash
     * @param password The password to verify
     * @param hash The hash to verify against
     * @return true if the password matches the hash
     */
    boolean verify(String password, String hash);
} 