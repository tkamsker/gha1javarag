package at.a1ta.cuco.admin.ui.common.client.ui;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.data.BasePagingLoader;
import com.extjs.gxt.ui.client.data.GroupingLoadConfig;
import com.extjs.gxt.ui.client.data.ListLoadResult;
import com.extjs.gxt.ui.client.data.LoadEvent;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.data.PagingLoadResult;
import com.extjs.gxt.ui.client.event.LoadListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.google.gwt.core.client.Scheduler;
import com.google.gwt.core.client.Scheduler.ScheduledCommand;
import com.google.gwt.user.client.rpc.AsyncCallback;
import com.google.gwt.user.client.ui.FlexTable;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.framework.gxt.ui.DetailsDialog;
import at.a1ta.framework.gxt.ui.FilterablePagingMemoryProxy;
import at.a1ta.framework.gxt.ui.PagingGridContainer;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.ui.StyledLabel;
import at.a1ta.framework.ui.client.ui.StyledLabel.Font_Style;
import at.a1ta.framework.ui.client.util.PrintHelper;

public abstract class LocalPagingDetails<T extends Serializable> extends DetailsDialog {

  private FilterablePagingMemoryProxy proxy;

  private PagingGridContainer<ListStore<ModelData>, ModelData> gridContainer;

  private FlexTable printTable;

  public LocalPagingDetails(PortletDefinition portletDefinition, String header) {
    super(portletDefinition, header);
  }

  @Override
  protected void createDetailsContent() {
    getContentPanel().clear();

    BaseAsyncCallback<ArrayList<T>> callback = createCallback();
    fetchDataFromServer(callback);
  }

  protected BaseAsyncCallback<ArrayList<T>> createCallback() {
    BaseAsyncCallback<ArrayList<T>> callback = new BaseAsyncCallback<ArrayList<T>>(this) {

      @Override
      public void onSuccess(ArrayList<T> result) {
        proxy = new FilterablePagingMemoryProxy(convertToBaseModelData(result));

        // loader
        final BasePagingLoader<PagingLoadResult<GroupingLoadConfig>> loader = new BasePagingLoader<PagingLoadResult<GroupingLoadConfig>>(proxy);

        loader.setRemoteSort(true);
        ListStore<ModelData> store = new ListStore<ModelData>(loader);
        gridContainer = new PagingGridContainer<ListStore<ModelData>, ModelData>(store, createColumnModel(), getPagingSize(), getGridHeight());
        gridContainer.setWidth("100%");

        if (!PrintHelper.isInPrintMode()) {
          add(gridContainer);
        } else {
          printTable = new FlexTable();
          printTable.setWidth("100%");
          add(printTable);
        }

        afterGridCreation();

        loader.addLoadListener(new LoadListener() {

          @Override
          public void loaderBeforeLoad(LoadEvent le) {
            if (PrintHelper.isInPrintMode()) {
              showLoading();
            }
          }

          @Override
          public void loaderLoad(final LoadEvent le) {
            if (PrintHelper.isInPrintMode()) {
              fillPrintableTable();
              showContent();
            } else {
              if (((ListLoadResult<?>) le.getData()).getData().isEmpty()) {
                showEmptyContent();
              } else {
                showContent();
              }
              Scheduler.get().scheduleDeferred(new ScheduledCommand() {

                @Override
                public void execute() {
                  gridContainer.syncSize();
                }
              });
            }
          }

        });
        loader.load(0, getPagingSize());
      }

    };
    return callback;
  }

  private void fillPrintableTable() {
    printTable.clear();
    printTable.removeAllRows();
    for (int i = 0; i < gridContainer.getGrid().getColumnModel().getColumnCount(); i++) {
      printTable.setWidget(0, i, new StyledLabel(gridContainer.getGrid().getColumnModel().getColumn(i).getHeader(), Font_Style.BOLD));
      printTable.getColumnFormatter().setWidth(i, String.valueOf(gridContainer.getGrid().getColumnModel().getColumn(i).getWidth()));
    }
  }

  private int getPagingSize() {
    return PrintHelper.isInPrintMode() ? 25 : AdminUI.CONFIG.applicationPagingSize();
  }

  private int getGridHeight() {
    return PrintHelper.isInPrintMode() ? 600 : 430;
  }

  private void afterGridCreation() {
    // do nothing by default;
  }

  protected abstract void fetchDataFromServer(AsyncCallback<ArrayList<T>> callback);

  protected abstract List<BaseModelData> convertToBaseModelData(ArrayList<T> beans);

  protected abstract ColumnModel createColumnModel();

}
