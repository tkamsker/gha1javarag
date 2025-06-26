package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class PartyAdditionalInfo implements Serializable {
  private static final long serialVersionUID = 1L;
  private ServiceClassInfo serviceClassInfo;
  private PointOfSaleInfo pointOfSaleInfo;
  private PartyDeclarationOfConsentInfo partyDeclarationOfConsentInfo;
  private PartyProfileInfo partyProfileInfo;
  private PartyCustomerLoyaltyInfo partyCustomerLoyaltyInfo;

  public PartyAdditionalInfo() {
    // default constructor to support GWT parsing
  }

  public PointOfSaleInfo getPointOfSaleInfo() {
    return pointOfSaleInfo;
  }

  public void setPointOfSaleInfo(PointOfSaleInfo pointOfSaleInfo) {
    this.pointOfSaleInfo = pointOfSaleInfo;
  }

  public ServiceClassInfo getServiceClassInfo() {
    return serviceClassInfo;
  }

  public void setServiceClassInfo(ServiceClassInfo serviceClassInfo) {
    this.serviceClassInfo = serviceClassInfo;
  }

  public PartyDeclarationOfConsentInfo getPartyDeclarationOfConsentInfo() {
    return partyDeclarationOfConsentInfo;
  }

  public void setPartyDeclarationOfConsentInfo(PartyDeclarationOfConsentInfo partyDeclarationOfConsentInfo) {
    this.partyDeclarationOfConsentInfo = partyDeclarationOfConsentInfo;
  }

  public PartyProfileInfo getPartyProfileInfo() {
    return partyProfileInfo;
  }

  public void setPartyProfileInfo(PartyProfileInfo partyProfileInfo) {
    this.partyProfileInfo = partyProfileInfo;
  }

  public PartyCustomerLoyaltyInfo getPartyCustomerLoyaltyInfo() {
    return partyCustomerLoyaltyInfo;
  }

  public void setPartyCustomerLoyaltyInfo(PartyCustomerLoyaltyInfo partyCustomerLoyaltyInfo) {
    this.partyCustomerLoyaltyInfo = partyCustomerLoyaltyInfo;
  }

}
