package com.example.test.base;

import java.util.List;

/**
 * Abstract base class for testing.
 */
public abstract class AbstractBaseClass {

    protected String name;

    public AbstractBaseClass(String name) {
        this.name = name;
    }

    /**
     * Abstract method to be implemented.
     */
    public abstract void execute();

    /**
     * Concrete method.
     */
    public String getName() {
        return name;
    }

    /**
     * Static utility method.
     */
    public static boolean isValid(String input) {
        return input != null && !input.isEmpty();
    }
}
