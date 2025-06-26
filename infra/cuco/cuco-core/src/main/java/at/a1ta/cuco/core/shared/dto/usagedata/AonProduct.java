package at.a1ta.cuco.core.shared.dto.usagedata;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;

public class AonProduct implements Serializable {

  private String aonNumber;
  private ArrayList<String> productNames = new ArrayList<String>();
  private String phoneNumber;
  private PhoneNumberStructure phoneNumberStructure;

  public String getAonNumber() {
    return aonNumber;
  }

  public void setAonNumber(String aonNumber) {
    this.aonNumber = aonNumber;
  }

  public List<String> getProductNames() {
    return productNames;
  }

  public void setProductNames(ArrayList<String> productNames) {
    this.productNames = productNames;
  }

  public String getPhoneNumber() {
    return phoneNumber;
  }

  public void setPhoneNumber(String phoneNumber) {
    this.phoneNumber = phoneNumber;
  }

  public PhoneNumberStructure getPhoneNumberStructure() {
    return phoneNumberStructure;
  }

  public void setPhoneNumberStructure(PhoneNumberStructure phoneNumberStructure) {
    this.phoneNumberStructure = phoneNumberStructure;
  }

}