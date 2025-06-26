package at.a1ta.cuco.core.shared.dto;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

import org.apache.solr.client.solrj.beans.Field;

import at.a1ta.bite.core.shared.dto.KumsSkzShop;
import at.a1ta.cuco.core.shared.dto.PartyDeclarationOfConsentInfo.StatusOfCompleteness;

public class Party extends Customer {
  private static final long serialVersionUID = 1L;
  private static final String CREDIT_WORTHINESS_GREEN = "grün";
  private static final String CREDIT_WORTHINESS_YELLOW = "gelb";
  private static final String CREDIT_WORTHINESS_RED = "rot";
  private static final String SBS = "SBS";

  private VipStatus vipStatus;
  private String vipTooltip;
  private String leadId;
  private String leadNote;
  private ServiceClassInfo serviceClassInfo = new ServiceClassInfo();
  private int type;
  private int marker;
  private boolean active = true;
  private ArrayList<BillingAccountNumber> billingAccountNumbers;
  private boolean hierarchical;
  private List<Party> children = new ArrayList<Party>();
  private BigDecimal turnover;
  private int flashInfoCount;
  private ArrayList<MobileChurnLikeliness> mobileChurnLikeliness;
  private String maxMobileChurnLikeliness;
  private KumsSkzShop kumsSkzShop;
  private IndexationStatus idxStatus = IndexationStatus.NOT_AVAILABLE;
  private PointOfSaleInfo posInfo = new PointOfSaleInfo(PointOfSaleInfo.LOADING, "", "");
  private PartyDeclarationOfConsentInfo declarationOfConsentInfo = new PartyDeclarationOfConsentInfo(PartyDeclarationOfConsentInfo.LOADING, StatusOfCompleteness.UNKNOWN);
  private PartyProfileInfo partyProfileInfo = new PartyProfileInfo(PartyProfileInfo.LOADING);
  private CrmAuthenticationInfo crmAuthenticationInfo = new CrmAuthenticationInfo(CrmAuthenticationInfo.LOADING);
  private PartyCustomerLoyaltyInfo partyCustomerLoyaltyInfo = new PartyCustomerLoyaltyInfo();
  private String emptySeparatorString;
  private String cmBuddyLink;

  public Party() {}

  public Party(long partyId) {
    this.setId(partyId);
  }

  public VipStatus getVipStatus() {
    return vipStatus;
  }

  public void setVipStatus(VipStatus vipStatus) {
    this.vipStatus = vipStatus;
  }

  public boolean isVip() {
    return vipStatus != null && (vipStatus.getIntValue() != null || vipStatus.getState() == VipStatus.State.VIP);
  }

  public String getVipTooltip() {
    return vipTooltip;
  }

  public void setVipTooltip(String vipTooltip) {
    this.vipTooltip = vipTooltip;
  }

  @Field("dualsegment")
  public void setType(int type) {
    this.type = type;
  }

  public int getType() {
    return type;
  }

  public int getMarker() {
    return marker;
  }

  public void setMarker(int marker) {
    this.marker = marker;
  }

  public String getFullname() {
    if (getTitle() != null) {
      return getTitle() + " " + getFirstname() + " " + getLastname();
    }
    return getFirstname() + " " + getLastname();
  }

  public String getName() {
    String firstname = getFirstname();
    if (firstname == null || firstname.length() == 0) {
      return getLastname();
    }
    return firstname + " " + getLastname();
  }

  public ArrayList<BillingAccountNumber> getBillingAccountNumbers() {
    return billingAccountNumbers;
  }

  public void setBillingAccountNumbers(ArrayList<BillingAccountNumber> billingAccountNumbers) {
    this.billingAccountNumbers = billingAccountNumbers;
  }

  public boolean hasBillingAccountNumbers() {
    return this.billingAccountNumbers != null && !this.billingAccountNumbers.isEmpty();
  }

  public boolean hasSupportUser() {
    return getSupportUserId() != null && !getSupportUserId().equalsIgnoreCase("Kein Be");
  }

