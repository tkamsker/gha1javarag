package at.a1ta.cuco.admin.ui.common.client.event;

import at.a1ta.cuco.core.shared.dto.ProductGroup;
import at.a1ta.framework.ui.client.event.PortletEvent;

public class ProductgroupEvent extends PortletEvent {
  public enum UpdateType {
    insert, update, none
  }

  private ProductGroup group;
  private UpdateType type;

  public ProductgroupEvent(ProductGroup group, UpdateType type) {
    super(null, CuCoEventType.PRODUCT_GROUPUPDATE);
    this.group = group;
    this.type = type;
  }

  public ProductGroup getGroup() {
    return group;
  }

  public UpdateType getUpdateType() {
    return type;
  }
}
