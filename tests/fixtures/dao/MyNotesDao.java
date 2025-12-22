package com.example.dao;

import javax.persistence.*;
import java.util.Date;
import java.util.List;

/**
 * DAO with @JoinColumn foreign key annotations for testing FK extraction
 */
@Entity
@Table(name = "my_notes")
public class MyNotesDao {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "note_id")
    private Long noteId;

    @Column(name = "title", nullable = false, length = 255)
    private String title;

    @Column(name = "content", columnDefinition = "TEXT")
    private String content;

    @Column(name = "created_at")
    @Temporal(TemporalType.TIMESTAMP)
    private Date createdAt;

    @Column(name = "updated_at")
    @Temporal(TemporalType.TIMESTAMP)
    private Date updatedAt;

    // Foreign key to users table
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", referencedColumnName = "id", nullable = false)
    private UserDao user;

    // Foreign key to categories table
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id", referencedColumnName = "id")
    private CategoryDao category;

    // Foreign key to projects table
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id", referencedColumnName = "project_id")
    private ProjectDao project;

    @Column(name = "is_archived")
    private Boolean isArchived = false;

    @Column(name = "priority")
    private Integer priority;

    // Getters and Setters
    public Long getNoteId() {
        return noteId;
    }

    public void setNoteId(Long noteId) {
        this.noteId = noteId;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
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

    public UserDao getUser() {
        return user;
    }

    public void setUser(UserDao user) {
        this.user = user;
    }

    public CategoryDao getCategory() {
        return category;
    }

    public void setCategory(CategoryDao category) {
        this.category = category;
    }

    public ProjectDao getProject() {
        return project;
    }

    public void setProject(ProjectDao project) {
        this.project = project;
    }

    public Boolean getIsArchived() {
        return isArchived;
    }

    public void setIsArchived(Boolean isArchived) {
        this.isArchived = isArchived;
    }

    public Integer getPriority() {
        return priority;
    }

    public void setPriority(Integer priority) {
        this.priority = priority;
    }
}
