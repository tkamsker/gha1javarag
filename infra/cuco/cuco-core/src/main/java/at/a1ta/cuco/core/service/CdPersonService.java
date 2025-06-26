package at.a1ta.cuco.core.service;

import java.util.List;

import at.a1ta.bite.core.shared.dto.cd.CdPerson;

public interface CdPersonService {

  public List<CdPerson> getPersons(List<String> userNames);

  public CdPerson getPerson(String userName);

}
