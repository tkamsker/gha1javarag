package at.a1ta.cuco.core.dao.esb;

import at.a1ta.cuco.core.shared.dto.mobilpoints.BusinessHardwareReplacement;

public interface BusinessHardwareReplacementDao {

  public BusinessHardwareReplacement getBusinessHardwareReplacement(long billingAccountNumber);

}