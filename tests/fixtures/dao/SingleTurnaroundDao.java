package com.example.dao;

import java.util.List;
import java.util.Date;

/**
 * DAO with SQL JOIN statements containing foreign key relationships.
 * Foreign keys are extracted from inline SQL JOIN clauses.
 */
public class SingleTurnaroundDao {

    private Long turnaroundId;
    private String turnaroundCode;
    private Long salesInfoId;  // FK to sales_info table
    private Long customerId;  // FK to customers table
    private Date startDate;
    private Date endDate;
    private String status;
    private Double totalAmount;

    // SQL query with JOIN for FK extraction testing
    private static final String FIND_BY_CUSTOMER_SQL =
        "SELECT t.turnaround_id, t.turnaround_code, t.sales_info_id, t.customer_id, " +
        "t.start_date, t.end_date, t.status, t.total_amount, " +
        "s.sales_rep_name, c.customer_name " +
        "FROM single_turnaround t " +
        "JOIN sales_info s ON t.sales_info_id = s.sales_info_id " +
        "JOIN customers c ON t.customer_id = c.customer_id " +
        "WHERE t.customer_id = ? AND t.status = ?";

    // SQL query with multiple JOINs
    private static final String FIND_WITH_DETAILS_SQL =
        "SELECT t.*, s.*, c.*, p.* " +
        "FROM single_turnaround t " +
        "INNER JOIN sales_info s ON t.sales_info_id = s.id " +
        "INNER JOIN customers c ON t.customer_id = c.id " +
        "LEFT JOIN products p ON t.product_id = p.product_id " +
        "WHERE t.turnaround_id = ?";

    // SQL query with complex JOIN conditions
    private static final String FIND_BY_DATE_RANGE_SQL =
        "SELECT t.turnaround_id, t.turnaround_code, t.customer_id " +
        "FROM single_turnaround t " +
        "JOIN sales_info s ON (t.sales_info_id = s.sales_info_id AND s.is_active = 1) " +
        "JOIN customers c ON (t.customer_id = c.customer_id) " +
        "WHERE t.start_date >= ? AND t.end_date <= ?";

    public SingleTurnaroundDao() {
    }

    // Getters and Setters
    public Long getTurnaroundId() {
        return turnaroundId;
    }

    public void setTurnaroundId(Long turnaroundId) {
        this.turnaroundId = turnaroundId;
    }

    public String getTurnaroundCode() {
        return turnaroundCode;
    }

    public void setTurnaroundCode(String turnaroundCode) {
        this.turnaroundCode = turnaroundCode;
    }

    public Long getSalesInfoId() {
        return salesInfoId;
    }

    public void setSalesInfoId(Long salesInfoId) {
        this.salesInfoId = salesInfoId;
    }

    public Long getCustomerId() {
        return customerId;
    }

    public void setCustomerId(Long customerId) {
        this.customerId = customerId;
    }

    public Date getStartDate() {
        return startDate;
    }

    public void setStartDate(Date startDate) {
        this.startDate = startDate;
    }

    public Date getEndDate() {
        return endDate;
    }

    public void setEndDate(Date endDate) {
        this.endDate = endDate;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Double getTotalAmount() {
        return totalAmount;
    }

    public void setTotalAmount(Double totalAmount) {
        this.totalAmount = totalAmount;
    }

    // Business methods that use SQL queries
    public List<SingleTurnaroundDao> findByCustomer(Long customerId, String status) {
        // SQL execution using FIND_BY_CUSTOMER_SQL
        // Foreign keys: t.sales_info_id = s.sales_info_id, t.customer_id = c.customer_id
        return null;  // Placeholder
    }

    public SingleTurnaroundDao findWithDetails(Long turnaroundId) {
        // SQL execution using FIND_WITH_DETAILS_SQL
        // Foreign keys: multiple JOIN conditions
        return null;  // Placeholder
    }

    public List<SingleTurnaroundDao> findByDateRange(Date start, Date end) {
        // SQL execution using FIND_BY_DATE_RANGE_SQL
        return null;  // Placeholder
    }
}
