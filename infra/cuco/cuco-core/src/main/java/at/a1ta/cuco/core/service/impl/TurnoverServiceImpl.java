package at.a1ta.cuco.core.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.db.TurnoverDao;
import at.a1ta.cuco.core.service.TurnoverService;
import at.a1ta.cuco.core.shared.dto.Turnover;

@Service
public class TurnoverServiceImpl implements TurnoverService {

  @Autowired
  private TurnoverDao turnoverDao;

  @Override
  public List<Turnover> getAllForParty(long partyId) {
    return turnoverDao.getAllForParty(partyId);
  }
}
