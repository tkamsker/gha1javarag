package com.example.dto;

import java.io.Serializable;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;
import javax.validation.constraints.Min;
import javax.validation.constraints.Max;
import javax.validation.constraints.Email;
import javax.validation.constraints.Pattern;

/**
 * Standard DTO example with JSR-303 validation annotations.
 * Used for testing DTO classification and annotation extraction.
 */
public class UserDTO implements Serializable {

    private static final long serialVersionUID = 1L;

    @NotNull
    @Min(value = 1)
    private Long userId;

    @NotBlank
    @Size(min = 3, max = 50)
    @Pattern(regexp = "[A-Za-z0-9_]+")
    private String username;

    @NotNull
    @Email
    @Size(max = 100)
    private String email;

    @Size(min = 10, max = 15)
    @Pattern(regexp = "\\d{10,15}")
    private String phoneNumber;

    @Min(value = 18)
    @Max(value = 120)
    private Integer age;

    private String firstName;

    private String lastName;

    // Getters and setters
    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    @Override
    public String toString() {
        return "UserDTO{" +
                "userId=" + userId +
                ", username='" + username + '\'' +
                ", email='" + email + '\'' +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        UserDTO userDTO = (UserDTO) o;
        return userId != null ? userId.equals(userDTO.userId) : userDTO.userId == null;
    }

    @Override
    public int hashCode() {
        return userId != null ? userId.hashCode() : 0;
    }
}