  public boolean isActive() {
    return active;
  }

  public void setActive(boolean active) {
    this.active = active;
  }

  public boolean hasCreditWorthinessGreen() {
    return CREDIT_WORTHINESS_GREEN.equalsIgnoreCase(getCreditworthiness());
  }

  public boolean hasCreditWorthinessYellow() {
    return CREDIT_WORTHINESS_YELLOW.equalsIgnoreCase(getCreditworthiness());
  }

  public boolean hasCreditWorthinessRed() {
    return CREDIT_WORTHINESS_RED.equalsIgnoreCase(getCreditworthiness());
  }

  public boolean hasKnownCreditworthiness() {
    return hasCreditWorthinessGreen() || hasCreditWorthinessYellow() || hasCreditWorthinessRed();
  }

  public boolean hasIndexedProduct() {
    return IndexationStatus.INDEXED.equals(IndexationStatus.getForDWHValue(getIndexation()));
  }

  public boolean hasIndexedProductNotUsed() {
    return IndexationStatus.INDEXED_NOT_STARTED.equals(IndexationStatus.getForDWHValue(getIndexation()));
  }

  public boolean hasIndexedExcluded() {
    return IndexationStatus.NOT_INDEXED.equals(IndexationStatus.getForDWHValue(getIndexation()));
  }

  public boolean hasKnownIndexed() {
    return !IndexationStatus.NOT_AVAILABLE.equals(IndexationStatus.getForDWHValue(getIndexation()));

  }

  public boolean isHierarchical() {
    return hierarchical;
  }

  public void setHierarchical(boolean hierarchical) {
    this.hierarchical = hierarchical;
  }

  public boolean isTaCustomer() {
    return type == 1 || type == 3 || type == 5 || type == 7;
  }

  @Override
  public boolean equals(Object obj) {
    if (!(obj instanceof Party)) {
      return false;
    }
    Party otherParty = (Party) obj;
    return otherParty != null && getId() == otherParty.getId();
  }

  @Override
  public int hashCode() {
    return (int) (getId() ^ (getId() >>> 32)); // default hashCode algo.
  }

  @Override
  public String toString() {
    return "Party: partyId=" + getId();
  }

  public void addChild(Party party) {
    if (!children.contains(party)) {
      children.add(party);
    }
  }

  public List<Party> getChildren() {
    return children;
  }

  public BigDecimal getTurnover() {
    return turnover;
  }

  public void setTurnover(BigDecimal turnover) {
    this.turnover = turnover;
  }

  public void setFlashInfoCount(int flashInfoCount) {
    this.flashInfoCount = flashInfoCount;
  }

  public int getFlashInfoCount() {
    return flashInfoCount;
  }

  public void setMobileChurnLikeliness(ArrayList<MobileChurnLikeliness> mobileChurnLikeliness) {
    this.mobileChurnLikeliness = mobileChurnLikeliness;
  }

  public ArrayList<MobileChurnLikeliness> getMobileChurnLikeliness() {
    return mobileChurnLikeliness;
  }

  public void setMaxMobileChurnLikeliness(String maxMobileChurnLikeliness) {
    this.maxMobileChurnLikeliness = maxMobileChurnLikeliness;
  }

  public String getMaxMobileChurnLikeliness() {
    return maxMobileChurnLikeliness;
  }

  public KumsSkzShop getKumsSkzShop() {
    return kumsSkzShop;
  }

  public void setKumsSkzShop(KumsSkzShop kumsSkzShop) {
    this.kumsSkzShop = kumsSkzShop;
  }

  public String getLeadId() {
    return leadId;
  }

  public void setLeadId(String leadId) {
    this.leadId = leadId;
  }

  public String getLeadNote() {
    return leadNote;
  }

  public void setLeadNote(String leadNote) {
    this.leadNote = leadNote;
  }

  public boolean isLead() {
    return (getId() <= 0 && getLeadId() != null && !getLeadId().trim().isEmpty()) || getType() == 9;
  }

