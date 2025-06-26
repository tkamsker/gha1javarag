package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class SecurityNew extends SecurityBase {
  private boolean a1CyberProtectionSingle;
  private BigDecimal a1CyberProtectionSinglePrice;
  private boolean a1CyberProtectionFamily;
  private BigDecimal a1CyberProtectionFamilyPrice;
  private String a1CyberProtectionText;

  private boolean a1Mastercard;
  private BigDecimal a1MastercardPrice;

  public boolean isA1CyberProtectionSingle() {
    return a1CyberProtectionSingle;
  }

  public void setA1CyberProtectionSingle(boolean a1CyberProtectionSingle) {
    this.a1CyberProtectionSingle = a1CyberProtectionSingle;
  }

  public BigDecimal getA1CyberProtectionSinglePrice() {
    return a1CyberProtectionSinglePrice;
  }

  public void setA1CyberProtectionSinglePrice(BigDecimal a1CyberProtectionSinglePrice) {
    this.a1CyberProtectionSinglePrice = a1CyberProtectionSinglePrice;
  }

  public boolean isA1CyberProtectionFamily() {
    return a1CyberProtectionFamily;
  }

  public void setA1CyberProtectionFamily(boolean a1CyberProtectionFamily) {
    this.a1CyberProtectionFamily = a1CyberProtectionFamily;
  }

  public BigDecimal getA1CyberProtectionFamilyPrice() {
    return a1CyberProtectionFamilyPrice;
  }

  public void setA1CyberProtectionFamilyPrice(BigDecimal a1CyberProtectionFamilyPrice) {
    this.a1CyberProtectionFamilyPrice = a1CyberProtectionFamilyPrice;
  }

  public String getA1CyberProtectionText() {
    return a1CyberProtectionText;
  }

  public void setA1CyberProtectionText(String a1CyberProtectionText) {
    this.a1CyberProtectionText = a1CyberProtectionText;
  }

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

  @Override
  public String toString() {
    return "SecurityNew [a1CyberProtectionSingle=" + a1CyberProtectionSingle + ", a1CyberProtectionSinglePrice=" + a1CyberProtectionSinglePrice + ", a1CyberProtectionFamily=" + a1CyberProtectionFamily
        + ", a1CyberProtectionFamilyPrice=" + a1CyberProtectionFamilyPrice + ", a1CyberProtectionText=" + a1CyberProtectionText + ", a1Mastercard=" + a1Mastercard + ", a1MastercardPrice="
        + a1MastercardPrice + "]";
  }

}
