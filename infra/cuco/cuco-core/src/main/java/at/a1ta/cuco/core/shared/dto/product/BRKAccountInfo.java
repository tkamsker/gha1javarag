package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

public class BRKAccountInfo implements Serializable {

  private String accountNumber;

  private String accountStatus;

  private String accountName;

  private String handlingFee;

  public String getAccountNumber() {
    return accountNumber;
  }

  public void setAccountNumber(String accountNumber) {
    this.accountNumber = accountNumber;
  }

  public String getAccountStatus() {
    return accountStatus;
  }

  public void setAccountStatus(String accountStatus) {
    this.accountStatus = accountStatus;
  }

  public String getAccountName() {
    return accountName;
  }

  public void setAccountName(String accountName) {
    this.accountName = accountName;
  }

  public String getHandlingFee() {
    return handlingFee;
  }

  public void setHandlingFee(String handlingFee) {
    this.handlingFee = handlingFee;
  }

}
