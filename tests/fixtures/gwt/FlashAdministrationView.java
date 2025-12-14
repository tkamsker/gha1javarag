package com.example.client.admin;

import com.google.gwt.core.client.GWT;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.uibinder.client.UiTemplate;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Widget;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.cellview.client.CellTable;

import com.example.shared.FlashInfoDTO;
import com.example.client.admin.FlashAdministrationPresenter.Display;

import java.util.List;

/**
 * View for Flash Information Administration.
 *
 * Implements the Display interface from FlashAdministrationPresenter.
 * Uses UiBinder for UI definition.
 */
public class FlashAdministrationView extends Composite implements Display {

    /**
     * UiBinder interface for this view.
     */
    @UiTemplate("FlashAdministrationView.ui.xml")
    interface FlashAdministrationViewUiBinder extends UiBinder<Widget, FlashAdministrationView> {
    }

    private static FlashAdministrationViewUiBinder uiBinder =
        GWT.create(FlashAdministrationViewUiBinder.class);

    // UI fields bound from UiBinder template
    @UiField
    CellTable<FlashInfoDTO> dataTable;

    @UiField
    Button createButton;

    @UiField
    Button refreshButton;

    @UiField
    Button deleteButton;

    @UiField
    Label statusLabel;

    @UiField
    Label errorLabel;

    private FlashInfoDTO selectedItem;

    /**
     * Constructor.
     */
    public FlashAdministrationView() {
        initWidget(uiBinder.createAndBindUi(this));
        initializeTable();
    }

    /**
     * Initialize the data table.
     */
    private void initializeTable() {
        // Table initialization would go here
        // Add columns, selection handlers, etc.
    }

    // Implementation of Display interface

    @Override
    public void setData(List<FlashInfoDTO> data) {
        // Update table with data
        dataTable.setRowCount(data.size(), true);
        dataTable.setRowData(0, data);
    }

    @Override
    public void showLoadingIndicator(boolean show) {
        if (show) {
            statusLabel.setText("Loading...");
            statusLabel.setVisible(true);
        } else {
            statusLabel.setVisible(false);
        }
    }

    @Override
    public void showError(String message) {
        errorLabel.setText(message);
        errorLabel.setVisible(true);
    }

    @Override
    public FlashAdministrationPresenter.HasClickHandler getCreateButton() {
        return new ButtonClickAdapter(createButton);
    }

    @Override
    public FlashAdministrationPresenter.HasClickHandler getRefreshButton() {
        return new ButtonClickAdapter(refreshButton);
    }

    @Override
    public FlashAdministrationPresenter.HasClickHandler getDeleteButton() {
        return new ButtonClickAdapter(deleteButton);
    }

    @Override
    public FlashInfoDTO getSelectedItem() {
        return selectedItem;
    }

    @Override
    public void clearSelection() {
        selectedItem = null;
        // Clear table selection
    }

    @Override
    public void updateItem(FlashInfoDTO item) {
        // Update specific item in table
    }

    /**
     * Adapter to bridge Button and HasClickHandler.
     */
    private static class ButtonClickAdapter implements FlashAdministrationPresenter.HasClickHandler {
        private final Button button;

        public ButtonClickAdapter(Button button) {
            this.button = button;
        }

        @Override
        public void addClickHandler(com.google.gwt.event.dom.client.ClickHandler handler) {
            button.addClickHandler(handler);
        }
    }
}
