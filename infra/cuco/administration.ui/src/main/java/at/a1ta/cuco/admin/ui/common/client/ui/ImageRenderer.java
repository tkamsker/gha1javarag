/*
 * Copyright 2009 - 2012 by A1 Telekom Austria AG
 * All Rights Reserved.
 * 
 * The Software is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * All information contained herein is, and remains the property of
 * A1 Telekom Austria AG and its suppliers, if any.
 * The intellectual and technical concepts contained herein are proprietary
 * to A1 Telekom Austria AG and its suppliers and may be covered by
 * intertional or national patents, patents in process, and are protected
 * by trade secret or copyright law. Dissemination of this information or
 * reproduction of this material is strictly forbidden unless prior written
 * permission is obtained from A1 Telekom Austria AG.
 */
package at.a1ta.cuco.admin.ui.common.client.ui;

import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.event.BaseEvent;
import com.extjs.gxt.ui.client.event.Events;
import com.extjs.gxt.ui.client.event.Listener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.grid.ColumnData;
import com.extjs.gxt.ui.client.widget.grid.Grid;
import com.extjs.gxt.ui.client.widget.grid.GridCellRenderer;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.ui.Image;

import at.a1ta.bite.ui.client.bundle.UI;

public class ImageRenderer implements GridCellRenderer<ModelData> {

  public static final int DELETE = 2;
  public static final int DOWN = 5;
  public static final int UP = 6;
  public static final int DOWNLOAD = 7;
  public static final int ERASE = 8; 
  
  protected Listener<BaseEvent> listener;
  protected String tooltip = null;
  protected int type = 1;

  public ImageRenderer(int type, Listener<BaseEvent> listener) {
    this.listener = listener;
    this.type = type;
  }

  @Override
  public Object render(final ModelData model, String property, ColumnData config, final int rowIndex, final int colIndex,
      ListStore<ModelData> store, Grid<ModelData> grid) {
    Image img = null;

    if (type == DELETE) {
      img = new Image(UI.IMAGES.iconPlaceholder());
    }
    
    if(type == DOWNLOAD) {
      img = new Image(UI.IMAGES.iconDownload()); 
    }
    
    if(type == ERASE) {
      img = new Image(UI.IMAGES.iconDelete());
    }

    if (type == DOWN) {
      img = new Image(UI.IMAGES.iconCheck());
    }

    if (type == UP) {
      img = new Image(UI.IMAGES.iconPlaceholder());
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
