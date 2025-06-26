package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs;

import java.io.Serializable;
import java.util.List;

public class SBSProductNoteConfig implements Serializable {
  private List<SBSProduct> products;
  private List<SBSOrgUnit> orgUnits;

  public List<SBSProduct> getProducts() {
    return products;
  }

  public void setProducts(List<SBSProduct> products) {
    this.products = products;
  }

  public List<SBSOrgUnit> getOrgUnits() {
    return orgUnits;
  }

  public void setOrgUnits(List<SBSOrgUnit> orgUnits) {
    this.orgUnits = orgUnits;
  }

}
