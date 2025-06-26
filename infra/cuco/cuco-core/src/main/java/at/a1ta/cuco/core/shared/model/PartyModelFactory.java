package at.a1ta.cuco.core.shared.model;

import at.a1ta.cuco.core.shared.dto.BillingAccountNumber;
import at.a1ta.cuco.core.shared.dto.MobileChurnLikeliness;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PartyCustomerLoyaltyInfo;
import at.a1ta.cuco.core.shared.dto.PartyProfileInfo;
import at.a1ta.cuco.core.shared.dto.PartyProfileNPSInfo;
import at.a1ta.cuco.core.shared.dto.PointOfSaleInfo;
import at.a1ta.cuco.core.shared.dto.ServiceClassInfo;
import at.a1ta.cuco.core.shared.dto.VipStatus.State;

public class PartyModelFactory {

  enum MobileChurnLikelinessType {
    HIGH(2), MEDIUM(3), LOW(4), NONE(5), UNKNOWN(6);

    private final int order;

    MobileChurnLikelinessType(int order) {
      this.order = order;
    }

    public int getOrder() {
      return order;
    }
  }

  private static final String PRIO_UNKNOWN_TEXT = "1. Unbekannt";
  private static final String PRIO_HIGH_TEXT = "2. Hoch";
  private static final String PRIO_MEDIUM_TEXT = "3. Mittel";
  private static final String PRIO_LOW_TEXT = "4. Gering";
  private static final String PRIO_NONE_TEXT = "5. Kein";

  private static final String DISPLAY_UNKNOWN_TEXT = "Unbekannt";
  private static final String DISPLAY_HIGH_TEXT = "Hoch";
  private static final String DISPLAY_MEDIUM_TEXT = "Mittel";
  private static final String DISPLAY_LOW_TEXT = "Gering";
  private static final String DISPLAY_NONE_TEXT = "Kein";

  public static PartyModel createPartyModel(Party party) {
    PartyModel result = new PartyModel();

    result.setId(party.getId());
    result.setCommercialRegisterNumber(party.getCommercialRegisterNumber());
    result.setBusinessSegment(party.getBusinessSegment());
    result.setServiceClass((!(party.isSBSCustomer() && (party.getServiceClassInfo() != null && party.getServiceClassInfo().getServiceClass() != ServiceClassInfo.SERVICE_CLASS_NOT_RECEIVED)))
        || party.getServiceClassInfo().getServiceClassText() == null ? "" : party.getServiceClassInfo().getServiceClassText());
    result.setGender(getGender(party));
    result.setFirstname(party.getFirstname());
    result.setLastname(party.getLastname());
    result.setAddressLine1(party.getAddressLine1());
    result.setAddressLine2(party.getAddressLine2());
    result.setBirthdate(party.getBirthdate());
    result.setRegion(party.getRegion());
    result.setTeamName(party.getTeamName());
    result.setSupportUserName(!isAttended(party) ? party.getSupportUserName() : "Kein Betreuer");
    result.setIndexation(party.getIndexation());
    result.setAttendingShop(isAttended(party) ? party.getKumsSkzShop().getBetreuteStelleNam() : "Kein Shop");
    result.setNpsString(getNPSText(party));
    result.setCustomerType(getCustomerType(party));
    result.setType(getType(party) + (party.isLead() ? ("(" + party.getLeadId() + ")") : ""));
    result.setChurnLikeliness(getDisplayChurnText(party.getChurnLikeliness()));
    result.setCustomerWorthiness(party.getCustomerWorthclass());
    result.setFramework(party.isListedInFramework() ? "ja" : "nein");
    result.setCreditworthiness(party.getCreditworthiness());
    result.setFaxNumber(party.getFaxNumber());
    result.setVipStatus(getVipStatus(party));
    result.setAssocRegisterNumber(party.getCentralAssociationNumber());
    result.setBinding(party.getCurrentBinding());
    result.setCooperation(party.getCooperationDescription());
    result.setBans(getBans(party));
    result.setPosString(getPOSText(party));
    result.setEveStatus(getEVEText(party));
    if (party.getMobileChurnLikeliness() != null && !party.getMobileChurnLikeliness().isEmpty()) {
      result.setAccumulatedChurnLikeliness(getDisplayChurnText(getAccumulatedChurnLikeliness(party)));
    }
    result.setA1ConnectPlusInfo(getA1ConnectPlusText(party));
    return result;
  }

