package com.example.test;

import java.util.List;

/**
 * Sample Java class for testing.
 */
public class SampleClass {

    private String name;
    private int count;

    public SampleClass(String name) {
        this.name = name;
        this.count = 0;
    }

    public String greet(String recipient) {
        return "Hello, " + recipient + " from " + name;
    }

    public void increment() {
        count++;
    }

    public int getCount() {
        return count;
    }
}
