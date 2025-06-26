package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.db.CCTOrgStructureElementDao;
import at.a1ta.cuco.core.service.CCTOrgStructureElementService;
import at.a1ta.cuco.core.shared.dto.product.CCTOrgStructureElement;

@Service
public class CCTOrgStructureElementServiceImpl implements CCTOrgStructureElementService {
  private CCTOrgStructureElementDao cCTOrgStructureElementDao;

  @Autowired
  public void setcCTOrgStructureElementDao(CCTOrgStructureElementDao cCTOrgStructureElementDao) {
    this.cCTOrgStructureElementDao = cCTOrgStructureElementDao;
  }

  @Override
  public void updateCCTOrg(ArrayList<CCTOrgStructureElement> cctClearanceOrgStructure) {
    cCTOrgStructureElementDao.deleteAllAndBatchInsertInTransaction(cctClearanceOrgStructure);
  }

  @Override
  public List<String> getAllUsers() {
    return cCTOrgStructureElementDao.getAllUsers();
  }

  @Override
  public void eraseOldEntries() {
    cCTOrgStructureElementDao.eraseOldEntries();
  }
}
