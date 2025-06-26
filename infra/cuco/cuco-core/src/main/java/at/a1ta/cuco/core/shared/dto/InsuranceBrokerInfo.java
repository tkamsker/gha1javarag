package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class InsuranceBrokerInfo implements Serializable {

  private static final long serialVersionUID = 1L;

  public static final int ERROR = 99;
  public static final int LOADING = -1;
  public static final int NOT_RECEIVED = 98;
  public static final int LOADED = 0;

  private int status = LOADING;

  private int monthLeft;
  private Boolean costFreeClaimInd;
  private String marketingContractTypeName;
  private Boolean contractInd;
  private Boolean contractTypeEligible;
  private String deviceMarketingName;
  private String imei;

  private List<InsuranceBrokerContractInfo> contractInfo = new ArrayList<InsuranceBrokerContractInfo>();

  public InsuranceBrokerInfo() {
    // default constructor to support GWT parsing
  }

  public InsuranceBrokerInfo(int status) {
    super();
    this.status = status;
  }

  public int getStatus() {
    return status;
  }

  public void setStatus(int status) {
    this.status = status;
  }

  public int getMonthLeft() {
    return monthLeft;
  }

  public void setMonthLeft(int monthLeft) {
    this.monthLeft = monthLeft;
  }

  public Boolean getCostFreeClaimInd() {
    return costFreeClaimInd;
  }

  public void setCostFreeClaimInd(Boolean costFreeClaimInd) {
    this.costFreeClaimInd = costFreeClaimInd;
  }

  public String getMarketingContractTypeName() {
    return marketingContractTypeName;
  }

  public void setMarketingContractTypeName(String marketingContractTypeName) {
    this.marketingContractTypeName = marketingContractTypeName;
  }

  public Boolean getContractInd() {
    return contractInd;
  }

  public void setContractInd(Boolean contractInd) {
    this.contractInd = contractInd;
  }

  public Boolean getContractTypeEligible() {
    return contractTypeEligible;
  }

  public void setContractTypeEligible(Boolean contractTypeEligible) {
    this.contractTypeEligible = contractTypeEligible;
  }

  public String getDeviceMarketingName() {
    return deviceMarketingName;
  }

  public void setDeviceMarketingName(String deviceMarkingName) {
    this.deviceMarketingName = deviceMarkingName;
  }

  public String getImei() {
    return imei;
  }

  public void setImei(String imei) {
    this.imei = imei;
  }

  public List<InsuranceBrokerContractInfo> getContractInfo() {
    return contractInfo;
  }

  public void setContractInfo(List<InsuranceBrokerContractInfo> contractInfo) {
    this.contractInfo = contractInfo;
  }

  public void addToContractInfo(InsuranceBrokerContractInfo contractInfo) {
    if (this.contractInfo == null) {
      this.contractInfo = new ArrayList<InsuranceBrokerContractInfo>();
    }
    this.contractInfo.add(contractInfo);
  }

}
