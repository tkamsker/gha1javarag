package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class ProductHierarchy implements Serializable {
  private String productId;
  private String productDescription;
  private Long productLevel1Id;
  private String productLevel1Description;
  private Long productLevel2Id;
  private String productLevel2Description;
  private Long productLevel3Id;
  private String productLevel3Description;
  private Long productLevel4Id;
  private String productLevel4Description;

  public String getProductId() {
    return productId;
  }

  public void setProductId(String productId) {
    this.productId = productId;
  }

  public String getProductDescription() {
    return productDescription;
  }

  public void setProductDescription(String productDescription) {
    this.productDescription = productDescription;
  }

  public Long getProductLevel1Id() {
    return productLevel1Id;
  }

  public void setProductLevel1Id(Long productLevel1Id) {
    this.productLevel1Id = productLevel1Id;
  }

  public String getProductLevel1Description() {
    return productLevel1Description;
  }

  public void setProductLevel1Description(String productLevel1Description) {
    this.productLevel1Description = productLevel1Description;
  }

  public Long getProductLevel2Id() {
    return productLevel2Id;
  }

  public void setProductLevel2Id(Long productLevel2Id) {
    this.productLevel2Id = productLevel2Id;
  }

  public String getProductLevel2Description() {
    return productLevel2Description;
  }

  public void setProductLevel2Description(String productLevel2Description) {
    this.productLevel2Description = productLevel2Description;
  }

  public Long getProductLevel3Id() {
    return productLevel3Id;
  }

  public void setProductLevel3Id(Long productLevel3Id) {
    this.productLevel3Id = productLevel3Id;
  }

  public String getProductLevel3Description() {
    return productLevel3Description;
  }

  public void setProductLevel3Description(String productLevel3Description) {
    this.productLevel3Description = productLevel3Description;
  }

  public Long getProductLevel4Id() {
    return productLevel4Id;
  }

  public void setProductLevel4Id(Long productLevel4Id) {
    this.productLevel4Id = productLevel4Id;
  }

  public String getProductLevel4Description() {
    return productLevel4Description;
  }

  public void setProductLevel4Description(String productLevel4Description) {
    this.productLevel4Description = productLevel4Description;
  }

}
