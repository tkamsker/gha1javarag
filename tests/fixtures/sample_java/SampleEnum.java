package com.example.test.enums;

/**
 * Sample enum for testing.
 */
public enum SampleEnum {
    ACTIVE("Active status"),
    INACTIVE("Inactive status"),
    PENDING("Pending status");

    private final String description;

    SampleEnum(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }
}
