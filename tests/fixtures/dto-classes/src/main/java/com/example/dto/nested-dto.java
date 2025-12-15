package com.example.dto;

import java.io.Serializable;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.util.List;

/**
 * DTO with nested DTO fields for testing nested DTO identification.
 */
public class OrderDTO implements Serializable {

    private static final long serialVersionUID = 1L;

    @NotNull
    private Long orderId;

    @NotNull
    @Valid
    private CustomerDTO customer;

    @NotNull
    @Size(min = 1)
    @Valid
    private List<OrderItemDTO> items;

    @Valid
    private ShippingAddressDTO shippingAddress;

    private String orderStatus;

    private Double totalAmount;

    // Nested DTO classes
    public static class CustomerDTO implements Serializable {
        @NotNull
        private Long customerId;

        @NotNull
        private String customerName;

        private String email;

        // Getters and setters
        public Long getCustomerId() {
            return customerId;
        }

        public void setCustomerId(Long customerId) {
            this.customerId = customerId;
        }

        public String getCustomerName() {
            return customerName;
        }

        public void setCustomerName(String customerName) {
            this.customerName = customerName;
        }

        public String getEmail() {
            return email;
        }

        public void setEmail(String email) {
            this.email = email;
        }
    }

    public static class OrderItemDTO implements Serializable {
        @NotNull
        private Long productId;

        @NotNull
        private String productName;

        @NotNull
        @Min(1)
        private Integer quantity;

        private Double price;

        // Getters and setters omitted for brevity
    }

    public static class ShippingAddressDTO implements Serializable {
        private String street;
        private String city;
        private String state;
        private String zipCode;
        private String country;

        // Getters and setters omitted for brevity
    }

    // Getters and setters
    public Long getOrderId() {
        return orderId;
    }

    public void setOrderId(Long orderId) {
        this.orderId = orderId;
    }

    public CustomerDTO getCustomer() {
        return customer;
    }

    public void setCustomer(CustomerDTO customer) {
        this.customer = customer;
    }

    public List<OrderItemDTO> getItems() {
        return items;
    }

    public void setItems(List<OrderItemDTO> items) {
        this.items = items;
    }

    public ShippingAddressDTO getShippingAddress() {
        return shippingAddress;
    }

    public void setShippingAddress(ShippingAddressDTO shippingAddress) {
        this.shippingAddress = shippingAddress;
    }

    public String getOrderStatus() {
        return orderStatus;
    }

    public void setOrderStatus(String orderStatus) {
        this.orderStatus = orderStatus;
    }

    public Double getTotalAmount() {
        return totalAmount;
    }

    public void setTotalAmount(Double totalAmount) {
        this.totalAmount = totalAmount;
    }
}
