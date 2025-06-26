package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.ArrayList;

import at.a1ta.bite.core.shared.util.CommonUtils;
import at.a1ta.cuco.core.shared.dto.IndexationStatus;
import at.a1ta.cuco.core.shared.validator.CommonValidator;

@SuppressWarnings("serial")
public class DefaultProductNode extends BaseNode implements Serializable {
  public enum DefaultProductNodeType {
    BUNDLE, COMPONENT, VOICE
  }

  public enum ProductType {
    FIXED, MOBILE, INET, UNDEFINED, TV
  }

  public enum ProductPromotionStatus {
    AVAILABLE, NOT_AVAILABLE, UNKNOWN
  }

  private String text;
  private DefaultProductNodeType productType;
  private ProductType voiceProductType;
  private CallNumber callNumber;
  private BillableUser billableUser;
  private String productStatus = "";
  private String commitmentStartDate;
  private String productBrand;
  private String productName;
  private String commitmentEndDate;
  private Integer commitmentDuration;
  private String productOfferingTermId;
  private String autovvlDuration;
  private String autovvlStartDate;
  private String autovvlEndDate;
  private String productCharacteristicValuesAsString;
  private String validForStart;
  private String validForEnd;
  private boolean hasOANProduct = false;
  private boolean hasOANProductInHiddenNodes = false;
  private MetaData productCharacteristicValuesAsMetaData;
  private boolean matchingCallNumberWithRootSubscription = false;
  private CallNumber rootCallNumberForBundleProduct;

  private ArrayList<CuCoProdPriceCharge> priceTree = new ArrayList<CuCoProdPriceCharge>();

  private ArrayList<CuCoComponentProductPrice> allPrices = new ArrayList<CuCoComponentProductPrice>();

  private ProductPromotionStatus promotionStatus = ProductPromotionStatus.UNKNOWN;

  public ProductPromotionStatus getPromotionStatus() {
    return promotionStatus;
  }

  public void setPromotionStatus(ProductPromotionStatus promotionStatus) {
    this.promotionStatus = promotionStatus;
  }

  @Override
  public String getText() {
    return text;
  }

  public void setText(String text) {
    this.text = text;
  }

  public DefaultProductNodeType getProductType() {
    return productType;
  }

  public void setProductType(DefaultProductNodeType productType) {
    this.productType = productType;
  }

  public boolean hasVoiceProductType() {
    return voiceProductType != null;
  }

  public ProductType getVoiceProductType() {
    return voiceProductType;
  }

  public void setVoiceProductType(ProductType voiceProductType) {
    this.voiceProductType = voiceProductType;
  }

  public boolean hasCallNumber() {
    return callNumber != null;
  }

  @Override
  public CallNumber getCallNumber() {
    return callNumber;
  }

  @Override
  public void setCallNumber(CallNumber callNumber) {
    this.callNumber = callNumber;
  }

  @Override
  public BillableUser getBillableUser() {
    return billableUser;
  }

  @Override
  public void setBillableUser(BillableUser billableUser) {
    this.billableUser = billableUser;
  }

  // CMSYS703 Start
  public void setCommitmentStartDate(String commitmentStartDate) {
    this.commitmentStartDate = commitmentStartDate;
  }

  public String getCommitmentStartDate() {
    return commitmentStartDate;
  }

  public void setCommitmentEndDate(String commitmentEndDate) {
    this.commitmentEndDate = commitmentEndDate;
  }

  public String getCommitmentEndDate() {
    return commitmentEndDate;
  }

  public void setCommitmentDuration(Integer commitmentDuration) {
    this.commitmentDuration = commitmentDuration;
  }

  public Integer getCommitmentDuration() {
    return commitmentDuration;
  }

  public void setProductOfferingTermId(String productOfferingTermId) {
    this.productOfferingTermId = productOfferingTermId;
  }

  public String getProductOfferingTermId() {
    return productOfferingTermId;
  }

  public void setAutoVVLDuration(String autovvlDuration) {
    this.autovvlDuration = autovvlDuration;
  }

  public String getAutoVVLDuration() {
    return autovvlDuration;
  }

  public void setAutoVVLStartDate(String autovvlStartDate) {
    this.autovvlStartDate = autovvlStartDate;
  }

