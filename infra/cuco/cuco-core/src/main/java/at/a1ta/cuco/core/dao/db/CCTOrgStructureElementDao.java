package at.a1ta.cuco.core.dao.db;

import java.util.ArrayList;
import java.util.List;

import at.a1ta.cuco.core.shared.dto.product.CCTOrgStructureElement;

public interface CCTOrgStructureElementDao {

  List<String> getAllUsers();

  void eraseOldEntries();

  void updateCCTOrg(CCTOrgStructureElement user);

  void deleteAllAndBatchInsertInTransaction(ArrayList<CCTOrgStructureElement> user);

}