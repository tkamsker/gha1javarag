package at.a1ta.cuco.core.shared.dto.freeunits;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;

public class FreeUnitsData implements Serializable {
  private ArrayList<FreeUnitsResult> freeUnits;
  private ArrayList<FreeUnitsResult> sumsPerProduct;
  private ArrayList<FreeUnitsResult> sumsPerSidGroup;
  private Date dateOf;
  private Date usageEnd;
  private String phoneNumber;
  private boolean packagesAvailable;

  public FreeUnitsData() {}

  public ArrayList<FreeUnitsResult> getFreeUnits() {
    return freeUnits;
  }

  public void setFreeUnits(final ArrayList<FreeUnitsResult> freeUnits) {
    this.freeUnits = freeUnits;
  }

  public ArrayList<FreeUnitsResult> getSumsPerProduct() {
    return sumsPerProduct;
  }

  public void setSumsPerProduct(ArrayList<FreeUnitsResult> sumsPerProduct) {
    this.sumsPerProduct = sumsPerProduct;
  }

  public ArrayList<FreeUnitsResult> getSumsPerSidGroup() {
    return sumsPerSidGroup;
  }

  public void setSumsPerSidGroup(ArrayList<FreeUnitsResult> sumsPerSidGroup) {
    this.sumsPerSidGroup = sumsPerSidGroup;
  }

  public Date getDateOf() {
    return dateOf;
  }

  public void setDateOf(Date dateOf) {
    this.dateOf = dateOf;
  }

  public Date getUsageEnd() {
    return usageEnd;
  }

  public void setUsageEnd(Date usageEnd) {
    this.usageEnd = usageEnd;
  }

  public String getPhoneNumber() {
    return phoneNumber;
  }

  public void setPhoneNumber(String phoneNumber) {
    this.phoneNumber = phoneNumber;
  }

  public boolean arePackagesAvailable() {
    return packagesAvailable;
  }

  public void setPackagesAvailable(boolean packagesAvailable) {
    this.packagesAvailable = packagesAvailable;
  }

}
