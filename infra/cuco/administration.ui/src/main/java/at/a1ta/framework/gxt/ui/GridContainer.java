package at.a1ta.framework.gxt.ui;

import com.extjs.gxt.ui.client.Style.SelectionMode;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.event.BaseEvent;
import com.extjs.gxt.ui.client.event.Events;
import com.extjs.gxt.ui.client.event.Listener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.ContentPanel;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.extjs.gxt.ui.client.widget.grid.EditorGrid;
import com.extjs.gxt.ui.client.widget.grid.Grid;
import com.extjs.gxt.ui.client.widget.layout.FitLayout;
import com.google.gwt.core.client.Scheduler;
import com.google.gwt.core.client.Scheduler.ScheduledCommand;

import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;

/**
 * This class provides a grid wrapped in a content panel.By default the header of the content panel is not shown, the
 * grid's columns automatically resize to fit the grid's width and the load mask is shown. To include paging
 * functionality, see {@link PagingGridContainer}
 */
public class GridContainer<T extends ListStore<U>, U extends ModelData> extends ContentPanel {

  private final Grid<U> grid;

  public GridContainer(T store, ColumnModel cm) {
    this(store, cm, 0, false);
    grid.setAutoHeight(true);
  }

  public GridContainer(T store, ColumnModel cm, boolean editable) {
    this(store, cm, 0, editable);
    grid.setAutoHeight(true);
  }

  /**
   * @param store The store of the grid.
   * @param cm The column model of the grid.
   * @param height The height of the grid. It has to be set to a fixed sized because of layout issues.
   */
  public GridContainer(T store, ColumnModel cm, int height) {
    this(store, cm, height, false);
  }

  /**
   * @param store The store of the grid.
   * @param cm The column model of the grid.
   * @param height The height of the grid. It has to be set to a fixed sized because of layout issues.
   * @param editable True to add edit capabilities to grid.
   */
  public GridContainer(T store, ColumnModel cm, int height, boolean editable) {
    // setSize("100%", "100%");

    // setFrame(true);
    setHeaderVisible(false);
    setLayout(new FitLayout());
    setLayoutOnChange(true);
    setHeight(height);

    grid = editable ? new EditorGrid<U>(store, cm) : new Grid<U>(store, cm);
    // grid.setAutoExpandColumn(cm.getColumn(cm.getColumnCount() -
    // 1).getId());
    grid.getView().setAutoFill(true);
    grid.getView().setForceFit(true);
    grid.getView().setEmptyText(AdminUI.ADMINCOMMONTEXTPOOL.noData());
    grid.setStripeRows(true);

    grid.setLoadMask(true);
    grid.getSelectionModel().setSelectionMode(SelectionMode.SINGLE);
    setBottomComponent(null);

    grid.disableTextSelection(false);
    add(grid);

    setMonitorWindowResize(true);

    grid.addListener(Events.Attach, new Listener<BaseEvent>() {

      @Override
      public void handleEvent(BaseEvent be) {
        layout(true);
        grid.getView().refresh(true);
      }
    });
  }

  public void reconfigure(T store) {
    getGrid().reconfigure(store, getGrid().getColumnModel());
  }

  public Grid<U> getGrid() {
    return grid;
  }

  @Override
  protected void onWindowResize(int width, int height) {
    Scheduler.get().scheduleDeferred(new ScheduledCommand() {

      @Override
      public void execute() {
        layout(true);
      }
    });
  }

}
