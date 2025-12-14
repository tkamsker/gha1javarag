package com.example.client.view;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.ui.*;
import com.example.client.service.UserServiceAsync;

/**
 * Sample GWT widget for testing PRD generation.
 * Demonstrates GWT widget structure and event handling.
 */
public class UserListPanel extends Composite {

    private static UserListPanelUiBinder uiBinder = GWT.create(UserListPanelUiBinder.class);

    interface UserListPanelUiBinder extends UiBinder<Widget, UserListPanel> {}

    @UiField
    FlexTable userTable;

    @UiField
    Button addUserButton;

    @UiField
    Button refreshButton;

    @UiField
    TextBox searchBox;

    @UiField
    Button searchButton;

    private UserServiceAsync userService;

    /**
     * Constructor initializes the panel and loads users.
     */
    public UserListPanel() {
        initWidget(uiBinder.createAndBindUi(this));

        userService = GWT.create(UserService.class);

        // Set up table headers
        userTable.setText(0, 0, "ID");
        userTable.setText(0, 1, "Email");
        userTable.setText(0, 2, "Name");
        userTable.setText(0, 3, "Active");
        userTable.setText(0, 4, "Actions");

        // Initialize event handlers
        setupEventHandlers();

        // Load initial data
        loadUsers();
    }

    /**
     * Sets up event handlers for buttons and inputs.
     */
    private void setupEventHandlers() {
        // Add user button
        addUserButton.addClickHandler(new ClickHandler() {
            @Override
            public void onClick(ClickEvent event) {
                showAddUserDialog();
            }
        });

        // Refresh button
        refreshButton.addClickHandler(new ClickHandler() {
            @Override
            public void onClick(ClickEvent event) {
                loadUsers();
            }
        });

        // Search button
        searchButton.addClickHandler(new ClickHandler() {
            @Override
            public void onClick(ClickEvent event) {
                searchUsers(searchBox.getValue());
            }
        });

        // Enter key in search box
        searchBox.addKeyPressHandler(new KeyPressHandler() {
            @Override
            public void onKeyPress(KeyPressEvent event) {
                if (event.getCharCode() == KeyCodes.KEY_ENTER) {
                    searchUsers(searchBox.getValue());
                }
            }
        });
    }

    /**
     * Loads all users from the server.
     */
    private void loadUsers() {
        userService.getAllUsers(new AsyncCallback<List<User>>() {
            @Override
            public void onSuccess(List<User> users) {
                displayUsers(users);
            }

            @Override
            public void onFailure(Throwable caught) {
                Window.alert("Failed to load users: " + caught.getMessage());
            }
        });
    }

    /**
     * Searches users by query string.
     *
     * @param query Search query
     */
    private void searchUsers(String query) {
        if (query == null || query.trim().isEmpty()) {
            loadUsers();
            return;
        }

        userService.searchUsers(query, new AsyncCallback<List<User>>() {
            @Override
            public void onSuccess(List<User> users) {
                displayUsers(users);
            }

            @Override
            public void onFailure(Throwable caught) {
                Window.alert("Search failed: " + caught.getMessage());
            }
        });
    }

    /**
     * Displays users in the table.
     *
     * @param users List of users to display
     */
    private void displayUsers(List<User> users) {
        // Clear existing rows (except header)
        while (userTable.getRowCount() > 1) {
            userTable.removeRow(1);
        }

        // Add user rows
        int row = 1;
        for (final User user : users) {
            userTable.setText(row, 0, String.valueOf(user.getId()));
            userTable.setText(row, 1, user.getEmail());
            userTable.setText(row, 2, user.getFirstName() + " " + user.getLastName());
            userTable.setText(row, 3, user.isActive() ? "Yes" : "No");

            // Action buttons
            HorizontalPanel actions = new HorizontalPanel();

            Button editButton = new Button("Edit");
            editButton.addClickHandler(new ClickHandler() {
                @Override
                public void onClick(ClickEvent event) {
                    editUser(user);
                }
            });

            Button deleteButton = new Button("Delete");
            deleteButton.addClickHandler(new ClickHandler() {
                @Override
                public void onClick(ClickEvent event) {
                    deleteUser(user);
                }
            });

            actions.add(editButton);
            actions.add(deleteButton);
            userTable.setWidget(row, 4, actions);

            row++;
        }
    }

    /**
     * Shows dialog to add a new user.
     */
    private void showAddUserDialog() {
        // Navigate to add user form
        // Implementation depends on application architecture
        Window.alert("Add user functionality would open here");
    }

    /**
     * Edits an existing user.
     *
     * @param user User to edit
     */
    private void editUser(User user) {
        // Navigate to edit user form
        Window.alert("Edit user: " + user.getEmail());
    }

    /**
     * Deletes a user after confirmation.
     *
     * @param user User to delete
     */
    private void deleteUser(final User user) {
        if (Window.confirm("Are you sure you want to delete user: " + user.getEmail() + "?")) {
            userService.deleteUser(user.getId(), new AsyncCallback<Void>() {
                @Override
                public void onSuccess(Void result) {
                    Window.alert("User deleted successfully");
                    loadUsers();
                }

                @Override
                public void onFailure(Throwable caught) {
                    Window.alert("Failed to delete user: " + caught.getMessage());
                }
            });
        }
    }
}
