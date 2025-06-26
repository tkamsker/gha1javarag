package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.ArrayList;

public class ClearingAccount implements Serializable, Comparable<ClearingAccount> {
  private Long accountNumber;
  private Long ban;
  private Long ben;
  private Long partyId;
  private String invoiceType;
  private String invoiceReceiverSalution;
  private String invoiceReceiverTitle;
  private String invoiceReceiverName;
  private String invoiceAddressLine1;
  private String invoiceAddressLine2;
  private ArrayList<Invoice> invoices;
  private boolean virtualClearingAccountMobile;
  private boolean virtualClearingAccountFixedLine;
  private boolean active;

  public ClearingAccount() {}

  public ClearingAccount(Long accountNumber) {
    this.accountNumber = accountNumber;
  }

  public Long getAccountNumber() {
    return accountNumber;
  }

  public void setAccountNumber(Long accountNumber) {
    this.accountNumber = accountNumber;
  }

  public String getBanBenAccountNumber() {
    return ban + "/" + ben;
  }

  public Long getBan() {
    return ban;
  }

  public void setBan(Long ban) {
    this.ban = ban;
  }

  public Long getBen() {
    return ben;
  }

  public void setBen(Long ben) {
    this.ben = ben;
  }

  public Long getPartyId() {
    return partyId;
  }

  public void setPartyId(Long partyId) {
    this.partyId = partyId;
  }

  public String getInvoiceType() {
    return invoiceType;
  }

  public void setInvoiceType(String invoiceType) {
    this.invoiceType = invoiceType;
  }

  public boolean hasInvoiceType() {
    return invoiceType != null && !invoiceType.isEmpty();
  }

  public String getInvoiceReceiverFullName() {
    String fullName = "";
    if (invoiceReceiverSalution != null) {
      fullName += invoiceReceiverSalution + " ";
    }
    if (invoiceReceiverTitle != null) {
      fullName += invoiceReceiverTitle + " ";
    }
    if (invoiceReceiverName != null) {
      fullName += invoiceReceiverName;
    }
    return fullName;
  }

  public String getInvoiceReceiverSalution() {
    return invoiceReceiverSalution;
  }

  public void setInvoiceReceiverSalution(String invoiceReceiverSalution) {
    this.invoiceReceiverSalution = invoiceReceiverSalution;
  }

  public String getInvoiceReceiverTitle() {
    return invoiceReceiverTitle;
  }

  public void setInvoiceReceiverTitle(String invoiceReceiverTitle) {
    this.invoiceReceiverTitle = invoiceReceiverTitle;
  }

  public String getInvoiceReceiverName() {
    return invoiceReceiverName;
  }

  public void setInvoiceReceiverName(String invoiceReceiverName) {
    this.invoiceReceiverName = invoiceReceiverName;
  }

  public String getInvoiceAddressLine1() {
    return invoiceAddressLine1;
  }

  public void setInvoiceAddressLine1(String invoiceAddressLine1) {
    this.invoiceAddressLine1 = invoiceAddressLine1;
  }

  public String getInvoiceAddressLine2() {
    return invoiceAddressLine2;
  }

  public void setInvoiceAddressLine2(String invoiceAddressLine2) {
    this.invoiceAddressLine2 = invoiceAddressLine2;
  }

  public ArrayList<Invoice> getInvoices() {
    return invoices;
  }

  public void setInvoices(ArrayList<Invoice> invoices) {
    this.invoices = invoices;
  }

  public boolean hasInvoices() {
    return invoices != null && !invoices.isEmpty();
  }

  public void addInvoices(Invoice invoice) {
    if (invoices == null) {
      invoices = new ArrayList<Invoice>();
    }
    invoices.add(invoice);
  }

  public float getNettoSum() {
    BigDecimal sum = new BigDecimal(0F);
    if (hasInvoices()) {
      for (Invoice invoice : invoices) {
        sum = sum.add(new BigDecimal(invoice.getTotalFee()));
      }
    }
    return sum.floatValue();
  }

  public float getBruttoSum() {
    BigDecimal sum = new BigDecimal(0F);
    if (hasInvoices()) {
      for (Invoice invoice : invoices) {
        sum = sum.add(new BigDecimal(invoice.getTotalGrossFee()));
      }
    }
    return sum.floatValue();
  }

  public float getPaymentSum() {
    BigDecimal sum = new BigDecimal(0F);
    if (hasInvoices()) {
      for (Invoice invoice : invoices) {
        sum = sum.add(new BigDecimal(invoice.getTotalPaymentFee()));
      }
    }
    return sum.floatValue();
  }

  public boolean isVirtualClearingAccount() {
    return virtualClearingAccountMobile || virtualClearingAccountFixedLine;
  }

  public boolean isVirtualClearingAccountMobile() {
    return virtualClearingAccountMobile;
  }

  public boolean isVirtualClearingAccountFixedLine() {
    return virtualClearingAccountFixedLine;
  }

  public void setVirtualClearingAccountMobile(boolean virtualClearingAccountMobile) {
    this.virtualClearingAccountMobile = virtualClearingAccountMobile;
  }

  public void setVirtualClearingAccountFixedLine(boolean virtualClearingAccountFixedLine) {
    this.virtualClearingAccountFixedLine = virtualClearingAccountFixedLine;
  }

  public boolean isMobileAccount() {
    return ban != null;
  }

  public boolean isFixedLineAccount() {
    return !isMobileAccount();
  }

  public void setActive(boolean active) {
    this.active = active;
  }

  public boolean isActive() {
    return active;
  }

  @Override
  public boolean equals(Object obj) {
    if (!(obj instanceof ClearingAccount)) {
      return false;
    }

    ClearingAccount other = ((ClearingAccount) obj);
    return (accountNumber == null && other.accountNumber == null) || (accountNumber != null && accountNumber.equals(other.accountNumber));
  }

  @Override
  public int hashCode() {
    return accountNumber != null ? accountNumber.hashCode() : super.hashCode();
  }

  @Override
  public int compareTo(ClearingAccount o) {
    if (accountNumber == null || o.accountNumber == null) {
      return 0;
    }
    return accountNumber.compareTo(o.accountNumber);
  }

}
