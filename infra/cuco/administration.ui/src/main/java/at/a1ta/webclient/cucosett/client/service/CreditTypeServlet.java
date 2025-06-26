package at.a1ta.webclient.cucosett.client.service;

import java.util.ArrayList;

import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;

import at.a1ta.cuco.core.shared.dto.CreditType;
import at.a1ta.framework.ui.client.dto.RpcStatus;

@RemoteServiceRelativePath("cuco/creditType.rpc")
public interface CreditTypeServlet extends RemoteService {
  public ArrayList<CreditType> getAllCreditTypes();

  public CreditType saveCreditType(CreditType ct);

  public RpcStatus deleteCreditType(Long id);
}
