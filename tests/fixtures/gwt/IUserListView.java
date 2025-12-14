package com.example.client.view;

import com.google.gwt.event.dom.client.HasClickHandlers;
import com.example.shared.UserDTO;
import java.util.List;

/**
 * View interface for User List.
 *
 * Separate interface pattern - not nested in presenter.
 * This represents the 85% confidence pattern for view binding detection.
 */
public interface IUserListView {

    /**
     * Display list of users.
     */
    void displayUsers(List<UserDTO> users);

    /**
     * Show/hide loading indicator.
     */
    void showLoading(boolean loading);

    /**
     * Show error message.
     */
    void showError(String message);

    /**
     * Show info message.
     */
    void showMessage(String message);

    /**
     * Get add button handler.
     */
    HasClickHandlers getAddButton();

    /**
     * Get edit button handler.
     */
    HasClickHandlers getEditButton();

    /**
     * Get search button handler.
     */
    HasClickHandlers getSearchButton();

    /**
     * Get selected user.
     */
    UserDTO getSelectedUser();

    /**
     * Get search query text.
     */
    String getSearchQuery();

    /**
     * Navigate to URL.
     */
    void navigateTo(String url);
}
