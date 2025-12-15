package com.example.shared;

import com.google.gwt.user.client.rpc.IsSerializable;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.io.Serializable;
import java.util.Date;

/**
 * Data Transfer Object for Flash Information.
 *
 * Shared between client and server.
 * Implements GWT serialization and includes validation annotations.
 */
public class FlashInfoDTO implements Serializable, IsSerializable {

    private static final long serialVersionUID = 1L;

    /**
     * Unique identifier.
     */
    private Long id;

    /**
     * Flash title (required, 3-100 characters).
     */
    @NotNull(message = "Title is required")
    @Size(min = 3, max = 100, message = "Title must be between 3 and 100 characters")
    private String title;

    /**
     * Flash description.
     */
    @Size(max = 500, message = "Description must be less than 500 characters")
    private String description;

    /**
     * Category code.
     */
    @NotNull(message = "Category is required")
    private String category;

    /**
     * Priority level (LOW, MEDIUM, HIGH, CRITICAL).
     */
    private String priority;

    /**
     * Active flag.
     */
    @NotNull(message = "Active flag is required")
    private Boolean active;

    /**
     * Send notification flag.
     */
    private Boolean sendNotification;

    /**
     * Expiration date.
     */
    private Date expirationDate;

    /**
     * Author name.
     */
    @Size(max = 50, message = "Author name must be less than 50 characters")
    private String author;

    /**
     * Creation timestamp.
     */
    private Date createdAt;

    /**
     * Last update timestamp.
     */
    private Date updatedAt;

    /**
     * Default constructor (required for GWT serialization).
     */
    public FlashInfoDTO() {
        // Default constructor for serialization
    }

    /**
     * Constructor with required fields.
     */
    public FlashInfoDTO(String title, String category) {
        this.title = title;
        this.category = category;
        this.active = true;
        this.sendNotification = false;
    }

    // Getters and setters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getPriority() {
        return priority;
    }

    public void setPriority(String priority) {
        this.priority = priority;
    }

    public Boolean getActive() {
        return active;
    }

    public void setActive(Boolean active) {
        this.active = active;
    }

    public Boolean getSendNotification() {
        return sendNotification;
    }

    public void setSendNotification(Boolean sendNotification) {
        this.sendNotification = sendNotification;
    }

    public Date getExpirationDate() {
        return expirationDate;
    }

    public void setExpirationDate(Date expirationDate) {
        this.expirationDate = expirationDate;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public Date getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

    public Date getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(Date updatedAt) {
        this.updatedAt = updatedAt;
    }

    @Override
    public String toString() {
        return "FlashInfoDTO{" +
                "id=" + id +
                ", title='" + title + '\'' +
                ", category='" + category + '\'' +
                ", active=" + active +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        FlashInfoDTO that = (FlashInfoDTO) o;

        return id != null ? id.equals(that.id) : that.id == null;
    }

    @Override
    public int hashCode() {
        return id != null ? id.hashCode() : 0;
    }
}
