package at.a1ta.cuco.core.dao.esb;

import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;
import at.a1ta.cuco.core.shared.dto.mobilpoints.MobilPoints;

public interface MobilPointsDao {

  public MobilPoints getMobilPoints(PhoneNumberStructure phoneNumber);

}