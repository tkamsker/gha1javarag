package at.a1ta.framework.gxt.ui;

import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.data.PagingLoader;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.extjs.gxt.ui.client.widget.toolbar.PagingToolBar;

import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;

/**
 * Extending {@link GridContainer}, this class provides a content panel containing a grid with paging functionality.
 */
public class PagingGridContainer<T extends ListStore<U>, U extends ModelData> extends GridContainer<T, U> {

  private final int pagingSize;

  private final PagingToolBar pagingToolBar;

  public PagingGridContainer(T store, ColumnModel cm, int pagingSize) {
    this(store, cm, pagingSize, 0);
    getGrid().setAutoHeight(true);
  }

  public PagingGridContainer(T store, ColumnModel cm, int pagingSize, int height) {
    this(store, cm, pagingSize, height, false);
  }

  private PagingGridContainer(T store, ColumnModel cm, int pagingSize, int height, boolean editable) {
    super(store, cm, height, editable);
    this.pagingSize = pagingSize;
    pagingToolBar = Util.createPagingToolBar(pagingSize);
    pagingToolBar.bind((PagingLoader<?>) store.getLoader());
    pagingToolBar.setMessages(new PagingToolBar.PagingToolBarMessages() {

      @Override
      public String getEmptyMsg() {
        return AdminUI.ADMINCOMMONTEXTPOOL.noData();
      }

    });
    setBottomComponent(pagingToolBar);
  }

  @Override
  public void reconfigure(T store) {
    super.reconfigure(store);
    pagingToolBar.bind((PagingLoader<?>) store.getLoader());
  }

  public PagingToolBar getToolbar() {
    return pagingToolBar;
  }

  public int getPagingSize() {
    return pagingSize;
  }

  public void first() {
    pagingToolBar.first();
  }

}
