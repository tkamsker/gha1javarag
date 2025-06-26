package at.a1ta.webclient.cucosett.client.service;

import java.util.ArrayList;

import com.google.gwt.user.client.rpc.AsyncCallback;

import at.a1ta.cuco.core.shared.dto.CreditType;
import at.a1ta.framework.ui.client.dto.RpcStatus;

public interface CreditTypeServletAsync {
  public void getAllCreditTypes(AsyncCallback<ArrayList<CreditType>> callback);

  public void saveCreditType(CreditType ct, AsyncCallback<CreditType> callback);

  public void deleteCreditType(Long id, AsyncCallback<RpcStatus> callback);
}
