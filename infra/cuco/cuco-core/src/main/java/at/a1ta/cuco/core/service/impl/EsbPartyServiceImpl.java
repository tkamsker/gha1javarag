package at.a1ta.cuco.core.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.esb.EsbPartyDao;
import at.a1ta.cuco.core.service.EsbPartyService;
import at.a1ta.cuco.core.shared.dto.EsbParty;
import at.a1telekom.eai.party.Party;

@Service
public class EsbPartyServiceImpl implements EsbPartyService {

  private EsbPartyDao esbPartyDao;

  @Override
  public Party getParty(long partyId) {
    return esbPartyDao.getParty(partyId);
  }
  
  @Override
  public EsbParty getESBParty(long partyId) {
    return esbPartyDao.getESBParty(partyId);
  }

  @Autowired
  public void setEsbPartyDao(EsbPartyDao esbPartyDao) {
    this.esbPartyDao = esbPartyDao;
  }
}
