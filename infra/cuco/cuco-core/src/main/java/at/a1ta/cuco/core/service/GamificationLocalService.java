package at.a1ta.cuco.core.service;

import java.util.ArrayList;
import java.util.Map;

import at.a1ta.cuco.core.shared.dto.GamificationMessage;

public interface GamificationLocalService {
  public void markAllMessagesRead(ArrayList<GamificationMessage> messages, String agentId);

  public void addAllMessagesToCuCoDB(ArrayList<GamificationMessage> messages, String agentId);

  public Map<String, GamificationMessage> getAlreadyStoredMessages(ArrayList<GamificationMessage> messages, String agentId);

  public String getGamificationToken(String userName);

  public Boolean validateGamificationOneTimeToken(String token);

}
