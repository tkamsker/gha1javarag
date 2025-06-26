package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;
import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class SecurityBase implements Serializable {
  private static final long serialVersionUID = 1L;

  private boolean internetProtection;
  private BigDecimal internetProtectionPrice;
  private String internetProtectionText;

  private String comment;

  private BigDecimal sum;

  public boolean isInternetProtection() {
    return internetProtection;
  }

  public void setInternetProtection(boolean internetProtection) {
    this.internetProtection = internetProtection;
  }

  public BigDecimal getInternetProtectionPrice() {
    return internetProtectionPrice;
  }

  public void setInternetProtectionPrice(BigDecimal internetProtectionPrice) {
    this.internetProtectionPrice = internetProtectionPrice;
  }

  public String getInternetProtectionText() {
    return internetProtectionText;
  }

  public void setInternetProtectionText(String internetProtectionText) {
    this.internetProtectionText = internetProtectionText;
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
    return "SecurityBase [internetProtection=" + internetProtection + ", internetProtectionPrice=" + internetProtectionPrice + ", internetProtectionText=" + internetProtectionText + ", comment="
        + comment + ", sum=" + sum + "]";
  }

}
