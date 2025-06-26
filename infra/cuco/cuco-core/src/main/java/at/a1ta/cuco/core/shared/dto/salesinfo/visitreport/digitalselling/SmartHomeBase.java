package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;
import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class SmartHomeBase implements Serializable {
  private static final long serialVersionUID = 1L;

  private boolean comfortSolution;
  private BigDecimal comfortSolutionPrice;
  private String comfortSolutionText;

  private boolean smartProduct;
  private BigDecimal smartProductPrice;

  private boolean amazonAlexa;

  private String comment;
  private BigDecimal sum;

  public boolean isComfortSolution() {
    return comfortSolution;
  }

  public void setComfortSolution(boolean comfortSolution) {
    this.comfortSolution = comfortSolution;
  }

  public BigDecimal getComfortSolutionPrice() {
    return comfortSolutionPrice;
  }

  public void setComfortSolutionPrice(BigDecimal comfortSolutionPrice) {
    this.comfortSolutionPrice = comfortSolutionPrice;
  }

  public String getComfortSolutionText() {
    return comfortSolutionText;
  }

  public void setComfortSolutionText(String comfortSolutionText) {
    this.comfortSolutionText = comfortSolutionText;
  }

  public boolean isSmartProduct() {
    return smartProduct;
  }

  public void setSmartProduct(boolean smartProduct) {
    this.smartProduct = smartProduct;
  }

  public BigDecimal getSmartProductPrice() {
    return smartProductPrice;
  }

  public void setSmartProductPrice(BigDecimal smartProductPrice) {
    this.smartProductPrice = smartProductPrice;
  }

  public boolean isAmazonAlexa() {
    return amazonAlexa;
  }

  public void setAmazonAlexa(boolean amazonAlexa) {
    this.amazonAlexa = amazonAlexa;
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
    return "SmartHomeBase [comfortSolution=" + comfortSolution + ", comfortSolutionPrice=" + comfortSolutionPrice + ", comfortSolutionText=" + comfortSolutionText + ", smartProduct=" + smartProduct
        + ", smartProductPrice=" + smartProductPrice + ", amazonAlexa=" + amazonAlexa + ", comment=" + comment + ", sum=" + sum + "]";
  }

}
