package at.a1ta.cuco.core.service;

import at.a1ta.cuco.core.shared.dto.product.BRKAccountInfo;

public interface BrkServiceClient {

  public BRKAccountInfo getBRKAccountInfo(String brkAccountNumber);

  public String getBRKAccountNumber(String banNumber);

  public BRKAccountInfo getBRKAccountInfoForBAN(String banNumber);
}
