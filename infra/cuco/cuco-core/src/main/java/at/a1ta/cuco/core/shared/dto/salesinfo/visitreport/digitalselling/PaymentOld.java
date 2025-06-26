package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;
import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class PaymentOld implements Serializable {
  private static final long serialVersionUID = 1L;

  private String appsPaymentTypeText;
  private String shoppingPaymentTypeText;
  private String travelPaymentTypeText;
  private String mobilePaymentTypeText;
  private String creditCardTypeText;
  private BigDecimal creditCardTypePrice;

  private String comment;
  private BigDecimal sum;

  public String getAppsPaymentTypeText() {
    return appsPaymentTypeText;
  }

  public void setAppsPaymentTypeText(String appsPaymentTypeText) {
    this.appsPaymentTypeText = appsPaymentTypeText;
  }

  public String getShoppingPaymentTypeText() {
    return shoppingPaymentTypeText;
  }

  public void setShoppingPaymentTypeText(String shoppingPaymentTypeText) {
    this.shoppingPaymentTypeText = shoppingPaymentTypeText;
  }

  public String getTravelPaymentTypeText() {
    return travelPaymentTypeText;
  }

  public void setTravelPaymentTypeText(String travelPaymentTypeText) {
    this.travelPaymentTypeText = travelPaymentTypeText;
  }

  public String getMobilePaymentTypeText() {
    return mobilePaymentTypeText;
  }

  public void setMobilePaymentTypeText(String mobilePaymentTypeText) {
    this.mobilePaymentTypeText = mobilePaymentTypeText;
  }

  public String getCreditCardTypeText() {
    return creditCardTypeText;
  }

  public void setCreditCardTypeText(String creditCardTypeText) {
    this.creditCardTypeText = creditCardTypeText;
  }

  public BigDecimal getCreditCardTypePrice() {
    return creditCardTypePrice;
  }

  public void setCreditCardTypePrice(BigDecimal creditCardTypePrice) {
    this.creditCardTypePrice = creditCardTypePrice;
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
    return "PaymentOld [appsPaymentTypeText=" + appsPaymentTypeText + ", shoppingPaymentTypeText=" + shoppingPaymentTypeText + ", travelPaymentTypeText=" + travelPaymentTypeText
        + ", mobilePaymentTypeText=" + mobilePaymentTypeText + ", creditCardTypeText=" + creditCardTypeText + ", creditCardTypePrice=" + creditCardTypePrice + ", comment=" + comment + ", sum=" + sum
        + "]";
  }

}
