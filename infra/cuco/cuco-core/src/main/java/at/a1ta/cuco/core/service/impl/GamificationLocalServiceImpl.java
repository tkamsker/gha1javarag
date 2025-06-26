package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;
import java.util.Map;

import org.apache.commons.lang.math.RandomUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.db.GamificationLocalDAO;
import at.a1ta.cuco.core.service.GamificationLocalService;
import at.a1ta.cuco.core.shared.dto.GamificationMessage;

@Service
public class GamificationLocalServiceImpl implements GamificationLocalService {

  @Autowired
  private GamificationLocalDAO gamificationLocalDAO;

  @Override
  public void markAllMessagesRead(ArrayList<GamificationMessage> messages, String agentId) {
    gamificationLocalDAO.markAllMessagesRead(messages, agentId);
  }

  @Override
  public void addAllMessagesToCuCoDB(ArrayList<GamificationMessage> messages, String agentId) {
    gamificationLocalDAO.addAllMessagesToCuCoDB(messages, agentId);
  }

  @Override
  public Map<String, GamificationMessage> getAlreadyStoredMessages(ArrayList<GamificationMessage> messages, String agentId) {
    return gamificationLocalDAO.getAlreadyStoredMessages(messages, agentId);
  }

  @Override
  public String getGamificationToken(String userName) {
    return gamificationLocalDAO.creatGamificationOneTimeToken(userName, userName + "-" + System.currentTimeMillis() + RandomUtils.nextInt());
  }

  @Override
  public Boolean validateGamificationOneTimeToken(String token) {
    if (token != null && (token.contains("/"))) {
      token = token.replaceAll("/", "");
    }
    return gamificationLocalDAO.validateGamificationOneTimeToken(token);
  }

}
