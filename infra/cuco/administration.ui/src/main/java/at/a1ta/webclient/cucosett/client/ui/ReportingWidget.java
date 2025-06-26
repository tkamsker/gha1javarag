package at.a1ta.webclient.cucosett.client.ui;

import java.util.HashMap;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.Image;

import at.a1ta.bite.ui.client.bundle.UI;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;

public class ReportingWidget extends HorizontalPanel {
  // @formatter:off
  private long id;
  private DataTable<HashMap<String, Object>> dataTable;
  private Image close;
  // @formatter:on

  public ReportingWidget(final DataTable<HashMap<String, Object>> table, long id) {
    this.setDataTable(table);
    this.id = id;

    close = new Image(UI.IMAGES.iconDelete());
    close.setStyleName(UI.STYLES.cursor_pointer());
    close.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        removeFromParent();
      }
    });
    add(table);
    add(close);
  }

  public long getId() {
    return id;
  }

  public void setId(long id) {
    this.id = id;
  }

  public void setDataTable(DataTable<HashMap<String, Object>> dataTable) {
    this.dataTable = dataTable;
  }

  public DataTable<HashMap<String, Object>> getDataTable() {
    return dataTable;
  }

  public Image getClose() {
    return close;
  }

  public void setClose(Image close) {
    this.close = close;
  }
}
