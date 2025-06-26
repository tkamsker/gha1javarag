package at.a1ta.cuco.core.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.dao.cd.CdPersonDao;
import at.a1ta.bite.core.shared.dto.cd.CdPerson;
import at.a1ta.cuco.core.service.CdPersonService;

@Service
public class CdPersonServiceImpl implements CdPersonService {

  @Autowired
  private CdPersonDao cdPersonDao;

  @Override
  public List<CdPerson> getPersons(List<String> userNames) {
    return cdPersonDao.getPersons(userNames);
  }

  @Override
  public CdPerson getPerson(String userName) {
    return cdPersonDao.getPerson(userName);
  }

}
