package at.a1ta.cuco.core.shared.dto.product;

import java.util.ArrayList;

import at.a1ta.bite.core.shared.util.CommonUtils;
import at.a1ta.cuco.core.shared.dto.IndexationStatus;

@SuppressWarnings("serial")
public class DefaultSubscriptionNode extends SubscriptionNode {

  public DefaultSubscriptionNode(String accountNumber, String subscriptionId, DefaultSubscriptionType type, CallNumber callNumber, LastMileId lastMileId, BillableUser billableUser) {
    super(accountNumber, subscriptionId);
    this.type = type;
    this.callNumber = callNumber;
    this.lastMileId = lastMileId;
    this.billableUser = billableUser;
  }

  public DefaultSubscriptionNode() {
    super();
  }

  private DefaultSubscriptionType type;
  private String typeText;
  private CallNumber callNumber;
  private BillableUser billableUser;
  private LastMileId lastMileId;
  private String address1;
  private String address2;
  private String address3;
  private CallNumber rootCallNumberForBundleProduct;
  private Integer childrenWithMatchingCallNumbersArraySize;

  public DefaultSubscriptionType getType() {
    return type;
  }

  public void setType(DefaultSubscriptionType type) {
    this.type = type;
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

  public LastMileId getLastMileId() {
    return lastMileId;
  }

  public void setLastMileId(LastMileId lastMileId) {
    this.lastMileId = lastMileId;
  }

  @Override
  public String getText() {
    String text = "";
    if (lastMileId != null) {
      text = lastMileId.toString();
    } else if (callNumber != null) {
      text = callNumber.toString();
    } else if (billableUser != null) {
      text = billableUser.getUserName();
    } else if (getTopLevelProducts() != null) {
      text = getTopLevelProducts();
    }
    return text;
  }

  public String getAddress1() {
    return address1;
  }

  public void setAddress1(String address1) {
    this.address1 = address1;
  }

  public String getAddress2() {
    return address2;
  }

  public void setAddress2(String address2) {
    this.address2 = address2;
  }

  public String getAddress3() {
    return address3;
  }

  public void setAddress3(String address3) {
    this.address3 = address3;
  }

  private String getCallNumberText() {
    String callNum = getCallNumber() != null ? getCallNumber().toString() : "-";
    return callNum.replaceAll("\\s+", "");
  }

  private String getAddress1text() {
    return getAddress1() != null ? getAddress1() : "-";
  }

  private String getAddress2Text() {
    return getAddress2() != null ? getAddress2() : "-";
  }

  private String getAddress3Text() {
    return getAddress3() != null ? getAddress3() : "-";
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
    return CommonUtils.toString(type).toString() + "~" + CommonUtils.toString(getCallNumberText()).toLowerCase() + "~" + CommonUtils.toString(getBillableUserText()).toLowerCase() + "~"
        + CommonUtils.toString(getAddress1text()).toLowerCase() + "~" + CommonUtils.toString(getAddress2Text()).toLowerCase() + "~" + CommonUtils.toString(getAddress3Text()).toLowerCase() + "~"
        + CommonUtils.toString(getAccountNumber()).toLowerCase() + "~" + CommonUtils.toString(getSubscriptionId()).toLowerCase() + "~" + CommonUtils.toString(getVertragNoForDisplay()).toLowerCase()
        + "~" + CommonUtils.toString(getIndexationText()).toLowerCase() + "~" + CommonUtils.toString(getChildrenForSearchFilter()).toString().toLowerCase() + "~"
        + CommonUtils.toString(getGeoCallNumberText()) + "~" + (getTypeText() != null ? getTypeText().toLowerCase() : "") + "~"
        + (getTopLevelProducts() != null ? getTopLevelProducts().toLowerCase() : "") + "~";
  }

  public String getTypeText() {
    return typeText;
  }

  public void setTypeText(String typeText) {
    this.typeText = typeText;
  }

  public CallNumber getRootCallNumberForBundleProduct() {
    return rootCallNumberForBundleProduct;
  }

  public void setRootCallNumberForBundleProduct(CallNumber callNumber) {
    this.rootCallNumberForBundleProduct = callNumber;
  }

  public Integer getChildrenWithMatchingCallNumbersArraySize() {
    return childrenWithMatchingCallNumbersArraySize;
  }

  public void setChildrenWithMatchingCallNumbersArraySize(Integer childrenWithMatchingCallNumbersArraySize) {
    this.childrenWithMatchingCallNumbersArraySize = childrenWithMatchingCallNumbersArraySize;
  }
}
