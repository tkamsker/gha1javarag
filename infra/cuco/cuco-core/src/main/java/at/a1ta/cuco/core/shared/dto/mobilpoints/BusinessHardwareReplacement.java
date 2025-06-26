package at.a1ta.cuco.core.shared.dto.mobilpoints;

import java.io.Serializable;
import java.math.BigDecimal;
import java.math.BigInteger;

public class BusinessHardwareReplacement implements Serializable {
  private long billingAccountNumber;
  private BigInteger simCount;
  private BigDecimal bindingMonthsPerSim;
  private BigInteger openBasicFeePerBan;
  private BigInteger possibleHardwareReplacement;
  private boolean businessRewardingAccountsAvailable = true;

  public long getBillingAccountNumber() {
    return billingAccountNumber;
  }

  public void setBillingAccountNumber(long billingAccountNumber) {
    this.billingAccountNumber = billingAccountNumber;
  }

  public BigInteger getSimCount() {
    return simCount;
  }

  public void setSimCount(BigInteger nbActiveSims) {
    this.simCount = nbActiveSims;
  }

  public BigDecimal getBindingMonthsPerSim() {
    return bindingMonthsPerSim;
  }

  public void setBindingMonthsPerSim(BigDecimal rmCommitmentPerSim) {
    this.bindingMonthsPerSim = rmCommitmentPerSim;
  }

  public BigInteger getOpenBasicFeePerBan() {
    return openBasicFeePerBan;
  }

  public void setOpenBasicFeePerBan(BigInteger nbOGE) {
    this.openBasicFeePerBan = nbOGE;
  }

  public BigInteger getPossibleHardwareReplacement() {
    return possibleHardwareReplacement;
  }

  public void setPossibleHardwareReplacement(BigInteger possibleHWRedemptionVoice) {
    this.possibleHardwareReplacement = possibleHWRedemptionVoice;
  }

  public void setBusinessRewardingAccountsAvailable(boolean isAvailable) {
    this.businessRewardingAccountsAvailable = isAvailable;
  }

  public boolean hasBusinessRewardingAccounts() {
    return businessRewardingAccountsAvailable;
  }
}