  public String getAutoVVLStartDate() {
    return autovvlStartDate;
  }

  public void setAutoVVLEndDate(String autovvlEndDate) {
    this.autovvlEndDate = autovvlEndDate;
  }

  public String getAutoVVLEndDate() {
    return autovvlEndDate;
  }

  public void addToPriceTree(CuCoProdPriceCharge cuCoProdPriceCharge) {
    if (this.priceTree == null) {
      this.priceTree = new ArrayList<CuCoProdPriceCharge>();
    }
    this.priceTree.add(cuCoProdPriceCharge);
  }

  public ArrayList<CuCoComponentProductPrice> getAllPrices() {
    return allPrices;
  }

  public void setAllPrices(ArrayList<CuCoComponentProductPrice> allPrices) {
    this.allPrices = allPrices;
  }

  public void addToAllPrices(CuCoComponentProductPrice priceComponent) {
    if (this.allPrices == null) {
      this.allPrices = new ArrayList<CuCoComponentProductPrice>();
    }
    this.allPrices.add(priceComponent);
  }

  public ArrayList<CuCoProdPriceCharge> getPriceTree() {
    return priceTree;
  }

  public void setPriceTree(ArrayList<CuCoProdPriceCharge> priceTree) {
    this.priceTree = priceTree;
  }

  public String getProductBrand() {
    return productBrand;
  }

  public void setProductBrand(String productBrand) {
    this.productBrand = productBrand;
  }

  public String getProductStatus() {
    return productStatus;
  }

  public void setProductStatus(String productStatus) {
    this.productStatus = productStatus;
  }

  public String getProductCharacteristicValuesAsString() {
    return productCharacteristicValuesAsString;
  }

  public void setProductCharacteristicValuesAsString(String productCharacteristicValuesAsString) {
    this.productCharacteristicValuesAsString = productCharacteristicValuesAsString;
  }

  public String getProductName() {
    return productName;
  }

  public void setProductName(String productName) {
    this.productName = productName;
  }

  public MetaData getProductCharacteristicValuesAsMetaData() {
    return productCharacteristicValuesAsMetaData;
  }

  public void setProductCharacteristicValuesAsMetaData(MetaData productCharacteristicValuesAsMetaData) {
    this.productCharacteristicValuesAsMetaData = productCharacteristicValuesAsMetaData;
  }

  public String getValidForStart() {
    return validForStart;
  }

  public void setValidForStart(String validForStart) {
    this.validForStart = validForStart;
  }

  public String getValidForEnd() {
    return validForEnd;
  }

  public void setValidForEnd(String validForEnd) {
    this.validForEnd = validForEnd;
  }

  private String getIndexationText() {
    if (getIdxStatus().equals(IndexationStatus.INDEXED)) {
      return "Mit Indexierung";
    } else if (getIdxStatus().equals(IndexationStatus.NOT_INDEXED)) {
      return "Indexierung ausgenommen";
    } else if (getIdxStatus().equals(IndexationStatus.INDEXED_NOT_STARTED)) {
      return "Mit Indexanpassung";
    }
    return "Ohne Indexierung";
  }

  private String getCallNumberText() {
    String callNum = getCallNumber() != null ? getCallNumber().toString() : "-";
    return callNum.replaceAll("\\s+", "");
  }

  private String getProductBrandText() {
    return getProductBrand() != null ? getProductBrand() : "-";
  }

  private String getProductCharacteristicValuesAsStringText() {
    String removeTags1 = getProductCharacteristicValuesAsString() != null ? (getProductCharacteristicValuesAsString().replace("<pre-wrap style='font-family: Verdana;'>", "")) : "";
    String removeTags2 = removeTags1.replace("</pre-wrap>", "");
    String removeTags3 = removeTags2.replace("<br/>", " ");
    return removeTags3;
  }

  private String getPriceValueAsText() {
    for (CuCoComponentProductPrice obj : getAllPrices()) {
      if (obj.getPrice() != null && obj.getPrice().getAmount() != null) {
        String price = obj.getPrice().getAmount().toString();
        BigDecimal pricePrecisionUptoTwoDecimal = new BigDecimal(price);
        pricePrecisionUptoTwoDecimal = pricePrecisionUptoTwoDecimal.setScale(2, BigDecimal.ROUND_HALF_UP);
        String pricePrecisionUptoTwoDecimalWithEuro = pricePrecisionUptoTwoDecimal + " €";
        return pricePrecisionUptoTwoDecimalWithEuro.replace('.', ',');
      }
    }
    return "-";
  }

