package at.a1ta.cuco.admin.ui.common.client.service;

import java.util.ArrayList;
import java.util.List;

import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;

import at.a1ta.cuco.core.shared.dto.product.CCTOrgStructureElement;

@RemoteServiceRelativePath("cuco/cctorgstructureelement.rpc")
public interface CCTOrgStructureElementServlet extends RemoteService {

  List<String> getAllUsers();

  public void eraseOldEntries();

  void updateCCTOrg(ArrayList<CCTOrgStructureElement> user);
}