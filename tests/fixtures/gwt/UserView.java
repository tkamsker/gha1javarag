package com.example.client;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.HasClickHandlers;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.HasText;
import com.google.gwt.user.client.ui.HasValue;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.Panel;
import com.google.gwt.user.client.ui.TextBox;
import com.google.gwt.user.client.ui.Widget;

/**
 * GWT View implementing UserPresenter.Display interface
 * with @UiField annotations bound to UiBinder template
 */
public class UserView extends Composite implements UserPresenter.Display {

    private static UserViewUiBinder uiBinder = GWT.create(UserViewUiBinder.class);

    interface UserViewUiBinder extends UiBinder<Widget, UserView> {
    }

    // UI fields bound to UiBinder template
    @UiField
    TextBox usernameTextBox;

    @UiField
    TextBox emailTextBox;

    @UiField
    Label statusLabel;

    @UiField
    Label errorLabel;

    @UiField
    Button saveButton;

    @UiField
    Button cancelButton;

    @UiField
    Button viewDetailsButton;

    @UiField
    Button deleteButton;

    @UiField
    Panel loadingPanel;

    @UiField
    Panel errorPanel;

    @UiField
    Panel formPanel;

    /**
     * Constructor initializes UiBinder
     */
    public UserView() {
        initWidget(uiBinder.createAndBindUi(this));
        errorPanel.setVisible(false);
        loadingPanel.setVisible(false);
    }

    // Implementation of Display interface methods

    @Override
    public HasValue<String> getUsername() {
        return usernameTextBox;
    }

    @Override
    public HasValue<String> getEmail() {
        return emailTextBox;
    }

    @Override
    public HasText getStatusLabel() {
        return statusLabel;
    }

    @Override
    public HasClickHandlers getSaveButton() {
        return saveButton;
    }

    @Override
    public HasClickHandlers getCancelButton() {
        return cancelButton;
    }

    @Override
    public HasClickHandlers getViewDetailsButton() {
        return viewDetailsButton;
    }

    @Override
    public HasClickHandlers getDeleteButton() {
        return deleteButton;
    }

    @Override
    public void showLoading(boolean show) {
        loadingPanel.setVisible(show);
        formPanel.setVisible(!show);
    }

    @Override
    public void showError(String message) {
        errorLabel.setText(message);
        errorPanel.setVisible(message != null && !message.isEmpty());
    }
}
