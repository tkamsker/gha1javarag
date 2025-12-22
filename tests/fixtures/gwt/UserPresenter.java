package com.example.client;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.dom.client.HasClickHandlers;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.rpc.AsyncCallback;
import com.google.gwt.user.client.ui.HasText;
import com.google.gwt.user.client.ui.HasValue;

import com.example.client.place.DashboardPlace;
import com.example.client.place.UserDetailPlace;
import com.example.shared.UserDTO;
import com.example.client.service.UserServiceAsync;

/**
 * GWT Presenter with Display interface for testing MVP pattern detection
 */
public class UserPresenter {

    /**
     * Display interface defining the contract between Presenter and View
     * This is the MVP Display pattern that should be detected with 90% confidence
     */
    public interface Display {
        HasValue<String> getUsername();
        HasValue<String> getEmail();
        HasText getStatusLabel();
        HasClickHandlers getSaveButton();
        HasClickHandlers getCancelButton();
        HasClickHandlers getViewDetailsButton();
        HasClickHandlers getDeleteButton();
        void showLoading(boolean show);
        void showError(String message);
    }

    private final Display display;
    private final UserServiceAsync userService;
    private Long currentUserId;

    /**
     * Constructor with Display and service dependencies
     */
    public UserPresenter(Display display, UserServiceAsync userService) {
        this.display = display;
        this.userService = userService;
        bind();
    }

    /**
     * Bind event handlers to Display widgets
     * These event handlers demonstrate navigation and RPC calls
     */
    private void bind() {
        // Save button click handler with RPC call
        display.getSaveButton().addClickHandler(new ClickHandler() {
            @Override
            public void onClick(ClickEvent event) {
                saveUser();
            }
        });

        // Cancel button click handler with navigation to Dashboard
        display.getCancelButton().addClickHandler(new ClickHandler() {
            @Override
            public void onClick(ClickEvent event) {
                goToDashboard();
            }
        });

        // View details button with navigation to UserDetailPlace
        display.getViewDetailsButton().addClickHandler(new ClickHandler() {
            @Override
            public void onClick(ClickEvent event) {
                goToUserDetail();
            }
        });

        // Delete button with RPC call
        display.getDeleteButton().addClickHandler(new ClickHandler() {
            @Override
            public void onClick(ClickEvent event) {
                deleteUser();
            }
        });
    }

    /**
     * Load user data via RPC
     */
    public void loadUser(Long userId) {
        this.currentUserId = userId;
        display.showLoading(true);

        userService.getUser(userId, new AsyncCallback<UserDTO>() {
            @Override
            public void onSuccess(UserDTO user) {
                display.showLoading(false);
                display.getUsername().setValue(user.getUsername());
                display.getEmail().setValue(user.getEmail());
                display.getStatusLabel().setText("Active");
            }

            @Override
            public void onFailure(Throwable caught) {
                display.showLoading(false);
                display.showError("Failed to load user: " + caught.getMessage());
            }
        });
    }

    /**
     * Save user via RPC
     */
    private void saveUser() {
        display.showLoading(true);

        UserDTO user = new UserDTO();
        user.setId(currentUserId);
        user.setUsername(display.getUsername().getValue());
        user.setEmail(display.getEmail().getValue());

        userService.saveUser(user, new AsyncCallback<UserDTO>() {
            @Override
            public void onSuccess(UserDTO result) {
                display.showLoading(false);
                Window.alert("User saved successfully");
                goToDashboard();
            }

            @Override
            public void onFailure(Throwable caught) {
                display.showLoading(false);
                display.showError("Failed to save user: " + caught.getMessage());
            }
        });
    }

    /**
     * Delete user via RPC
     */
    private void deleteUser() {
        if (!Window.confirm("Are you sure you want to delete this user?")) {
            return;
        }

        display.showLoading(true);

        userService.deleteUser(currentUserId, new AsyncCallback<Void>() {
            @Override
            public void onSuccess(Void result) {
                display.showLoading(false);
                Window.alert("User deleted successfully");
                goToDashboard();
            }

            @Override
            public void onFailure(Throwable caught) {
                display.showLoading(false);
                display.showError("Failed to delete user: " + caught.getMessage());
            }
        });
    }

    /**
     * Navigate to Dashboard place
     * This navigation should be detected by navigation analyzer
     */
    private void goToDashboard() {
        // Navigation to DashboardPlace
        // placeController.goTo(new DashboardPlace());
    }

    /**
     * Navigate to UserDetail place
     * This navigation should be detected by navigation analyzer
     */
    private void goToUserDetail() {
        // Navigation to UserDetailPlace
        // placeController.goTo(new UserDetailPlace(currentUserId));
    }
}
