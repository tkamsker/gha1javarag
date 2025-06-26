package at.a1ta.cuco.admin.ui.common.client.service;

import java.util.ArrayList;

import com.google.gwt.user.client.rpc.AsyncCallback;

import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.framework.ui.client.dto.RpcStatus;

public interface ServiceServletAsync {
  void deleteService(Long id, AsyncCallback<RpcStatus> callback);

  void getAllServices(AsyncCallback<ArrayList<Service>> callback);

  void saveService(Service ct, AsyncCallback<Service> callback);

  void searchService(String service, AsyncCallback<ArrayList<Service>> callback);
}
