package at.a1ta.cuco.admin.ui.common.client.service;

import java.util.ArrayList;

import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;

import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.framework.ui.client.dto.RpcStatus;

@RemoteServiceRelativePath("cuco/service.rpc")
public interface ServiceServlet extends RemoteService {
  public ArrayList<Service> getAllServices();

  public Service saveService(Service ct);

  public RpcStatus deleteService(Long id);

  public ArrayList<Service> searchService(String service);
}
