package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import at.a1ta.cuco.core.shared.dto.ContactPerson;
import at.a1ta.cuco.core.shared.dto.ProductOffering;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.salesconvnote.ProductHistoryItem;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.generic.FileAttachment;

public class SBSProductNote extends SalesInfoNote {

  private String productId;
  private String productAlternativeId;
  private String productDisplayName;
  private String productCategory;
  private Set<SetupType> setupTypes;
  private SetupCategory category;

  private boolean winback;

  private boolean consultationDesired;
  private QuoteStatus quoteStatus;
  private boolean purchaseWithoutWrittenQuote;

  private Integer turnoverQuantity;
  private Integer turnoverDurationMonths;
  private BigDecimal turnoverOnetimeCost;
  private BigDecimal turnoverMonthlyCost;
  private BigDecimal turnoverYearlyCost;
  private BigDecimal turnoverSum; // Anzahl * (montl. *laufzeit + einmalig+ jährliche Kosten / 12 * laufzeit)

  private HandlingAssigneeType handlingAssigneeType;
  private String handlingAssigneeOrgUnitId;
  private String handlingAssigneeOrgUnitName;
  private String handlingAssigneeOrgUnitStreet;
  private String handlingAssigneeOrgUnitPostalCode;
  private String handlingAssigneeOrgUnitCity;

  private List<ProductHistoryItem> historyItems = new ArrayList<ProductHistoryItem>();
  private Long productOfferingId;
  private List<FileAttachment> fileAttachments;
  private ContactPerson contactPerson;
  private Long todoGroupNoteId;

  public SBSProductNote() {
    super();
  }

  /**
   * Copy Constructor
   * 
   * @param sBSProductNote a <code>SBSProductNote</code> object
   */
  public SBSProductNote(SBSProductNote sBSProductNote) {
    super(sBSProductNote);
    this.productId = sBSProductNote.productId;
    this.productAlternativeId = sBSProductNote.productAlternativeId;
    this.productDisplayName = sBSProductNote.productDisplayName;
    this.productCategory = sBSProductNote.productCategory;
    this.setupTypes = sBSProductNote.setupTypes;
    this.category = sBSProductNote.category;
    this.winback = sBSProductNote.winback;
    this.consultationDesired = sBSProductNote.consultationDesired;
    this.quoteStatus = sBSProductNote.quoteStatus;
    this.purchaseWithoutWrittenQuote = sBSProductNote.purchaseWithoutWrittenQuote;
    this.turnoverQuantity = sBSProductNote.turnoverQuantity;
    this.turnoverDurationMonths = sBSProductNote.turnoverDurationMonths;
    this.turnoverOnetimeCost = sBSProductNote.turnoverOnetimeCost;
    this.turnoverMonthlyCost = sBSProductNote.turnoverMonthlyCost;
    this.turnoverYearlyCost = sBSProductNote.turnoverYearlyCost;
    this.turnoverSum = sBSProductNote.turnoverSum;
    this.handlingAssigneeType = sBSProductNote.handlingAssigneeType;
    this.handlingAssigneeOrgUnitId = sBSProductNote.handlingAssigneeOrgUnitId;
    this.handlingAssigneeOrgUnitName = sBSProductNote.handlingAssigneeOrgUnitName;
    this.handlingAssigneeOrgUnitStreet = sBSProductNote.handlingAssigneeOrgUnitStreet;
    this.handlingAssigneeOrgUnitPostalCode = sBSProductNote.handlingAssigneeOrgUnitPostalCode;
    this.handlingAssigneeOrgUnitCity = sBSProductNote.handlingAssigneeOrgUnitCity;
    this.historyItems = sBSProductNote.historyItems;
    this.productOfferingId = sBSProductNote.productOfferingId;
  }

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

  public Set<SetupType> getSetupTypes() {
    return setupTypes;
  }

  public void setSetupTypes(Set<SetupType> setupTypes) {
    this.setupTypes = setupTypes;
  }

  public SetupCategory getCategory() {
    return category;
  }

  public void setCategory(SetupCategory category) {
    this.category = category;
  }

  public boolean isWinback() {
    return winback;
  }

  public void setWinback(boolean winback) {
    this.winback = winback;
  }

  public boolean isConsultationDesired() {
    return consultationDesired;
  }

  public void setConsultationDesired(boolean consultationDesired) {
    this.consultationDesired = consultationDesired;
  }

  public QuoteStatus getQuoteStatus() {
    return quoteStatus;
  }

  public void setQuoteStatus(QuoteStatus quoteStatus) {
    this.quoteStatus = quoteStatus;
  }

