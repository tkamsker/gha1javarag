package at.a1ta.cuco.core.dao.db.impl;

import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import org.springframework.orm.ibatis.SqlMapClientCallback;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.GamificationLocalDAO;
import at.a1ta.cuco.core.shared.dto.GamificationMessage;

import com.ibatis.sqlmap.client.SqlMapExecutor;

@SuppressWarnings("deprecation")
public class GamificationLocalDAOImpl extends AbstractDao implements GamificationLocalDAO {

  @SuppressWarnings("deprecation")
  @Override
  public void markAllMessagesRead(final ArrayList<GamificationMessage> messages, final String agentId) {
    getSqlMapClientTemplate().execute(new SqlMapClientCallback<Void>() {

      @Override
      public Void doInSqlMapClient(SqlMapExecutor executor) throws SQLException {
        executor.startBatch();
        Iterator<GamificationMessage> iter = messages.iterator();
        while (iter.hasNext()) {
          Map<String, Object> params = new HashMap<String, Object>(2);
          params.put("agentUserId", agentId);
          params.put("messageUid", iter.next().getMessageUid());
          executor.update("Gamification.markMessageAsRead", params);
        }
        executor.executeBatch();
        return null;
      }
    });
  }

  @SuppressWarnings("deprecation")
  @Override
  public void addAllMessagesToCuCoDB(final ArrayList<GamificationMessage> messages, final String agentId) {
    getSqlMapClientTemplate().execute(new SqlMapClientCallback<Void>() {

      @Override
      public Void doInSqlMapClient(SqlMapExecutor executor) throws SQLException {
        executor.startBatch();
        Iterator<GamificationMessage> iter = messages.iterator();
        while (iter.hasNext()) {
          Map<String, Object> params = new HashMap<String, Object>(2);
          params.put("agentUserId", agentId);
          params.put("message", iter.next());
          executor.insert("Gamification.insert", params);
        }
        executor.executeBatch();
        return null;
      }
    });

  }

  @SuppressWarnings("unchecked")
  @Override
  public Map<String, GamificationMessage> getAlreadyStoredMessages(ArrayList<GamificationMessage> messages, String agentId) {
    Map<String, Object> params = new HashMap<String, Object>(2);
    params.put("agentUserId", agentId);
    ArrayList<String> messageIds = new ArrayList<String>();
    for (GamificationMessage msg : messages) {
      messageIds.add(msg.getMessageUid());
    }
    params.put("messageIds", messageIds);
    return (Map<String, GamificationMessage>) performMapQuery("Gamification.getAlreadyStoredMessages", params, "messageUid");
  }

  @Override
  public String creatGamificationOneTimeToken(String userName, String token) {
    Map<String, Object> params = new HashMap<String, Object>(2);
    params.put("agentUserId", userName);
    params.put("token", token);
    executeInsert("Gamification.creatGamificationOneTimeToken", params);
    return token;
  }

  @Override
  public Boolean validateGamificationOneTimeToken(String token) {
    Map<String, Object> params = new HashMap<String, Object>(2);
    params.put("token", token);
    int count = performObjectQuery("Gamification.getMatchingActiveTokensCount", params);
    if (count == 1) {
      executeUpdate("Gamification.expireGamificationOneTimeToken", params);
      return true;
    }
    return false;
  }

}
