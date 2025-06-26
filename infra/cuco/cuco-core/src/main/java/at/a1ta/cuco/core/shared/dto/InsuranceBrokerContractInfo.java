package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class InsuranceBrokerContractInfo implements Serializable {

  private static final long serialVersionUID = 1L;

  private String marketingContractTypeName;
  private String deviceMarketingName;
  private String imei;

  public InsuranceBrokerContractInfo() {
    // default constructor to support GWT parsing
  }

  public InsuranceBrokerContractInfo(String marketingContractTypeName, String deviceMarketingName, String imei) {
    super();
    this.marketingContractTypeName = marketingContractTypeName;
    this.deviceMarketingName = deviceMarketingName;
    this.imei = imei;
  }

  public String getMarketingContractTypeName() {
    return marketingContractTypeName;
  }

  public void setMarketingContractTypeName(String marketingContractTypeName) {
    this.marketingContractTypeName = marketingContractTypeName;
  }

  public String getDeviceMarketingName() {
    return deviceMarketingName;
  }

  public void setDeviceMarketingName(String deviceMarketingName) {
    this.deviceMarketingName = deviceMarketingName;
  }

  public String getImei() {
    return imei;
  }

  public void setImei(String imei) {
    this.imei = imei;
  }

}