  public boolean isPurchaseWithoutWrittenQuote() {
    return purchaseWithoutWrittenQuote;
  }

  public void setPurchaseWithoutWrittenQuote(boolean purchaseWithoutWrittenQuote) {
    this.purchaseWithoutWrittenQuote = purchaseWithoutWrittenQuote;
  }

  public Integer getTurnoverQuantity() {
    return turnoverQuantity;
  }

  public void setTurnoverQuantity(Integer turnoverQuantity) {
    this.turnoverQuantity = turnoverQuantity;
  }

  public Integer getTurnoverDurationMonths() {
    return turnoverDurationMonths;
  }

  public void setTurnoverDurationMonths(Integer turnoverDurationMonths) {
    this.turnoverDurationMonths = turnoverDurationMonths;
  }

  public BigDecimal getTurnoverOnetimeCost() {
    return turnoverOnetimeCost;
  }

  public void setTurnoverOnetimeCost(BigDecimal turnoverOnetimeCost) {
    this.turnoverOnetimeCost = turnoverOnetimeCost;
  }

  public BigDecimal getTurnoverMonthlyCost() {
    return turnoverMonthlyCost;
  }

  public void setTurnoverMonthlyCost(BigDecimal turnoverMonthlyCost) {
    this.turnoverMonthlyCost = turnoverMonthlyCost;
  }

  public BigDecimal getTurnoverYearlyCost() {
    return turnoverYearlyCost;
  }

  public void setTurnoverYearlyCost(BigDecimal turnoverYearlyCost) {
    this.turnoverYearlyCost = turnoverYearlyCost;
  }

  public BigDecimal getTurnoverSum() {
    return turnoverSum;
  }

  public void setTurnoverSum(BigDecimal turnoverSum) {
    this.turnoverSum = turnoverSum;
  }

  public HandlingAssigneeType getHandlingAssigneeType() {
    return handlingAssigneeType;
  }

  public void setHandlingAssigneeType(HandlingAssigneeType handlingAssigneeType) {
    this.handlingAssigneeType = handlingAssigneeType;
  }

  public String getHandlingAssigneeOrgUnitId() {
    return handlingAssigneeOrgUnitId;
  }

  public void setHandlingAssigneeOrgUnitId(String handlingAssigneeOrgUnitId) {
    this.handlingAssigneeOrgUnitId = handlingAssigneeOrgUnitId;
  }

  public String getHandlingAssigneeOrgUnitName() {
    return handlingAssigneeOrgUnitName;
  }

  public void setHandlingAssigneeOrgUnitName(String handlingAssigneeOrgUnitName) {
    this.handlingAssigneeOrgUnitName = handlingAssigneeOrgUnitName;
  }

  public String getHandlingAssigneeOrgUnitStreet() {
    return handlingAssigneeOrgUnitStreet;
  }

  public void setHandlingAssigneeOrgUnitStreet(String handlingAssigneeOrgUnitStreet) {
    this.handlingAssigneeOrgUnitStreet = handlingAssigneeOrgUnitStreet;
  }

  public String getHandlingAssigneeOrgUnitPostalCode() {
    return handlingAssigneeOrgUnitPostalCode;
  }

  public void setHandlingAssigneeOrgUnitPostalCode(String handlingAssigneeOrgUnitPostalCode) {
    this.handlingAssigneeOrgUnitPostalCode = handlingAssigneeOrgUnitPostalCode;
  }

  public String getHandlingAssigneeOrgUnitCity() {
    return handlingAssigneeOrgUnitCity;
  }

  public void setHandlingAssigneeOrgUnitCity(String handlingAssigneeOrgUnitCity) {
    this.handlingAssigneeOrgUnitCity = handlingAssigneeOrgUnitCity;
  }

  @Override
  public String toString() {
    return "SBSProductNote [productId=" + productId + ", productAlternativeId=" + productAlternativeId + ", productDisplayName=" + productDisplayName + ", productCategory=" + productCategory
        + ", setupTypes=" + setupTypes + ", category=" + category + ", winback=" + winback + ", consultationDesired=" + consultationDesired + ", quoteStatus=" + quoteStatus
        + ", purchaseWithoutWrittenQuote=" + purchaseWithoutWrittenQuote + ", turnoverQuantity=" + turnoverQuantity + ", turnoverDurationMonths=" + turnoverDurationMonths + ", turnoverOnetimeCost="
        + turnoverOnetimeCost + ", turnoverMonthlyCost=" + turnoverMonthlyCost + ", turnoverYearlyCost=" + turnoverYearlyCost + ", turnoverSum=" + turnoverSum + ", handlingAssigneeType="
        + handlingAssigneeType + ", handlingAssigneeOrgUnitId=" + handlingAssigneeOrgUnitId + ", handlingAssigneeOrgUnitName=" + handlingAssigneeOrgUnitName + ", handlingAssigneeOrgUnitStreet="
        + handlingAssigneeOrgUnitStreet + ", handlingAssigneeOrgUnitPostalCode=" + handlingAssigneeOrgUnitPostalCode + ", handlingAssigneeOrgUnitCity=" + handlingAssigneeOrgUnitCity + "]";
  }

