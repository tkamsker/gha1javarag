package at.a1ta.cuco.admin.ui.common.client.event;

import java.util.List;

import at.a1ta.cuco.admin.ui.common.client.dto.ServiceModel;
import at.a1ta.framework.ui.client.event.PortletEvent;

public class AddServicesEvent extends PortletEvent {
  private List<ServiceModel> services;

  public AddServicesEvent(List<ServiceModel> services) {
    super(null, CuCoEventType.ADD_SERVICES);
    setServices(services);
  }

  public List<ServiceModel> getServices() {
    return services;
  }

  public void setServices(List<ServiceModel> services) {
    this.services = services;
  }
}