  private String getBillableUserText() {
    return getBillableUser() != null ? getBillableUser().getUserName() : "-";
  }

  private ArrayList<BaseNode> getChildrenForSearchFilter() {
    ArrayList<BaseNode> emptyChild = new ArrayList<BaseNode>();
    if (hasChildren()) {
      return getChildren();
    }
    return emptyChild;
  }

  @Override
  public String toString() {
    return CommonUtils.toString(text).toLowerCase() + "~" + (productType != null ? productType.toString().toLowerCase() : "") + "~" + getCallNumberText().toString().toLowerCase() + "~"
        + getBillableUserText().toLowerCase() + "~" + (productStatus != null ? productStatus.toString().toLowerCase() : "") + "~" + getProductBrandText().toLowerCase() + "~"
        + (productStatus != null ? productStatus.toLowerCase() : "") + "~" + getProductCharacteristicValuesAsStringText().toLowerCase() + "~"
        + (promotionStatus != null ? promotionStatus.toString().toLowerCase() : "") + "~" + getIndexationText().toLowerCase() + "~" + getPriceValueAsText() + "~"
        + getChildrenForSearchFilter().toString().toLowerCase() + "~" + getGeoCallNumberText() + "~"
        + (getFormattedBindingStr(getCommitmentStartDate() != null ? getCommitmentStartDate() : "", getCommitmentEndDate() != null ? getCommitmentEndDate() : "")) + "~";
  }

  public boolean hasOANProductInChildNodes() {
    boolean childNodeHasOANProduct = false;
    if (hasChildren()) {
      for (BaseNode child : getChildren()) {
        if (child instanceof DefaultProductNode && ((DefaultProductNode) child).hasOANProductInChildNodes()) {
          childNodeHasOANProduct = true;
        }
      }
    }
    return hasOANProduct || hasOANProductInHiddenNodes || childNodeHasOANProduct;
  }

  public boolean hasOANProductOnCurrentNode() {
    return hasOANProduct;
  }

  public void setHasOANProduct(boolean hasOANProduct) {
    this.hasOANProduct = hasOANProduct;
  }

  public boolean hasOANProductInHiddenNodes() {
    return hasOANProductInHiddenNodes;
  }

  public void setHasOANProductInHiddenNodes(boolean hasOANProductInHiddenNodes) {
    this.hasOANProductInHiddenNodes = hasOANProductInHiddenNodes;
  }

  public boolean isRootProductNode() {
    // should be child of subscription node OR depth is 1 assuming parent level node is subscription node at depth 0
    return getParent() != null ? getParent() instanceof SubscriptionNode : getDepth() == 1;
  }

  public boolean isMatchingCallNumberWithRootSubscription() {
    return matchingCallNumberWithRootSubscription;
  }

  public void setMatchingCallNumberWithRootSubscription(boolean matchingCallNumberWithRootSubscription) {
    this.matchingCallNumberWithRootSubscription = matchingCallNumberWithRootSubscription;
  }

  private String getFormattedBindingStr(String commitmentStartDt, String commitmentEndDt) {
    if (CommonValidator.isBlank(commitmentStartDt) && CommonValidator.isBlank(commitmentEndDt)) {
      return "-";
    }
    if (CommonValidator.isBlank(commitmentStartDt) && !CommonValidator.isBlank(commitmentEndDt)) {
      return "bis " + commitmentEndDt.trim();
    }

    if (!CommonValidator.isBlank(commitmentStartDt) && CommonValidator.isBlank(commitmentEndDt)) {
      return commitmentStartDt.trim() + "  bis ?";
    }

    return commitmentStartDt.trim() + " bis " + commitmentEndDt.trim();
  }

  public CallNumber getRootCallNumberForBundleProduct() {
    return rootCallNumberForBundleProduct;
  }

  public void setRootCallNumberForBundleProduct(CallNumber rootCallNumberForBundleProduct) {
    this.rootCallNumberForBundleProduct = rootCallNumberForBundleProduct;
  }
}
