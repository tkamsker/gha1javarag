package at.a1ta.cuco.core.dao.db.impl;

import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import com.ibatis.sqlmap.client.SqlMapClient;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.CCTOrgStructureElementDao;
import at.a1ta.cuco.core.shared.dto.product.CCTOrgStructureElement;

public class CCTOrgStructureElementDaoImpl extends AbstractDao implements CCTOrgStructureElementDao {

  @Override
  public List<String> getAllUsers() {
    return performListQuery("User.getAllLogin");
  }

  @Override
  public void eraseOldEntries() {
    executeDelete("CCTOrgStructureElement.eraseOldEntries", null);
  }

  @Override
  public void updateCCTOrg(CCTOrgStructureElement user) {
    executeInsert("CCTOrgStructureElement.insertCCTOrgStructureElements", user);
  }

  @Override
  public void deleteAllAndBatchInsertInTransaction(ArrayList<CCTOrgStructureElement> user) {
    executeDeleteAllAndBatchInsertInTransaction("CCTOrgStructureElement.eraseOldEntries", null, "CCTOrgStructureElement.insertCCTOrgStructureElements", user);
  }

  private void executeDeleteAllAndBatchInsertInTransaction(final String deleteStatementName, final Object deleteParameter, final String insertStatementName,
      final ArrayList<CCTOrgStructureElement> insertList) {
    SqlMapClient sqlMapClient = this.getSqlMapClientTemplate().getSqlMapClient();
    try {
      sqlMapClient.startTransaction();
      sqlMapClient.startBatch();
      sqlMapClient.delete(deleteStatementName, deleteParameter);
      for (CCTOrgStructureElement user : insertList) {
        logger.trace("Inserting user: " + user);
        sqlMapClient.insert(insertStatementName, user);
      }
      sqlMapClient.commitTransaction();
      logger.debug("Inserting Finished.");
    } catch (RuntimeException e) {
      handleException(insertList, e);
      throw e;
    } catch (SQLException e) {
      handleException(insertList, e);
      throw new RuntimeException(e);
    } finally {
      try {
        sqlMapClient.endTransaction();
      } catch (SQLException e) {
        logger.error(e.getMessage(), e);
      }
    }
  }

}