package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs;

import java.io.Serializable;
import java.util.List;

public class SBSProduct implements Serializable {
  private String productId;
  private String productAlternativeId;
  private String productDisplayName;
  private String productCategory;
  private String defaultConfig;
  private String siNoteClass;
  private boolean active;
  private long sequence;
  private List<String> setupTypes;
  private List<String> setupCategories;
  private List<String> quoteStatus;
  private List<String> assigneeTypes;

  public String getProductId() {
    return productId;
  }

  public void setProductId(String productId) {
    this.productId = productId;
  }

  public String getProductAlternativeId() {
    return productAlternativeId;
  }

  public void setProductAlternativeId(String productAlternativeId) {
    this.productAlternativeId = productAlternativeId;
  }

  public String getProductDisplayName() {
    return productDisplayName;
  }

  public void setProductDisplayName(String productDisplayName) {
    this.productDisplayName = productDisplayName;
  }

  public String getProductCategory() {
    return productCategory;
  }

  public void setProductCategory(String productCategory) {
    this.productCategory = productCategory;
  }

  public boolean isActive() {
    return active;
  }

  public void setActive(boolean active) {
    this.active = active;
  }

  public long getSequence() {
    return sequence;
  }

  public void setSequence(long sequence) {
    this.sequence = sequence;
  }

  public List<String> getSetupTypes() {
    return setupTypes;
  }

  public void setSetupTypes(List<String> setupTypes) {
    this.setupTypes = setupTypes;
  }

  public List<String> getSetupCategories() {
    return setupCategories;
  }

  public void setSetupCategories(List<String> setupCategories) {
    this.setupCategories = setupCategories;
  }

  public List<String> getQuoteStatus() {
    return quoteStatus;
  }

  public void setQuoteStatus(List<String> quoteStatus) {
    this.quoteStatus = quoteStatus;
  }

  public List<String> getAssigneeTypes() {
    return assigneeTypes;
  }

  public void setAssigneeTypes(List<String> assigneeTypes) {
    this.assigneeTypes = assigneeTypes;
  }

  public String getDefaultConfig() {
    return defaultConfig;
  }

  public void setDefaultConfig(String defaultConfig) {
    this.defaultConfig = defaultConfig;
  }

  public String getSiNoteClass() {
    return siNoteClass;
  }

  public void setSiNoteClass(String siNoteClass) {
    this.siNoteClass = siNoteClass;
  }

}
