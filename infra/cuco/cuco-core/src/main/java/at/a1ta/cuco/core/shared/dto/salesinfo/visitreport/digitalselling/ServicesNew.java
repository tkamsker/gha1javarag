package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class ServicesNew extends ServicesBase {
  private boolean a1InitialSetup; // A1 Statklarservice
  private BigDecimal a1InitialSetupPrice;

  private boolean a1GuruService;
  private BigDecimal a1GuruServicePrice;
  private String a1GuruServiceText;

  private boolean mobileBasicEquipment; // Handy-Grundausstattung
  private BigDecimal mobileBasicEquipmentPrice;
  private String mobileBasicEquipmentText;

  private boolean additionalAccessory; // Weiteres Zubehoer
  private BigDecimal additionalAccessoryPrice;
  private String additionalAccessoryText;

  private BigDecimal usedGadgetPrice;

  private String recommendedPromotionalProduct; // Empfohlene Aktionsprodukte aufgrund Nutzung
  private BigDecimal recommendedPromotionalProductPrice;

  public boolean isA1InitialSetup() {
    return a1InitialSetup;
  }

  public void setA1InitialSetup(boolean a1InitialSetup) {
    this.a1InitialSetup = a1InitialSetup;
  }

  public BigDecimal getA1InitialSetupPrice() {
    return a1InitialSetupPrice;
  }

  public void setA1InitialSetupPrice(BigDecimal a1InitialSetupPrice) {
    this.a1InitialSetupPrice = a1InitialSetupPrice;
  }

  public boolean isA1GuruService() {
    return a1GuruService;
  }

  public void setA1GuruService(boolean a1GuruService) {
    this.a1GuruService = a1GuruService;
  }

  public BigDecimal getA1GuruServicePrice() {
    return a1GuruServicePrice;
  }

  public void setA1GuruServicePrice(BigDecimal a1GuruServicePrice) {
    this.a1GuruServicePrice = a1GuruServicePrice;
  }

  public String getA1GuruServiceText() {
    return a1GuruServiceText;
  }

  public void setA1GuruServiceText(String a1GuruServiceText) {
    this.a1GuruServiceText = a1GuruServiceText;
  }

  public boolean isMobileBasicEquipment() {
    return mobileBasicEquipment;
  }

  public void setMobileBasicEquipment(boolean mobileBasicEquipment) {
    this.mobileBasicEquipment = mobileBasicEquipment;
  }

  public BigDecimal getMobileBasicEquipmentPrice() {
    return mobileBasicEquipmentPrice;
  }

  public void setMobileBasicEquipmentPrice(BigDecimal mobileBasicEquipmentPrice) {
    this.mobileBasicEquipmentPrice = mobileBasicEquipmentPrice;
  }

  public String getMobileBasicEquipmentText() {
    return mobileBasicEquipmentText;
  }

  public void setMobileBasicEquipmentText(String mobileBasicEquipmentText) {
    this.mobileBasicEquipmentText = mobileBasicEquipmentText;
  }

  public boolean isAdditionalAccessory() {
    return additionalAccessory;
  }

  public void setAdditionalAccessory(boolean additionalAccessory) {
    this.additionalAccessory = additionalAccessory;
  }

  public BigDecimal getAdditionalAccessoryPrice() {
    return additionalAccessoryPrice;
  }

  public void setAdditionalAccessoryPrice(BigDecimal additionalAccessoryPrice) {
    this.additionalAccessoryPrice = additionalAccessoryPrice;
  }

  public String getAdditionalAccessoryText() {
    return additionalAccessoryText;
  }

  public void setAdditionalAccessoryText(String additionalAccessoryText) {
    this.additionalAccessoryText = additionalAccessoryText;
  }

  public BigDecimal getUsedGadgetPrice() {
    return usedGadgetPrice;
  }

  public void setUsedGadgetPrice(BigDecimal usedGadgetPrice) {
    this.usedGadgetPrice = usedGadgetPrice;
  }

  public String getRecommendedPromotionalProduct() {
    return recommendedPromotionalProduct;
  }

  public void setRecommendedPromotionalProduct(String recommendedPromotionalProduct) {
    this.recommendedPromotionalProduct = recommendedPromotionalProduct;
  }

  public BigDecimal getRecommendedPromotionalProductPrice() {
    return recommendedPromotionalProductPrice;
  }

  public void setRecommendedPromotionalProductPrice(BigDecimal recommendedPromotionalProductPrice) {
    this.recommendedPromotionalProductPrice = recommendedPromotionalProductPrice;
  }

  @Override
  public String toString() {
    return "ServicesNew [a1InitialSetup=" + a1InitialSetup + ", a1InitialSetupPrice=" + a1InitialSetupPrice + ", a1GuruService=" + a1GuruService + ", a1GuruServicePrice=" + a1GuruServicePrice
        + ", a1GuruServiceText=" + a1GuruServiceText + ", mobileBasicEquipment=" + mobileBasicEquipment + ", mobileBasicEquipmentPrice=" + mobileBasicEquipmentPrice + ", mobileBasicEquipmentText="
        + mobileBasicEquipmentText + ", additionalAccessory=" + additionalAccessory + ", additionalAccessoryPrice=" + additionalAccessoryPrice + ", additionalAccessoryText=" + additionalAccessoryText
        + ", usedGadgetPrice=" + usedGadgetPrice + ", recommendedPromotionalProduct=" + recommendedPromotionalProduct + ", recommendedPromotionalProductPrice=" + recommendedPromotionalProductPrice
        + "]";
  }

}
