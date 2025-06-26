package at.a1ta.framework.gxt.ui;

import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.grid.ColumnData;
import com.extjs.gxt.ui.client.widget.grid.Grid;
import com.extjs.gxt.ui.client.widget.grid.GridCellRenderer;

import at.a1ta.framework.ui.client.util.Validator;

public class ButtonRenderer implements GridCellRenderer<ModelData> {
  private SelectionListener<ButtonEvent> listener;
  private String caption = null;

  public ButtonRenderer(SelectionListener<ButtonEvent> listener, String caption) {
    this.listener = listener;
    this.caption = caption;
  }

  @Override
  public Object render(final ModelData model, String property, ColumnData config, final int rowIndex, final int colIndex,
      final ListStore<ModelData> store, Grid<ModelData> grid) {
    Button b = new Button((String) model.get(property)) {

      @Override
      public String getId() {
        return String.valueOf(store.indexOf(model));
      }

    };
    if (!Validator.isNull(caption)) {
      b.setText(caption);
    }
    b.setItemId((String) model.get(property));
    // b.setId(String.valueOf(rowIndex));
    b.setWidth(grid.getColumnModel().getColumnWidth(colIndex) - 10);
    b.addSelectionListener(listener);

    return b;
  }
}
