package at.a1ta.cuco.core.shared.dto.product;

public class ProductHeaderNode extends BaseNode {
  private static final long serialVersionUID = 1L;
  private String nameHeader;
  private String detailsHeader;
  private String idxInfoHeader;
  private String callNumberHeader;
  private String brandHeader;
  private String validFromHeader;
  private String validToHeader;
  private String productStatusHeader;

  public String getNameHeader() {
    return nameHeader;
  }

  public void setNameHeader(String nameHeader) {
    this.nameHeader = nameHeader;
  }

  public String getDetailsHeader() {
    return detailsHeader;
  }

  public void setDetailsHeader(String detailsHeader) {
    this.detailsHeader = detailsHeader;
  }

  public String getIdxInfoHeader() {
    return idxInfoHeader;
  }

  public void setIdxInfoHeader(String idxInfoHeader) {
    this.idxInfoHeader = idxInfoHeader;
  }

  public String getCallNumberHeader() {
    return callNumberHeader;
  }

  public void setCallNumberHeader(String callNumberHeader) {
    this.callNumberHeader = callNumberHeader;
  }

  public String getBrandHeader() {
    return brandHeader;
  }

  public void setBrandHeader(String brandHeader) {
    this.brandHeader = brandHeader;
  }

  public String getValidFromHeader() {
    return validFromHeader;
  }

  public void setValidFromHeader(String validFromHeader) {
    this.validFromHeader = validFromHeader;
  }

  public String getValidToHeader() {
    return validToHeader;
  }

  public void setValidToHeader(String validToHeader) {
    this.validToHeader = validToHeader;
  }

  public String getProductStatusHeader() {
    return productStatusHeader;
  }

  public void setProductStatusHeader(String productStatusHeader) {
    this.productStatusHeader = productStatusHeader;
  }
}
