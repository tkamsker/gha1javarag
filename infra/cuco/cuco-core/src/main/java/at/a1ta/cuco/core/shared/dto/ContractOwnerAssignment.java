package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.List;

public class ContractOwnerAssignment implements Serializable {
  private String partyId;
  private List<BillingAccountNumber> accounts;

  public String getPartyId() {
    return partyId;
  }

  public void setPartyId(String partyId) {
    this.partyId = partyId;
  }

  public List<BillingAccountNumber> getAccounts() {
    return accounts;
  }

  public void setAccounts(List<BillingAccountNumber> accounts) {
    this.accounts = accounts;
  }

}
