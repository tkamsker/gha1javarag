package at.a1ta.cuco.core.service;

import java.util.ArrayList;
import java.util.List;

import at.a1ta.cuco.core.shared.dto.product.CCTOrgStructureElement;

public interface CCTOrgStructureElementService {
  public List<String> getAllUsers();

  public void eraseOldEntries();

  void updateCCTOrg(ArrayList<CCTOrgStructureElement> user);

}
