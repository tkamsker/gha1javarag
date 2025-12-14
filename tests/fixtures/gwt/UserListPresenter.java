package com.example.client.user;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.rpc.AsyncCallback;
import com.google.inject.Inject;

import com.example.client.UserServiceAsync;
import com.example.shared.UserDTO;
import com.example.client.view.IUserListView;

import java.util.List;

/**
 * Presenter for User List.
 *
 * Uses separate interface pattern (85% confidence).
 * View interface is defined in a separate file (IUserListView).
 */
public class UserListPresenter {

    private final IUserListView view;
    private final UserServiceAsync userService;

    /**
     * Constructor with separate view interface.
     *
     * @param view View implementing IUserListView interface
     * @param userService RPC service for user operations
     */
    @Inject
    public UserListPresenter(IUserListView view, UserServiceAsync userService) {
        this.view = view;
        this.userService = userService;
        bindHandlers();
    }

    /**
     * Bind event handlers to view.
     */
    private void bindHandlers() {
        // Event handler: Add user
        view.getAddButton().addClickHandler(new ClickHandler() {
            @Override
            public void onClick(ClickEvent event) {
                handleAddUser();
            }
        });

        // Event handler: Edit user
        view.getEditButton().addClickHandler(new ClickHandler() {
            @Override
            public void onClick(ClickEvent event) {
                handleEditUser();
            }
        });

        // Event handler: Search users
        view.getSearchButton().addClickHandler(new ClickHandler() {
            @Override
            public void onClick(ClickEvent event) {
                handleSearch();
            }
        });
    }

    /**
     * Start the presenter.
     */
    public void start() {
        loadUsers();
    }

    /**
     * Handle add user button - navigation logic.
     */
    private void handleAddUser() {
        // Navigation: redirect to user creation form
        view.navigateTo("/user/create");
    }

    /**
     * Handle edit user button - navigation logic.
     */
    private void handleEditUser() {
        UserDTO selected = view.getSelectedUser();
        if (selected != null) {
            // Navigation: redirect to user edit form
            view.navigateTo("/user/edit/" + selected.getId());
        } else {
            view.showMessage("Please select a user to edit");
        }
    }

    /**
     * Handle search button.
     */
    private void handleSearch() {
        String query = view.getSearchQuery();
        searchUsers(query);
    }

    /**
     * Load all users.
     */
    private void loadUsers() {
        view.showLoading(true);

        userService.getAllUsers(new AsyncCallback<List<UserDTO>>() {
            @Override
            public void onSuccess(List<UserDTO> result) {
                view.showLoading(false);
                view.displayUsers(result);
            }

            @Override
            public void onFailure(Throwable caught) {
                view.showLoading(false);
                view.showError("Failed to load users: " + caught.getMessage());
            }
        });
    }

    /**
     * Search users by query.
     */
    private void searchUsers(String query) {
        view.showLoading(true);

        userService.searchUsers(query, new AsyncCallback<List<UserDTO>>() {
            @Override
            public void onSuccess(List<UserDTO> result) {
                view.showLoading(false);
                view.displayUsers(result);
            }

            @Override
            public void onFailure(Throwable caught) {
                view.showLoading(false);
                view.showError("Search failed: " + caught.getMessage());
            }
        });
    }
}
