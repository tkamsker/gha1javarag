package at.a1ta.cuco.admin.ui.common.client.ui;

import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.grid.ColumnData;
import com.extjs.gxt.ui.client.widget.grid.Grid;
import com.extjs.gxt.ui.client.widget.grid.GridCellRenderer;

import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;

public class BooleanRenderer implements GridCellRenderer<ModelData> {
  @Override
  public Object render(ModelData model, String property, ColumnData config, int rowIndex, int colIndex, ListStore<ModelData> store, Grid<ModelData> grid) {
    return ((Boolean) model.get(property)) ? AdminUI.ADMINCOMMONTEXTPOOL.yes() : AdminUI.ADMINCOMMONTEXTPOOL.no();
  }
}
