package at.a1ta.cuco.core.service.mycuco;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.lang.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.shared.dto.Filter;
import at.a1ta.bite.core.shared.dto.FilterCollection;
import at.a1ta.cuco.core.dao.db.FlashInfoDao;
import at.a1ta.cuco.core.dao.db.PartyDao;
import at.a1ta.cuco.core.shared.dto.FlashInfo;
import at.a1ta.cuco.core.shared.dto.Party;

@Service
public class MyFlashInfosServiceImpl implements MyFlashInfosService {

  private FlashInfoDao flashInfoDao;

  private PartyDao partyDao;

  @Override
  public List<FlashInfo> loadFlashInfosForAgent(FilterCollection filters, String agentUuser) {
    Map<String, Object> params = new HashMap<String, Object>();

    Filter<String> filter = filters.getStringFilter("partyId");
    String value = filter.getSelectedValues();
    Long partyId = Long.valueOf(value);
    params.put("partyId", partyId);

    filter = filters.getStringFilter("title");
    value = filter.getSelectedValues();
    if (StringUtils.isNotBlank(value)) {
      params.put("title", value);
    }

    return flashInfoDao.loadMyFlashInfos(params);
  }

  @Override
  public List<Party> loadPartiesOfFlashInfoAndAgent(Long flashInfoId, String username) {
    return partyDao.loadPartiesOfFlashInfo(flashInfoId, username);
  }

  @Autowired
  public void setFlashInfoDao(FlashInfoDao flashInfoDao) {
    this.flashInfoDao = flashInfoDao;
  }

  @Autowired
  @Qualifier("cucoCustomerDao")
  public void setPartyDao(PartyDao partyDao) {
    this.partyDao = partyDao;
  }
}
