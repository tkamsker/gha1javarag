package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class PartyCustomerLoyaltyInfo implements Serializable {

  private static final long serialVersionUID = 1L;

  public static final int ERROR = 99;
  public static final int LOADING = -1;
  public static final int NOT_RECEIVED = 98;
  public static final int LOADED = 0;

  private int staus = LOADING;
  private boolean isConnectPlusCustomer;

  public PartyCustomerLoyaltyInfo() {
    // default constructor to support GWT parsing
  }

  public PartyCustomerLoyaltyInfo(int staus) {
    this.staus = staus;
  }

  public int getStaus() {
    return staus;
  }

  public void setStaus(int staus) {
    this.staus = staus;
  }

  public boolean isConnectPlusCustomer() {
    return isConnectPlusCustomer;
  }

  public void setConnectPlusCustomer(boolean isConnectPlusCustomer) {
    this.isConnectPlusCustomer = isConnectPlusCustomer;
  }

}
