package com.example.test.service;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;
import javax.annotation.PostConstruct;
import java.util.List;

/**
 * Sample annotated class for testing.
 */
@Service
@SuppressWarnings("unchecked")
public class AnnotatedClass {

    @Autowired
    private SampleRepository repository;

    @PostConstruct
    public void init() {
        // Initialization
    }

    @Deprecated
    public void oldMethod() {
        // Old implementation
    }

    @Override
    public String toString() {
        return "AnnotatedClass";
    }
}
