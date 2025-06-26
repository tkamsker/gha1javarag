package at.a1ta.cuco.admin.ui.common.server;

import javax.servlet.annotation.WebServlet;
import java.util.ArrayList;

import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.ui.server.servlet.SpringRemoteServiceServlet;
import at.a1ta.cuco.admin.ui.common.client.service.ServiceServlet;
import at.a1ta.cuco.core.service.ServiceService;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.framework.ui.client.dto.RpcStatus;

@WebServlet(name = "appServiceAdmin", urlPatterns = {"/admin/cuco/service.rpc"})
public class ServiceServletImpl extends SpringRemoteServiceServlet implements ServiceServlet {
  @Autowired
  private ServiceService serviceService;

  @Override
  public RpcStatus deleteService(Long id) {
    serviceService.deleteService(id);
    return RpcStatus.OK;
  }

  @Override
  public ArrayList<Service> getAllServices() {
    return (ArrayList<Service>) serviceService.getAllServices();
  }

  @Override
  public Service saveService(Service service) {
    serviceService.saveService(service);
    return service;
  }

  @Override
  public ArrayList<Service> searchService(String service) {
    return (ArrayList<Service>) serviceService.searchService(service);
  }
}
