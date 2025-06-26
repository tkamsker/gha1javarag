package at.a1ta.cuco.core.service;

import at.a1ta.cuco.core.shared.dto.product.AutoVvlInfo;
import at.a1ta.cuco.core.shared.dto.product.CallNumber;

public interface AutoVvlService {

  public AutoVvlInfo getAutoVvlInfoByCallNumber(CallNumber cn);

  public AutoVvlInfo getAutoVvlInfoByBan(String banNumber);
}
