package com.example.shared;

import com.google.gwt.user.client.rpc.IsSerializable;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import javax.validation.constraints.Email;
import javax.validation.constraints.Pattern;
import java.io.Serializable;
import java.util.List;
import java.util.Set;

/**
 * Data Transfer Object for User.
 *
 * Demonstrates nested DTO references and complex validation.
 */
public class UserDTO implements Serializable, IsSerializable {

    private static final long serialVersionUID = 1L;

    /**
     * User ID.
     */
    private Long id;

    /**
     * Username (required, 3-20 alphanumeric characters).
     */
    @NotNull(message = "Username is required")
    @Size(min = 3, max = 20, message = "Username must be between 3 and 20 characters")
    @Pattern(regexp = "^[a-zA-Z0-9_]+$", message = "Username must be alphanumeric")
    private String username;

    /**
     * Email address (required, valid email format).
     */
    @NotNull(message = "Email is required")
    @Email(message = "Email must be valid")
    private String email;

    /**
     * First name.
     */
    @Size(max = 50, message = "First name must be less than 50 characters")
    private String firstName;

    /**
     * Last name.
     */
    @Size(max = 50, message = "Last name must be less than 50 characters")
    private String lastName;

    /**
     * User role (ADMIN, USER, GUEST).
     */
    @NotNull(message = "Role is required")
    private String role;

    /**
     * Account active flag.
     */
    private Boolean active;

    /**
     * User profile (nested DTO).
     */
    private UserProfileDTO profile;

    /**
     * User address (nested DTO).
     */
    private AddressDTO address;

    /**
     * List of user permissions (nested DTOs).
     */
    private List<PermissionDTO> permissions;

    /**
     * Set of assigned projects (nested DTOs).
     */
    private Set<ProjectDTO> projects;

    /**
     * Default constructor (required for GWT serialization).
     */
    public UserDTO() {
        this.active = true;
    }

    /**
     * Constructor with required fields.
     */
    public UserDTO(String username, String email, String role) {
        this();
        this.username = username;
        this.email = email;
        this.role = role;
    }

    // Getters and setters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
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

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public Boolean getActive() {
        return active;
    }

    public void setActive(Boolean active) {
        this.active = active;
    }

    public UserProfileDTO getProfile() {
        return profile;
    }

    public void setProfile(UserProfileDTO profile) {
        this.profile = profile;
    }

    public AddressDTO getAddress() {
        return address;
    }

    public void setAddress(AddressDTO address) {
        this.address = address;
    }

    public List<PermissionDTO> getPermissions() {
        return permissions;
    }

    public void setPermissions(List<PermissionDTO> permissions) {
        this.permissions = permissions;
    }

    public Set<ProjectDTO> getProjects() {
        return projects;
    }

    public void setProjects(Set<ProjectDTO> projects) {
        this.projects = projects;
    }

    /**
     * Get full name.
     */
    public String getFullName() {
        if (firstName != null && lastName != null) {
            return firstName + " " + lastName;
        }
        return username;
    }

    @Override
    public String toString() {
        return "UserDTO{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", email='" + email + '\'' +
                ", role='" + role + '\'' +
                '}';
    }

    /**
     * Nested DTO: User Profile.
     */
    public static class UserProfileDTO implements Serializable, IsSerializable {
        private static final long serialVersionUID = 1L;

        private String bio;
        private String avatarUrl;
        private String phoneNumber;

        public UserProfileDTO() {}

        public String getBio() {
            return bio;
        }

        public void setBio(String bio) {
            this.bio = bio;
        }

        public String getAvatarUrl() {
            return avatarUrl;
        }

        public void setAvatarUrl(String avatarUrl) {
            this.avatarUrl = avatarUrl;
        }

        public String getPhoneNumber() {
            return phoneNumber;
        }

        public void setPhoneNumber(String phoneNumber) {
            this.phoneNumber = phoneNumber;
        }
    }

    /**
     * Nested DTO: Address.
     */
    public static class AddressDTO implements Serializable, IsSerializable {
        private static final long serialVersionUID = 1L;

        @Size(max = 100)
        private String street;

        @Size(max = 50)
        private String city;

        @Size(max = 20)
        private String zipCode;

        @Size(max = 50)
        private String country;

        public AddressDTO() {}

        public String getStreet() {
            return street;
        }

        public void setStreet(String street) {
            this.street = street;
        }

        public String getCity() {
            return city;
        }

        public void setCity(String city) {
            this.city = city;
        }

        public String getZipCode() {
            return zipCode;
        }

        public void setZipCode(String zipCode) {
            this.zipCode = zipCode;
        }

        public String getCountry() {
            return country;
        }

        public void setCountry(String country) {
            this.country = country;
        }
    }

    /**
     * Nested DTO: Permission.
     */
    public static class PermissionDTO implements Serializable, IsSerializable {
        private static final long serialVersionUID = 1L;

        @NotNull
        private String name;

        private String description;

        public PermissionDTO() {}

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getDescription() {
            return description;
        }

        public void setDescription(String description) {
            this.description = description;
        }
    }

    /**
     * Nested DTO: Project.
     */
    public static class ProjectDTO implements Serializable, IsSerializable {
        private static final long serialVersionUID = 1L;

        private Long id;

        @NotNull
        @Size(min = 3, max = 100)
        private String name;

        private String status;

        public ProjectDTO() {}

        public Long getId() {
            return id;
        }

        public void setId(Long id) {
            this.id = id;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getStatus() {
            return status;
        }

        public void setStatus(String status) {
            this.status = status;
        }
    }
}
