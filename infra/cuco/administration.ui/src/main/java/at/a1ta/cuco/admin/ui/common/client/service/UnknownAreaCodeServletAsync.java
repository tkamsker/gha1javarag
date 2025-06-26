package at.a1ta.cuco.admin.ui.common.client.service;

import java.util.ArrayList;

import com.google.gwt.user.client.rpc.AsyncCallback;

import at.a1ta.cuco.core.shared.dto.UnknownAreaCode;
import at.a1ta.framework.ui.client.dto.RpcStatus;

public interface UnknownAreaCodeServletAsync {
  public void getAllUnknownAreaCodes(AsyncCallback<ArrayList<UnknownAreaCode>> callback);

  public void saveUnknownAreaCode(UnknownAreaCode code, AsyncCallback<UnknownAreaCode> callback);

  public void deleteUnknownAreaCode(Long id, AsyncCallback<RpcStatus> callback);
}
