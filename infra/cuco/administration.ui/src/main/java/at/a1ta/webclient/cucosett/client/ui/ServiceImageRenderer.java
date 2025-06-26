package at.a1ta.webclient.cucosett.client.ui;

import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.event.BaseEvent;
import com.extjs.gxt.ui.client.event.Events;
import com.extjs.gxt.ui.client.event.Listener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.grid.ColumnData;
import com.extjs.gxt.ui.client.widget.grid.Grid;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.ui.Image;

import at.a1ta.bite.ui.client.bundle.UI;
import at.a1ta.cuco.admin.ui.common.client.ui.ImageRenderer;
import at.a1ta.cuco.admin.ui.common.client.ui.PortletHelper;
import at.a1ta.cuco.core.shared.dto.Service;

public class ServiceImageRenderer extends ImageRenderer {

  public ServiceImageRenderer(int type, Listener<BaseEvent> listener) {
    super(type, listener);
  }

  @Override
  public Object render(final ModelData model, String property, ColumnData config, final int rowIndex, final int colIndex, ListStore<ModelData> store, Grid<ModelData> grid) {
    Service service = (Service) model.get("bean");
    if (!service.getTicketcount().equals(0L)) {
      return null;
    }

    Image img = null;

    if (type == DELETE) {
      img = new Image(UI.IMAGES.iconDelete());
    }

    if (img == null) {
      throw new RuntimeException("Invalid Imagetype: " + type);
    }

    img.addStyleName(UI.STYLES.cursor_pointer());
    img.addClickHandler(new ClickHandler() {

      @Override
      public void onClick(ClickEvent event) {
        listener.handleEvent(new BaseEvent(Events.Select));
      }
    });

    if (tooltip != null) {
      return PortletHelper.createInfoWidget(img, tooltip);
    }
    return img;
  }
}
