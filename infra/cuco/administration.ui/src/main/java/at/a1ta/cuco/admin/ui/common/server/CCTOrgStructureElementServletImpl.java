package at.a1ta.cuco.admin.ui.common.server;

import javax.servlet.annotation.WebServlet;
import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.ui.server.servlet.AuthenticationServlet;
import at.a1ta.cuco.admin.ui.common.client.service.CCTOrgStructureElementServlet;
import at.a1ta.cuco.core.dao.db.CCTOrgStructureElementDao;
import at.a1ta.cuco.core.service.CCTOrgStructureElementService;
import at.a1ta.cuco.core.shared.dto.product.CCTOrgStructureElement;

@WebServlet(name = "cctorgstructureelement", urlPatterns = {"/admin/cuco/cctorgstructureelement.rpc"})
public class CCTOrgStructureElementServletImpl extends AuthenticationServlet implements CCTOrgStructureElementServlet {

  @Autowired
  private CCTOrgStructureElementService cctOrgStructureElementService;

  private CCTOrgStructureElementDao cctOrgStructureElementDao;

  @Autowired
  public void setCctOrgStructureElementDao(CCTOrgStructureElementDao cctOrgStructureElementDao) {
    this.cctOrgStructureElementDao = cctOrgStructureElementDao;
  }

  @Override
  public List<String> getAllUsers() {
    return cctOrgStructureElementService.getAllUsers();
  }

  @Override
  public void eraseOldEntries() {
    cctOrgStructureElementService.eraseOldEntries();
  }

  @Override
  public void updateCCTOrg(ArrayList<CCTOrgStructureElement> user) {
    for (CCTOrgStructureElement cctOrgElement : user) {
      cctOrgStructureElementDao.updateCCTOrg(cctOrgElement);
    }
  }

}
