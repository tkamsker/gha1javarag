package at.a1ta.cuco.core.service;

import at.a1ta.cuco.core.shared.dto.GamificationRequest;
import at.a1ta.cuco.core.shared.dto.GamificationResponse;

public interface GamificationHttpService {
  GamificationResponse getAvailableGamificationMessages(GamificationRequest message, String endpoint);
}