  private static String getPOSText(Party party) {
    if (party.getPOSInfo() != null) {
      if (party.getPOSInfo().getStaus() == PointOfSaleInfo.LOADING) {
        return "wird geladen...";
      } else if (party.getPOSInfo().getStaus() == PointOfSaleInfo.LOADED) {
        return party.getPOSInfo().getNameAddressString();
      } else if (party.getPOSInfo().getStaus() == PointOfSaleInfo.ERROR) {
        return "nicht verfügbar";
      } else {
        return "-";
      }
    }
    return "-";
  }

  private static String getEVEText(Party party) {
    if (party.getDeclarationOfConsentInfo() != null) {
      if (party.getDeclarationOfConsentInfo().getStaus() == PointOfSaleInfo.LOADING) {
        return "wird geladen...";
      } else if (party.getDeclarationOfConsentInfo().getStaus() == PointOfSaleInfo.LOADED) {
        return party.getDeclarationOfConsentInfo().getStatusNeedForAction().getDisplayText();
      } else if (party.getDeclarationOfConsentInfo().getStaus() == PointOfSaleInfo.ERROR) {
        return "nicht verfügbar";
      } else {
        return "-";
      }
    }
    return "-";
  }

  private static String getNPSText(Party party) {
    if (party.getPartyProfileInfo() != null) {
      if (party.getPartyProfileInfo().getStaus() == PartyProfileInfo.LOADING) {
        return "wird geladen...";
      } else if (party.getPartyProfileInfo().getStaus() == PartyProfileInfo.LOADED) {
        if (party.getPartyProfileInfo().getScores().isEmpty()) {
          return "-";
        } else {
          StringBuilder sb = new StringBuilder();
          for (PartyProfileNPSInfo partyProfileNPSInfo : party.getPartyProfileInfo().getScores()) {
            sb.append(partyProfileNPSInfo.getCompleteNpsStatus() + "\n");
          }
          return sb.toString();
        }
      } else if (party.getPartyProfileInfo().getStaus() == PartyProfileInfo.ERROR) {
        return "NPS kann nicht abgefragt werden.";
      } else {
        return "-";
      }
    }
    return "-";
  }

  private static String getA1ConnectPlusText(Party party) {
    if (party.getPartyCustomerLoyaltyInfo() != null) {
      if (party.getPartyCustomerLoyaltyInfo().getStaus() == PartyCustomerLoyaltyInfo.LOADING) {
        return "wird geladen...";
      } else if (party.getPartyCustomerLoyaltyInfo().getStaus() == PartyCustomerLoyaltyInfo.LOADED) {
        return party.getPartyCustomerLoyaltyInfo().isConnectPlusCustomer() ? "aktiv" : "-";
      } else if (party.getPartyCustomerLoyaltyInfo().getStaus() == PartyCustomerLoyaltyInfo.ERROR) {
        return "Connect Plus Status kann nicht abgefragt werden.";
      } else {
        return "-";
      }
    }
    return "-";
  }

  private static boolean isAttended(Party party) {
    return party.getKumsSkzShop() != null && party.getKumsSkzShop().isShopBetreut();
  }

  public static String getDisplayChurnText(String churnLikeliness) {
    if (churnLikeliness == null) {
      return DISPLAY_UNKNOWN_TEXT;
    }
    if (churnLikeliness.startsWith("2")) {
      return DISPLAY_HIGH_TEXT;
    }
    if (churnLikeliness.startsWith("3")) {
      return DISPLAY_MEDIUM_TEXT;
    }
    if (churnLikeliness.startsWith("4")) {
      return DISPLAY_LOW_TEXT;
    }
    if (churnLikeliness.startsWith("5")) {
      return DISPLAY_NONE_TEXT;
    }
    return DISPLAY_UNKNOWN_TEXT;
  }

  private static String getAccumulatedChurnLikeliness(Party party) {
    String wiredChurn = convertWiredChurnLikeliness(party.getChurnLikeliness());
    String mobileChurn = getMaxMobileChurnLikeliness(party);

    if (wiredChurn == null || wiredChurn.startsWith("(")) {
      return MobileChurnLikelinessType.UNKNOWN.name().equalsIgnoreCase(mobileChurn) ? DISPLAY_UNKNOWN_TEXT : mobileChurn;
    }
    if (mobileChurn == null || mobileChurn.equalsIgnoreCase(MobileChurnLikelinessType.UNKNOWN.name())) {
      return wiredChurn;
    }
    int churnId = Integer.parseInt(wiredChurn.charAt(0) + "");
    int mobileChurnId = Integer.parseInt(mobileChurn.charAt(0) + "");

    return churnId > mobileChurnId ? mobileChurn : wiredChurn;
  }

