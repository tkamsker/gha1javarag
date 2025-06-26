package at.a1ta.cuco.admin.ui.common.client.service;

import java.util.ArrayList;

import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;

import at.a1ta.cuco.core.shared.dto.UnknownAreaCode;
import at.a1ta.framework.ui.client.dto.RpcStatus;

@RemoteServiceRelativePath("cuco/unknownAreaCode.rpc")
public interface UnknownAreaCodeServlet extends RemoteService {
  public ArrayList<UnknownAreaCode> getAllUnknownAreaCodes();

  public UnknownAreaCode saveUnknownAreaCode(UnknownAreaCode code);

  public RpcStatus deleteUnknownAreaCode(Long id);
}
