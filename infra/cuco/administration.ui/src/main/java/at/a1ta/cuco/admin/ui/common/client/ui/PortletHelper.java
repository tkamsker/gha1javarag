package at.a1ta.cuco.admin.ui.common.client.ui;

import com.extjs.gxt.ui.client.widget.LayoutContainer;
import com.extjs.gxt.ui.client.widget.WidgetComponent;
import com.extjs.gxt.ui.client.widget.tips.ToolTipConfig;
import com.google.gwt.resources.client.ImageResource;
import com.google.gwt.user.client.ui.Grid;
import com.google.gwt.user.client.ui.Image;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.ui.client.bundle.UI;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.framework.ui.client.util.PrintHelper;

public class PortletHelper {
  private static WidgetComponent getInfoIcon() {
    return getIcon(UI.IMAGES.iconInfoTiny());
  }

  public static LayoutContainer createInfoWidget(Widget widget, String tooltip) {
    return createInfoWidget(widget, AdminUI.ADMINCOMMONTEXTPOOL.info(), tooltip);
  }

  private static LayoutContainer createInfoWidget(final Widget widget, final String title, final String tooltip) {
    LayoutContainer c = new LayoutContainer();
    if (!PrintHelper.isInPrintMode()) {
      ToolTipConfig toolTipConfig = new ToolTipConfig(title, tooltip);
      toolTipConfig.setDismissDelay(0);
      c.setToolTip(toolTipConfig);

      WidgetComponent infoIcon = getInfoIcon();

      Grid grid = new Grid(1, 2);
      grid.setWidget(0, 0, widget);
      grid.setWidget(0, 1, infoIcon);
      c.add(grid);
    } else {
      c.add(widget);
    }
    return c;
  }

  private static WidgetComponent getIcon(ImageResource imageResource) {
    Image img = new Image(imageResource);
    WidgetComponent component = new WidgetComponent(img);
    return component;
  }
}