  private static String getMaxMobileChurnLikeliness(Party party) {
    MobileChurnLikelinessType maxChurn = MobileChurnLikelinessType.UNKNOWN;
    for (MobileChurnLikeliness churn : party.getMobileChurnLikeliness()) {
      String likeliness = churn.getChurnLikeliness() == null ? MobileChurnLikelinessType.UNKNOWN.name() : churn.getChurnLikeliness();
      if (MobileChurnLikelinessType.valueOf(likeliness).getOrder() < maxChurn.getOrder()) {
        maxChurn = MobileChurnLikelinessType.valueOf(likeliness);
      }
    }
    party.setMaxMobileChurnLikeliness(maxChurn.name());

    return convertMobileChurnLikeliness(party.getMaxMobileChurnLikeliness());
  }

  private static String convertWiredChurnLikeliness(String churnLikeliness) {
    if (churnLikeliness == null) {
      return null;
    }
    if (churnLikeliness.contains(DISPLAY_HIGH_TEXT)) {
      return PRIO_HIGH_TEXT;
    }
    if (churnLikeliness.contains(DISPLAY_MEDIUM_TEXT)) {
      return PRIO_MEDIUM_TEXT;
    }
    if (churnLikeliness.contains(DISPLAY_LOW_TEXT)) {
      return PRIO_LOW_TEXT;
    }
    if (churnLikeliness.contains(DISPLAY_NONE_TEXT)) {
      return PRIO_NONE_TEXT;
    }
    return PRIO_UNKNOWN_TEXT;
  }

  private static String convertMobileChurnLikeliness(String churnLikeliness) {
    if (churnLikeliness == null) {
      return null;
    }
    if (churnLikeliness.equalsIgnoreCase(MobileChurnLikelinessType.HIGH.name())) {
      return PRIO_HIGH_TEXT;
    }
    if (churnLikeliness.equalsIgnoreCase(MobileChurnLikelinessType.MEDIUM.name())) {
      return PRIO_MEDIUM_TEXT;
    }
    if (churnLikeliness.equalsIgnoreCase(MobileChurnLikelinessType.LOW.name())) {
      return PRIO_LOW_TEXT;
    }
    if (churnLikeliness.equalsIgnoreCase(MobileChurnLikelinessType.NONE.name())) {
      return PRIO_NONE_TEXT;
    }
    return PRIO_UNKNOWN_TEXT;
  }

  private static String getVipStatus(Party party) {
    String result;

    if (party.getVipStatus() == null) {
      result = "Daten werden geladen ...";
    } else if (party.isVip()) {
      result = "VIP";
    } else if (party.getVipStatus().getState() == State.UNKNOWN) {
      result = "unbekannt";
    } else {
      result = "Kein VIP";
    }

    return result;
  }

  private static String getType(Party party) {
    return getType(party.getType());
  }

  public static String getType(int type) {
    return DualSegment.get(type).name();
  }

  public static String getTitle(int type) {
    return DualSegment.get(type).getTitle();
  }

  private static String getBans(Party party) {
    StringBuilder result = new StringBuilder();
    if (party.getBillingAccountNumbers() == null || party.getBillingAccountNumbers().size() == 0) {
      return result.toString();
    }

    int idx = 0;
    for (BillingAccountNumber ban : party.getBillingAccountNumbers()) {
      if (idx++ > 0) {
        result.append(", ");
      }
      result.append(ban.getBan());
    }

    return result.toString();
  }

  private static String getCustomerType(Party party) {
    if ("Per".equals(party.getCustomerType())) {
      return "Person";
    }
    if ("Org".equals(party.getCustomerType())) {
      return "Organisation";
    }
    return "";
  }

  private static String getGender(Party party) {
    if ("M".equals(party.getGender())) {
      return "Herr";
    }
    if ("W".equals(party.getGender()) || "F".equals(party.getGender())) {
      return "Frau";
    }
    return "Firma";
  }

}
