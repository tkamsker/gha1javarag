package at.a1ta.webclient.cucosett.client.portlet.vip;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.framework.ui.client.ui.AbstractPortlet;

public class VipSearchPortlet extends AbstractPortlet {

  public static final String VIP_SEARCH = "VipSearch";

  private static VipSearchPortlet instance;

  private VipSearchComponent component;

  public static VipSearchPortlet create(PortletDefinition portletDefinition) {
    if (instance == null) {
      instance = new VipSearchPortlet(portletDefinition);
    }
    return instance;
  }

  private VipSearchPortlet(PortletDefinition def) {
    super(def, false, false, false);

    component = new VipSearchComponent();
    add(component);
  }

  @Override
  public void init() {
    showContent();
  }
}
