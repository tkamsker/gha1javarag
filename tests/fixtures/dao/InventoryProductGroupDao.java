package com.example.dao;

import java.util.List;
import java.util.Date;

/**
 * DAO with iBATIS XML mappings for foreign key testing.
 * Foreign keys are defined in the companion iBATIS XML file.
 */
public class InventoryProductGroupDao {

    private Long groupId;
    private String groupName;
    private String description;
    private Long productId;  // FK to products table
    private Long warehouseId;  // FK to warehouses table
    private Integer quantity;
    private Date createdAt;
    private Date updatedAt;
    private Boolean isActive;

    // Default constructor
    public InventoryProductGroupDao() {
    }

    // Constructor with required fields
    public InventoryProductGroupDao(String groupName, Long productId, Long warehouseId) {
        this.groupName = groupName;
        this.productId = productId;
        this.warehouseId = warehouseId;
        this.isActive = true;
        this.createdAt = new Date();
    }

    // Getters and Setters
    public Long getGroupId() {
        return groupId;
    }

    public void setGroupId(Long groupId) {
        this.groupId = groupId;
    }

    public String getGroupName() {
        return groupName;
    }

    public void setGroupName(String groupName) {
        this.groupName = groupName;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Long getProductId() {
        return productId;
    }

    public void setProductId(Long productId) {
        this.productId = productId;
    }

    public Long getWarehouseId() {
        return warehouseId;
    }

    public void setWarehouseId(Long warehouseId) {
        this.warehouseId = warehouseId;
    }

    public Integer getQuantity() {
        return quantity;
    }

    public void setQuantity(Integer quantity) {
        this.quantity = quantity;
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

    public Boolean getIsActive() {
        return isActive;
    }

    public void setIsActive(Boolean isActive) {
        this.isActive = isActive;
    }

    @Override
    public String toString() {
        return "InventoryProductGroupDao{" +
                "groupId=" + groupId +
                ", groupName='" + groupName + '\'' +
                ", productId=" + productId +
                ", warehouseId=" + warehouseId +
                ", quantity=" + quantity +
                ", isActive=" + isActive +
                '}';
    }
}