  public List<ProductHistoryItem> getHistoryItems() {
    return historyItems;
  }

  public void setHistoryItems(List<ProductHistoryItem> historyItems) {
    this.historyItems = historyItems;
  }

  public ProductOffering getProductOffering() {
    if (productOfferingId == null) {
      return null;
    }
    ProductOffering.valueOf(productOfferingId);
    return ProductOffering.valueOf(productOfferingId);
  }

  public void setProductOffering(ProductOffering productOffering) {
    if (productOffering != null) {
      this.productOfferingId = productOffering.getId();
    } else {
      this.productOfferingId = null;
    }
  }

  public Long getProductOfferingId() {
    return productOfferingId;
  }

  public void setProductOfferingId(Long productOfferingId) {
    this.productOfferingId = productOfferingId;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = super.hashCode();
    result = prime * result + ((category == null) ? 0 : category.hashCode());
    result = prime * result + (consultationDesired ? 1231 : 1237);
    result = prime * result + ((handlingAssigneeOrgUnitCity == null) ? 0 : handlingAssigneeOrgUnitCity.hashCode());
    result = prime * result + ((handlingAssigneeOrgUnitId == null) ? 0 : handlingAssigneeOrgUnitId.hashCode());
    result = prime * result + ((handlingAssigneeOrgUnitName == null) ? 0 : handlingAssigneeOrgUnitName.hashCode());
    result = prime * result + ((handlingAssigneeOrgUnitPostalCode == null) ? 0 : handlingAssigneeOrgUnitPostalCode.hashCode());
    result = prime * result + ((handlingAssigneeOrgUnitStreet == null) ? 0 : handlingAssigneeOrgUnitStreet.hashCode());
    result = prime * result + ((handlingAssigneeType == null) ? 0 : handlingAssigneeType.hashCode());
    result = prime * result + ((historyItems == null) ? 0 : historyItems.hashCode());
    result = prime * result + ((productAlternativeId == null) ? 0 : productAlternativeId.hashCode());
    result = prime * result + ((productCategory == null) ? 0 : productCategory.hashCode());
    result = prime * result + ((productDisplayName == null) ? 0 : productDisplayName.hashCode());
    result = prime * result + ((productId == null) ? 0 : productId.hashCode());
    result = prime * result + ((productOfferingId == null) ? 0 : productOfferingId.hashCode());
    result = prime * result + (purchaseWithoutWrittenQuote ? 1231 : 1237);
    result = prime * result + ((quoteStatus == null) ? 0 : quoteStatus.hashCode());
    result = prime * result + ((setupTypes == null) ? 0 : setupTypes.hashCode());
    result = prime * result + ((turnoverDurationMonths == null) ? 0 : turnoverDurationMonths.hashCode());
    result = prime * result + ((turnoverMonthlyCost == null) ? 0 : turnoverMonthlyCost.hashCode());
    result = prime * result + ((turnoverOnetimeCost == null) ? 0 : turnoverOnetimeCost.hashCode());
    result = prime * result + ((turnoverQuantity == null) ? 0 : turnoverQuantity.hashCode());
    result = prime * result + ((turnoverSum == null) ? 0 : turnoverSum.hashCode());
    result = prime * result + ((turnoverYearlyCost == null) ? 0 : turnoverYearlyCost.hashCode());
    result = prime * result + (winback ? 1231 : 1237);
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) {
      return true;
    }
    if (!super.equals(obj)) {
      return false;
    }
    if (getClass() != obj.getClass()) {
      return false;
    }
    SBSProductNote other = (SBSProductNote) obj;
    if (category != other.category) {
      return false;
    }
    if (consultationDesired != other.consultationDesired) {
      return false;
    }
    if (handlingAssigneeOrgUnitCity == null) {
      if (other.handlingAssigneeOrgUnitCity != null) {
        return false;
      }
    } else if (!handlingAssigneeOrgUnitCity.equals(other.handlingAssigneeOrgUnitCity)) {
      return false;
    }
    if (handlingAssigneeOrgUnitId == null) {
      if (other.handlingAssigneeOrgUnitId != null) {
        return false;
      }
    } else if (!handlingAssigneeOrgUnitId.equals(other.handlingAssigneeOrgUnitId)) {
      return false;
    }
    if (handlingAssigneeOrgUnitName == null) {
      if (other.handlingAssigneeOrgUnitName != null) {
        return false;
      }
    } else if (!handlingAssigneeOrgUnitName.equals(other.handlingAssigneeOrgUnitName)) {
      return false;
    }
    if (handlingAssigneeOrgUnitPostalCode == null) {
      if (other.handlingAssigneeOrgUnitPostalCode != null) {
        return false;
      }
    } else if (!handlingAssigneeOrgUnitPostalCode.equals(other.handlingAssigneeOrgUnitPostalCode)) {
      return false;
    }
    if (handlingAssigneeOrgUnitStreet == null) {
      if (other.handlingAssigneeOrgUnitStreet != null) {
        return false;
      }
    } else if (!handlingAssigneeOrgUnitStreet.equals(other.handlingAssigneeOrgUnitStreet)) {
      return false;
    }
    if (handlingAssigneeType != other.handlingAssigneeType) {
      return false;
    }
    if (historyItems == null) {
      if (other.historyItems != null) {
        return false;
      }
    } else if (!historyItems.equals(other.historyItems)) {
      return false;
    }
    if (productAlternativeId == null) {
      if (other.productAlternativeId != null) {
        return false;
      }
    } else if (!productAlternativeId.equals(other.productAlternativeId)) {
      return false;
    }
    if (productCategory == null) {
      if (other.productCategory != null) {
        return false;
      }
    } else if (!productCategory.equals(other.productCategory)) {
      return false;
    }
    if (productDisplayName == null) {
      if (other.productDisplayName != null) {
        return false;
      }
    } else if (!productDisplayName.equals(other.productDisplayName)) {
      return false;
    }
    if (productId == null) {
      if (other.productId != null) {
        return false;
      }
    } else if (!productId.equals(other.productId)) {
      return false;
    }
    if (productOfferingId == null) {
      if (other.productOfferingId != null) {
        return false;
      }
    } else if (!productOfferingId.equals(other.productOfferingId)) {
      return false;
    }
    if (purchaseWithoutWrittenQuote != other.purchaseWithoutWrittenQuote) {
      return false;
    }
    if (quoteStatus != other.quoteStatus) {
      return false;
    }
    if (setupTypes == null) {
      if (other.setupTypes != null) {
        return false;
      }
    } else if (!setupTypes.equals(other.setupTypes)) {
      return false;
    }
    if (turnoverDurationMonths == null) {
      if (other.turnoverDurationMonths != null) {
        return false;
      }
    } else if (!turnoverDurationMonths.equals(other.turnoverDurationMonths)) {
      return false;
    }
    if (turnoverMonthlyCost == null) {
      if (other.turnoverMonthlyCost != null) {
        return false;
      }
    } else if (!turnoverMonthlyCost.equals(other.turnoverMonthlyCost)) {
      return false;
    }
    if (turnoverOnetimeCost == null) {
      if (other.turnoverOnetimeCost != null) {
        return false;
      }
    } else if (!turnoverOnetimeCost.equals(other.turnoverOnetimeCost)) {
      return false;
    }
    if (turnoverQuantity == null) {
      if (other.turnoverQuantity != null) {
        return false;
      }
    } else if (!turnoverQuantity.equals(other.turnoverQuantity)) {
      return false;
    }
    if (turnoverSum == null) {
      if (other.turnoverSum != null) {
        return false;
      }
    } else if (!turnoverSum.equals(other.turnoverSum)) {
      return false;
    }
    if (turnoverYearlyCost == null) {
      if (other.turnoverYearlyCost != null) {
        return false;
      }
    } else if (!turnoverYearlyCost.equals(other.turnoverYearlyCost)) {
      return false;
    }
    if (winback != other.winback) {
      return false;
    }
    return true;
  }

  public List<FileAttachment> getFileAttachments() {
    return fileAttachments;
  }

  public void setFileAttachments(List<FileAttachment> fileAttachments) {
    this.fileAttachments = fileAttachments;
  }

  public ContactPerson getContactPerson() {
    return contactPerson;
  }

  public void setContactPerson(ContactPerson contactPerson) {
    this.contactPerson = contactPerson;
  }

  public Long getTodoGroupNoteId() {
    return todoGroupNoteId;
  }

  public void setTodoGroupNoteId(Long todoGroupNoteId) {
    this.todoGroupNoteId = todoGroupNoteId;
  }

}
