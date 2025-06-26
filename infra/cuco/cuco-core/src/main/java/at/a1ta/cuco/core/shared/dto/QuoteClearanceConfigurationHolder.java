package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;

public class QuoteClearanceConfigurationHolder implements Serializable {
  /**
   * 
   */
  private static final long serialVersionUID = 1L;
  private ArrayList<ProductOffering> offerings = new ArrayList<ProductOffering>();
  private ArrayList<String> roles = new ArrayList<String>();
  private HashMap<ProductOffering, ArrayList<String>> variablesForOfferingMap = new HashMap<ProductOffering, ArrayList<String>>();

  public ArrayList<ProductOffering> getOfferings() {
    return offerings;
  }

  public void setOfferings(ArrayList<ProductOffering> offerings) {
    this.offerings = offerings;
  }

  public HashMap<ProductOffering, ArrayList<String>> getVariablesForOfferingMap() {
    return variablesForOfferingMap;
  }

  public void setVariablesForOfferingMap(HashMap<ProductOffering, ArrayList<String>> variablesForOfferingMap) {
    this.variablesForOfferingMap = variablesForOfferingMap;
  }

  public ArrayList<String> getVariablesForGivenOffering(ProductOffering offering) {
    return variablesForOfferingMap.get(offering);
  }

  public ArrayList<String> getRoles() {
    return roles;
  }

  public void setRoles(ArrayList<String> roles) {
    this.roles = roles;
  }

}
