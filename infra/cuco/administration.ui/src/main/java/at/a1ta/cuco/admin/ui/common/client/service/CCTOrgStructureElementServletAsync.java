package at.a1ta.cuco.admin.ui.common.client.service;

import java.util.ArrayList;
import java.util.List;

import com.google.gwt.user.client.rpc.AsyncCallback;

import at.a1ta.cuco.core.shared.dto.product.CCTOrgStructureElement;

public interface CCTOrgStructureElementServletAsync {

  public void getAllUsers(AsyncCallback<List<String>> callback);

  void eraseOldEntries(AsyncCallback<Void> callback);

  void updateCCTOrg(ArrayList<CCTOrgStructureElement> user, AsyncCallback<Void> callback);
}
