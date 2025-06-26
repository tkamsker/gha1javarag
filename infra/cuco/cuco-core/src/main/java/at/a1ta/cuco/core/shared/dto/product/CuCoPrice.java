package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;
import java.math.BigDecimal;

public class CuCoPrice implements Serializable {

  private String units;
  private BigDecimal amount;

  public String getUnits() {
    return units;
  }

  public void setUnits(String units) {
    this.units = units;
  }

  public BigDecimal getAmount() {
    return amount;
  }

  public void setAmount(BigDecimal bigDecimal) {
    this.amount = bigDecimal;
  }

}
