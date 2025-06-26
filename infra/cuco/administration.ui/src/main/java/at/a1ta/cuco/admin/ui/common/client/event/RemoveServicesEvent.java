package at.a1ta.cuco.admin.ui.common.client.event;

import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.framework.ui.client.event.PortletEvent;

public class RemoveServicesEvent extends PortletEvent {
  private Service service;

  public RemoveServicesEvent(Service service) {
    super(null, CuCoEventType.REMOVE_SERVICES);
    setService(service);
  }

  public Service getService() {
    return service;
  }

  public void setService(Service service) {
    this.service = service;
  }

}
