package at.a1ta.webclient.cucosett.client.portlet;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.framework.ui.client.ui.AbstractPortlet;

public abstract class CuCoSettBasePortlet extends AbstractPortlet {

  private CuCoSettBasePortlet(PortletDefinition def, boolean isDetails) {
    super(def, isDetails);
  }

  public CuCoSettBasePortlet(PortletDefinition def) {
    this(def, false);
  }

  public CuCoSettBasePortlet(PortletDefinition def, boolean isDetails, boolean collapsible, boolean hasDetails) {
    super(def, isDetails, collapsible, hasDetails);
  }

  public CuCoSettBasePortlet(PortletDefinition def, boolean collapsible, boolean hasDetails) {
    this(def, false, collapsible, hasDetails);
  }
}
