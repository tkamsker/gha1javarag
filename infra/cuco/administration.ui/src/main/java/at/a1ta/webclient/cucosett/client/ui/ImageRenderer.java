package at.a1ta.webclient.cucosett.client.ui;

import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.grid.ColumnData;
import com.extjs.gxt.ui.client.widget.grid.Grid;
import com.extjs.gxt.ui.client.widget.grid.GridCellRenderer;
import com.google.gwt.user.client.ui.Image;

import at.a1ta.framework.ui.client.util.Validator;

public class ImageRenderer implements GridCellRenderer<ModelData> {
  private int width;
  private int height;

  public ImageRenderer(int w, int h) {
    width = w;
    height = h;
  }

  @Override
  public Object render(final ModelData model, String property, ColumnData config, final int rowIndex, final int colIndex, ListStore<ModelData> store, Grid<ModelData> grid) {

    Image img = new Image((String) model.get(property));
    if (width != 0) {
      img.setWidth((width - 3) + "px");
    }
    if (height != 0) {
      img.setHeight((height - 3) + "px");
    }
    if (Validator.isNullOrEmpty(img.getUrl())) {
      img.setVisible(false);
    } else {
      img.setVisible(true);
    }
    return img;
  }
}
