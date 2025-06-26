package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class SecurityOld extends SecurityBase {
  private boolean cyberDefence;
  private BigDecimal cyberDefencePrice;
  private String cyberDefenceText;

  private boolean creditCard;
  private BigDecimal creditCardPrice;

  public boolean isCyberDefence() {
    return cyberDefence;
  }

  public void setCyberDefence(boolean cyberDefence) {
    this.cyberDefence = cyberDefence;
  }

  public BigDecimal getCyberDefencePrice() {
    return cyberDefencePrice;
  }

  public void setCyberDefencePrice(BigDecimal cyberDefencePrice) {
    this.cyberDefencePrice = cyberDefencePrice;
  }

  public String getCyberDefenceText() {
    return cyberDefenceText;
  }

  public void setCyberDefenceText(String cyberDefenceText) {
    this.cyberDefenceText = cyberDefenceText;
  }

  public boolean isCreditCard() {
    return creditCard;
  }

  public void setCreditCard(boolean creditCard) {
    this.creditCard = creditCard;
  }

  public BigDecimal getCreditCardPrice() {
    return creditCardPrice;
  }

  public void setCreditCardPrice(BigDecimal creditCardPrice) {
    this.creditCardPrice = creditCardPrice;
  }

  @Override
  public String toString() {
    return "SecurityOld [cyberDefence=" + cyberDefence + ", cyberDefencePrice=" + cyberDefencePrice + ", cyberDefenceText=" + cyberDefenceText + ", creditCard=" + creditCard + ", creditCardPrice="
        + creditCardPrice + "]";
  }

}
