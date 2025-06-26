package at.a1ta.framework.gxt.ui;

import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.grid.ColumnData;
import com.extjs.gxt.ui.client.widget.grid.Grid;
import com.extjs.gxt.ui.client.widget.grid.GridCellRenderer;
import com.google.gwt.event.dom.client.ClickHandler;

import at.a1ta.framework.ui.client.util.HtmlUtils;

/**
 * Renders an internal link
 * 
 * @author q909158
 */
public class LinkCellRenderer implements GridCellRenderer<ModelData> {

  private ClickHandler clickHandler;

  /**
   * @param clickHandler reference to the handler which should be calles when the link is clicked
   */
  public LinkCellRenderer(ClickHandler clickHandler) {
    super();
    this.clickHandler = clickHandler;
  }

  /**
   * renders a link with the cellvalue as text
   * 
   * @see com.extjs.gxt.ui.client.widget.grid.GridCellRenderer#render(com.extjs.gxt.ui.client.data.ModelData, java.lang.String,
   *      com.extjs.gxt.ui.client.widget.grid.ColumnData, int, int, com.extjs.gxt.ui.client.store.ListStore,
   *      com.extjs.gxt.ui.client.widget.grid.Grid)
   */
  @Override
  public Object render(ModelData model, String property, ColumnData config, int rowIndex, int colIndex, ListStore<ModelData> store,
      Grid<ModelData> grid) {
    if (model.get(property) != null) {
      return HtmlUtils.createInternalLink(model.get(property).toString(), clickHandler);
    }
    return HtmlUtils.createInternalLink("Not set", clickHandler);
  }

}
