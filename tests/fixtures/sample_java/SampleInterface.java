package com.example.test.api;

import java.util.List;
import java.util.Optional;

/**
 * Sample interface for testing.
 */
public interface SampleInterface {

    /**
     * Process items.
     */
    void processItems(List<String> items);

    /**
     * Find item by ID.
     */
    Optional<String> findById(Long id);

    /**
     * Get count.
     */
    default int getDefaultCount() {
        return 0;
    }
}
