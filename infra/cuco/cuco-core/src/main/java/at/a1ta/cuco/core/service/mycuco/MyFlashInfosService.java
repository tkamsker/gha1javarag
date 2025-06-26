package at.a1ta.cuco.core.service.mycuco;

import java.util.List;

import at.a1ta.bite.core.shared.dto.FilterCollection;
import at.a1ta.cuco.core.shared.dto.FlashInfo;
import at.a1ta.cuco.core.shared.dto.Party;

public interface MyFlashInfosService {

  List<FlashInfo> loadFlashInfosForAgent(FilterCollection filters, String agentUuser);

  List<Party> loadPartiesOfFlashInfoAndAgent(Long flashInfoId, String username);

}
