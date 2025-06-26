package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;
import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class PaymentNew implements Serializable {
  private static final long serialVersionUID = 1L;

  private boolean a1Mastercard;
  private BigDecimal a1MastercardPrice;
  private String a1MastercardText;

  private boolean appStoreA1Invoice; // App Store ueber A1 Rechnung
  private BigDecimal appStoreA1InvoicePrice;
  private String appStoreA1InvoiceText;

  private String comment;
  private BigDecimal sum;

  public boolean isA1Mastercard() {
    return a1Mastercard;
  }

  public void setA1Mastercard(boolean a1Mastercard) {
    this.a1Mastercard = a1Mastercard;
  }

  public BigDecimal getA1MastercardPrice() {
    return a1MastercardPrice;
  }

  public void setA1MastercardPrice(BigDecimal a1MastercardPrice) {
    this.a1MastercardPrice = a1MastercardPrice;
  }

  public String getA1MastercardText() {
    return a1MastercardText;
  }

  public void setA1MastercardText(String a1MastercardText) {
    this.a1MastercardText = a1MastercardText;
  }

  public boolean isAppStoreA1Invoice() {
    return appStoreA1Invoice;
  }

  public void setAppStoreA1Invoice(boolean appStoreA1Invoice) {
    this.appStoreA1Invoice = appStoreA1Invoice;
  }

  public BigDecimal getAppStoreA1InvoicePrice() {
    return appStoreA1InvoicePrice;
  }

  public void setAppStoreA1InvoicePrice(BigDecimal appStoreA1InvoicePrice) {
    this.appStoreA1InvoicePrice = appStoreA1InvoicePrice;
  }

  public String getAppStoreA1InvoiceText() {
    return appStoreA1InvoiceText;
  }

  public void setAppStoreA1InvoiceText(String appStoreA1InvoiceText) {
    this.appStoreA1InvoiceText = appStoreA1InvoiceText;
  }

  public String getComment() {
    return comment;
  }

  public void setComment(String comment) {
    this.comment = comment;
  }

  public BigDecimal getSum() {
    return sum;
  }

  public void setSum(BigDecimal sum) {
    this.sum = sum;
  }

  @Override
  public String toString() {
    return "PaymentNew [a1Mastercard=" + a1Mastercard + ", a1MastercardPrice=" + a1MastercardPrice + ", a1MastercardText=" + a1MastercardText + ", appStoreA1Invoice=" + appStoreA1Invoice
        + ", appStoreA1InvoicePrice=" + appStoreA1InvoicePrice + ", appStoreA1InvoiceText=" + appStoreA1InvoiceText + ", comment=" + comment + ", sum=" + sum + "]";
  }

}
