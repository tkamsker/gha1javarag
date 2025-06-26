package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Comparator;
import java.util.Date;

public class Invoice implements Serializable {
  private static final String BOB_INVOICE_ID_PREFIX = "5000";
  private static final int BOB_INVOICE_ID_MIN_LENGTH = 12;

  public static class InvoiceDateComparator implements Comparator<Invoice>, Serializable {
    @Override
    public int compare(Invoice o1, Invoice o2) {
      return o1.invoiceDate.compareTo(o2.invoiceDate) * -1;
    }
  }

  private Long invoiceId;
  private Long clearingAccountNumber;
  private Long customerId;
  private Date invoiceDate;
  private Date paymentDate;
  private float totalFee;
  private long invoiceRunId;
  private float totalGrossFee;
  private float totalPaymentFee;
  private boolean mobile;

  public Long getCustomerId() {
    return customerId;
  }

  public void setCustomerId(Long customerId) {
    this.customerId = customerId;
  }

  public Date getInvoiceDate() {
    return invoiceDate;
  }

  public void setInvoiceDate(Date invoiceDate) {
    this.invoiceDate = invoiceDate;
  }

  public Date getPaymentDate() {
    return paymentDate;
  }

  public void setPaymentDate(Date paymentDate) {
    this.paymentDate = paymentDate;
  }

  public float getTotalFee() {
    return totalFee;
  }

  public void setTotalFee(float totalFee) {
    this.totalFee = totalFee;
  }

  public Long getInvoiceId() {
    return this.invoiceId;
  }

  public void setInvoiceId(Long invoiceId) {
    this.invoiceId = invoiceId;
  }

  public Long getClearingAccountNumber() {
    return clearingAccountNumber;
  }

  public void setClearingAccountNumber(Long clearingAccountNumber) {
    this.clearingAccountNumber = clearingAccountNumber;
  }

  public long getInvoiceRunId() {
    return invoiceRunId;
  }

  public void setInvoiceRunId(long invoiceRunId) {
    this.invoiceRunId = invoiceRunId;
  }

  public float getTotalGrossFee() {
    return totalGrossFee;
  }

  public void setTotalGrossFee(float totalGrossFee) {
    this.totalGrossFee = totalGrossFee;
  }

  public boolean isMobile() {
    return mobile;
  }

  public void setMobile(boolean mobile) {
    this.mobile = mobile;
  }

  public boolean isBobInvoice() {
    String invoiceIdStr = invoiceId + "";
    return isMobile() && invoiceIdStr.length() >= BOB_INVOICE_ID_MIN_LENGTH && invoiceIdStr.startsWith(BOB_INVOICE_ID_PREFIX);
  }

  public void setTotalPaymentFee(float totalPaymentFee) {
    this.totalPaymentFee = totalPaymentFee;
  }

  public float getTotalPaymentFee() {
    return totalPaymentFee;
  }
}
