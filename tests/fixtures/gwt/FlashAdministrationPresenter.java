package com.example.client.admin;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.rpc.AsyncCallback;
import com.google.gwt.user.client.ui.HasWidgets;
import com.google.inject.Inject;

import com.example.client.FlashInfoServiceAsync;
import com.example.shared.FlashInfoDTO;
import com.example.client.place.DashboardPlace;
import com.example.client.ClientFactory;

import java.util.List;

/**
 * Presenter for Flash Information Administration.
 *
 * Follows MVP pattern with nested Display interface.
 * This is the high-confidence pattern (90%) for view binding detection.
 */
public class FlashAdministrationPresenter {

    /**
     * Display interface defines view contract.
     * This is the standard GWT MVP pattern.
     */
    public interface Display {
        void setData(List<FlashInfoDTO> data);
        void showLoadingIndicator(boolean show);
        void showError(String message);
        HasClickHandler getCreateButton();
        HasClickHandler getRefreshButton();
        HasClickHandler getDeleteButton();
        FlashInfoDTO getSelectedItem();
        void clearSelection();
        void updateItem(FlashInfoDTO item);
    }

    // Fake interface for button handlers
    public interface HasClickHandler {
        void addClickHandler(ClickHandler handler);
    }

    private final Display view;
    private final FlashInfoServiceAsync rpcService;
    private final ClientFactory clientFactory;

    /**
     * Constructor with view injection.
     *
     * @param view The view implementing Display interface
     * @param rpcService RPC service for backend calls
     * @param clientFactory Factory for navigation
     */
    @Inject
    public FlashAdministrationPresenter(
        Display view,
        FlashInfoServiceAsync rpcService,
        ClientFactory clientFactory
    ) {
        this.view = view;
        this.rpcService = rpcService;
        this.clientFactory = clientFactory;
    }

    /**
     * Initialize presenter and bind event handlers.
     */
    public void bind() {
        // Event handler: Create new flash info
        view.getCreateButton().addClickHandler(new ClickHandler() {
            @Override
            public void onClick(ClickEvent event) {
                handleCreate();
            }
        });

        // Event handler: Refresh data
        view.getRefreshButton().addClickHandler(new ClickHandler() {
            @Override
            public void onClick(ClickEvent event) {
                handleRefresh();
            }
        });

        // Event handler: Delete selected item
        view.getDeleteButton().addClickHandler(new ClickHandler() {
            @Override
            public void onClick(ClickEvent event) {
                handleDelete();
            }
        });

        // Load initial data
        loadData();
    }

    /**
     * Navigate to container.
     */
    public void go(HasWidgets container) {
        bind();
        // Container would add view widget here
    }

    /**
     * Handle create button click - navigation logic.
     */
    private void handleCreate() {
        // Navigation: Go to create form
        clientFactory.getPlaceController().goTo(
            new com.example.client.place.FlashInfoEditPlace("new")
        );
    }

    /**
     * Handle refresh button click.
     */
    private void handleRefresh() {
        loadData();
    }

    /**
     * Handle delete button click.
     */
    private void handleDelete() {
        FlashInfoDTO selected = view.getSelectedItem();

        if (selected == null) {
            view.showError("Please select an item to delete");
            return;
        }

        if (!Window.confirm("Delete flash info: " + selected.getTitle() + "?")) {
            return;
        }

        view.showLoadingIndicator(true);

        rpcService.deleteFlashInfo(selected.getId(), new AsyncCallback<Boolean>() {
            @Override
            public void onSuccess(Boolean result) {
                view.showLoadingIndicator(false);
                if (result) {
                    view.clearSelection();
                    loadData();
                } else {
                    view.showError("Failed to delete item");
                }
            }

            @Override
            public void onFailure(Throwable caught) {
                view.showLoadingIndicator(false);
                view.showError("Error deleting item: " + caught.getMessage());
            }
        });
    }

    /**
     * Load data from backend.
     */
    private void loadData() {
        view.showLoadingIndicator(true);

        rpcService.getAllFlashInfo(new AsyncCallback<List<FlashInfoDTO>>() {
            @Override
            public void onSuccess(List<FlashInfoDTO> result) {
                view.showLoadingIndicator(false);
                view.setData(result);
            }

            @Override
            public void onFailure(Throwable caught) {
                view.showLoadingIndicator(false);
                view.showError("Error loading data: " + caught.getMessage());
            }
        });
    }

    /**
     * Navigate back to dashboard - navigation logic.
     */
    public void navigateToDashboard() {
        clientFactory.getPlaceController().goTo(new DashboardPlace());
    }
}
