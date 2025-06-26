package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class ServicesOld extends ServicesBase {
  private String protectDataText;
  private String initialSetupText;
  private String basicEquipment;
  private String protectMobileText;

  public String getProtectDataText() {
    return protectDataText;
  }

  public void setProtectDataText(String protectDataText) {
    this.protectDataText = protectDataText;
  }

  public String getInitialSetupText() {
    return initialSetupText;
  }

  public void setInitialSetupText(String initialSetupText) {
    this.initialSetupText = initialSetupText;
  }

  public String getBasicEquipment() {
    return basicEquipment;
  }

  public void setBasicEquipment(String basicEquipment) {
    this.basicEquipment = basicEquipment;
  }

  public String getProtectMobileText() {
    return protectMobileText;
  }

  public void setProtectMobileText(String protectMobileText) {
    this.protectMobileText = protectMobileText;
  }

  @Override
  public String toString() {
    return "ServicesOld [protectDataText=" + protectDataText + ", initialSetupText=" + initialSetupText + ", basicEquipment=" + basicEquipment + ", protectMobileText=" + protectMobileText + "]";
  }

}
