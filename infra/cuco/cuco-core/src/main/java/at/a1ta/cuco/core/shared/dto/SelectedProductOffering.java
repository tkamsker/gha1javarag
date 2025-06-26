package at.a1ta.cuco.core.shared.dto;

public class SelectedProductOffering {
  private ProductOffering productOffering;
  private boolean selected;

  public ProductOffering getProductOffering() {
    return productOffering;
  }

  public void setProductOffering(ProductOffering productOffering) {
    this.productOffering = productOffering;
  }

  public boolean isSelected() {
    return selected;
  }

  public void setSelected(boolean selected) {
    this.selected = selected;
  }

}
