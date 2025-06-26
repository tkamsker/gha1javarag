package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

public class CuCoProductPriceBase implements Serializable {

  private String productPriceId;
  private String productOfferingPriceId;
  private String Name;

  public String getProductPriceId() {
    return productPriceId;
  }

  public void setProductPriceId(String productPriceId) {
    this.productPriceId = productPriceId;
  }

  public String getProductOfferingPriceId() {
    return productOfferingPriceId;
  }

  public void setProductOfferingPriceId(String productOfferingPriceId) {
    this.productOfferingPriceId = productOfferingPriceId;
  }

  public String getName() {
    return Name;
  }

  public void setName(String name) {
    Name = name;
  }

}
