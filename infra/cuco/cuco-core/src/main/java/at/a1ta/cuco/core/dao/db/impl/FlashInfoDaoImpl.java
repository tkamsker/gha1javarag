package at.a1ta.cuco.core.dao.db.impl;

import java.sql.SQLException;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.orm.ibatis.SqlMapClientCallback;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.FlashInfoDao;
import at.a1ta.cuco.core.shared.dto.FlashInfo;
import at.a1ta.cuco.core.shared.dto.Tupel;

import com.ibatis.sqlmap.client.SqlMapExecutor;

public class FlashInfoDaoImpl extends AbstractDao implements FlashInfoDao {

  @Override
  public FlashInfo getFlashInfoById(long flashId) {
    return (FlashInfo) performObjectQuery("FlashInfo.get", flashId);
  }

  @Override
  public List<FlashInfo> getAllFlashInfos() {
    return performListQuery("FlashInfo.get");
  }

  @Override
  public List<FlashInfo> getFlashInfoForUserAndCustomer(long userId, long customerId) {
    HashMap<String, Object> params = new HashMap<String, Object>();
    params.put("userId", userId);
    params.put("kundeId", customerId);

    return performListQuery("FlashInfo.getForUserAndCustomer", params);
  }

  @Override
  public List<FlashInfo> loadMyFlashInfos(Map<String, Object> params) {
    return performListQuery("FlashInfo.filterFlashInfos", params);
  }

  @Override
  public void insertFlashInfo(FlashInfo flashInfo) {
    executeInsert("FlashInfo.insert", flashInfo);
  }

  @Override
  public void updateFlashInfo(FlashInfo flashInfo) {
    executeUpdate("FlashInfo.update", flashInfo);
  }

  @Override
  public void deleteFlashInfo(long flashId) {
    executeDelete("FlashInfo.delete", flashId);
  }

  @SuppressWarnings("deprecation")
  @Override
  public void insertFlashCustomer(final Collection<Tupel<Long, Long>> tupel) {
    getSqlMapClientTemplate().execute(new SqlMapClientCallback<Long>() {
      @Override
      public Long doInSqlMapClient(SqlMapExecutor executor) throws SQLException {
        executor.startBatch();
        for (Tupel<Long, Long> values : tupel) {
          HashMap<String, Object> params = new HashMap<String, Object>();
          params.put("flashId", values.getValue1());
          params.put("kundeId", values.getValue2());

          executor.insert("FlashInfo.insertFlashKunde", params);
        }
        executor.executeBatch();
        return (long) tupel.size();
      }
    });
  }

  @Override
  public void deleteFlashCustomerForFlash(long flashId) {
    executeDelete("FlashInfo.deleteFlashKundeForFlash", flashId);
  }

  @Override
  public void insertFlashRole(long flashInfoId, String roleName) {
    HashMap<String, Object> params = new HashMap<String, Object>();
    params.put("flashId", flashInfoId);
    params.put("roleName", roleName);

    executeInsert("FlashInfo.insertFlashRolle", params);
  }

  @Override
  public void deleteFlashRoleForFlash(long flashId) {
    executeDelete("FlashInfo.deleteFlashRolleForFlash", flashId);
  }

  @Override
  public void insertFlashViewed(long flashInfoId, long partyId, long userId) {
    HashMap<String, Object> params = new HashMap<String, Object>();
    params.put("flashId", flashInfoId);
    params.put("kundeId", partyId);
    params.put("userId", userId);

    executeInsert("FlashInfo.insertView", params);
  }
}
