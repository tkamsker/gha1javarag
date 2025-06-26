package at.a1ta.cuco.core.service;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PointOfSaleInfo;
import at.a1ta.cuco.core.shared.dto.salesinfo.ToDoGroupNote;

public interface POSService {

  public void sendPOSChangeEmail(Party party, PointOfSaleInfo current, PointOfSaleInfo requested, String justification, UserInfo userInfo);

  public void sendToDoAssignedToPOSEmail(Party party, ToDoGroupNote current, PointOfSaleInfo requested, String justification, BiteUser authenticatedUser);

  void sendToDoCompletedToPOSEmail(Party party, ToDoGroupNote groupNote, PointOfSaleInfo requestedPOS, String justification, BiteUser user);

}