  public String getUniqueKey() {
    return getId() + getLeadId();
  }

  public String getPartyIdentifier() {
    return getId() == 0 ? getLeadId() : String.valueOf(getId());
  }

  public IndexationStatus getIdxStatus() {
    if (idxStatus.equals(IndexationStatus.NOT_AVAILABLE) && getIndexation() != null && getIndexation().trim().length() > 0) {
      idxStatus = IndexationStatus.getForDWHValue(getIndexation());
    }
    return idxStatus;
  }

  public void setIdxStatus(IndexationStatus idxStatus) {
    this.idxStatus = idxStatus;
  }

  public void setIdxStatus(String idxStatus) {
    this.idxStatus = IndexationStatus.getForDWHValue(idxStatus);
  }

  public ServiceClassInfo getServiceClassInfo() {
    return serviceClassInfo;
  }

  public void setServiceClassInfo(ServiceClassInfo serviceClassInfo) {
    this.serviceClassInfo = serviceClassInfo;
  }

  public PointOfSaleInfo getPOSInfo() {
    return posInfo;
  }

  @Field("posInfo")
  public void setPOSInfo(PointOfSaleInfo posInfo) {
    this.posInfo = posInfo;
  }

  public boolean isSBSCustomer() {
    return SBS.equalsIgnoreCase(getBusinessSegment());
  }

  @Field("betreuteStelleCd")
  public void setBetreuteStelleCd(String betreuteStelleCd) {
    if (this.kumsSkzShop == null) {
      this.kumsSkzShop = new KumsSkzShop();
    }
    this.kumsSkzShop.setBetreuteStelleCd(betreuteStelleCd);
  }

  @Field("betreuteStelleNam")
  public void setBetreuteStelleNam(String betreuteStelleNam) {
    if (this.kumsSkzShop == null) {
      this.kumsSkzShop = new KumsSkzShop();
    }
    this.kumsSkzShop.setBetreuteStelleNam(betreuteStelleNam);
  }

  @Field("isAttendent")
  public void setIsAttendent(String shopBetreut) {
    if (this.kumsSkzShop == null) {
      this.kumsSkzShop = new KumsSkzShop();
    }
    this.kumsSkzShop.setShopBetreut(shopBetreut != null && shopBetreut.equalsIgnoreCase("true"));
  }

  public PartyDeclarationOfConsentInfo getDeclarationOfConsentInfo() {
    return declarationOfConsentInfo;
  }

  public void setDeclarationOfConsentInfo(PartyDeclarationOfConsentInfo declarationOfConsentInfo) {
    this.declarationOfConsentInfo = declarationOfConsentInfo;
  }

  public PartyProfileInfo getPartyProfileInfo() {
    return partyProfileInfo;
  }

  public void setPartyProfileInfo(PartyProfileInfo partyProfileInfo) {
    this.partyProfileInfo = partyProfileInfo;
  }

  public CrmAuthenticationInfo getCrmAuthenticationInfo() {
    return crmAuthenticationInfo;
  }

  public void setCrmAuthenticationInfo(CrmAuthenticationInfo crmAuthenticationInfo) {
    this.crmAuthenticationInfo = crmAuthenticationInfo;
  }

  public String getEmptySeparatorString() {
    return emptySeparatorString;
  }

  public void setEmptySeparatorString(String emptySeparatorString) {
    this.emptySeparatorString = emptySeparatorString;
  }

  public PartyCustomerLoyaltyInfo getPartyCustomerLoyaltyInfo() {
    return partyCustomerLoyaltyInfo;
  }

  public void setPartyCustomerLoyaltyInfo(PartyCustomerLoyaltyInfo partyCustomerLoyaltyInfo) {
    this.partyCustomerLoyaltyInfo = partyCustomerLoyaltyInfo;
  }

  public String getCmBuddyLink() {
    return cmBuddyLink;
  }

  public void setCmBuddyLink(String cmBuddyLink) {
    this.cmBuddyLink = cmBuddyLink;
  }

}
