package at.a1ta.webclient.cucosett.client.ui;

import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.grid.ColumnData;
import com.extjs.gxt.ui.client.widget.grid.Grid;
import com.extjs.gxt.ui.client.widget.grid.GridCellRenderer;
import com.google.gwt.resources.client.ImageResource;
import com.google.gwt.user.client.ui.AbstractImagePrototype;

public class IconButtonRenderer implements GridCellRenderer<ModelData> {
  private SelectionListener<ButtonEvent> listener;
  private AbstractImagePrototype image;

  public IconButtonRenderer(SelectionListener<ButtonEvent> listener, ImageResource image) {
    this.listener = listener;
    this.image = AbstractImagePrototype.create(image);
  }

  @Override
  public Object render(final ModelData model, String property, ColumnData config, final int rowIndex, final int colIndex,
      ListStore<ModelData> store, Grid<ModelData> grid) {
    final Button b = new Button();
    b.setIcon(image);
    b.setItemId((String) model.get(property));
    b.addSelectionListener(listener);
    return b;
  }
}
