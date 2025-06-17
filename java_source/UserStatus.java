package com.example.model;

/**
 * Enum representing possible user account statuses.
 */
public enum UserStatus {
    ACTIVE,    // User account is active and can be used
    INACTIVE,  // User account has been deactivated
    SUSPENDED, // User account has been temporarily suspended
    PENDING    // User account is pending activation
} 