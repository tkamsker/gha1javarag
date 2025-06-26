package at.a1ta.cuco.core.shared.dto.product;

import java.util.ArrayList;

import at.a1ta.cuco.core.shared.dto.IndexationStatus;

public class BaseNode implements Node {
  private String id;
  private String contractSegment;
  private BaseNode parent;
  private int depth;
  private int effectiveDepthForView;
  private ArrayList<BaseNode> children = new ArrayList<BaseNode>();
  private boolean childDetailsLoaded;
  private boolean expanded;
  private boolean hasIndirectParent;
  private boolean feasibilityCheckAvailable;
  private boolean displayA1CoachLink;
  private String linkedSubscriptionId;

  public boolean isDisplayA1CoachLink() {
    return displayA1CoachLink;
  }

  public void setDisplayA1CoachLink(boolean displayA1CoachLink) {
    this.displayA1CoachLink = displayA1CoachLink;
  }

  public boolean isFeasibilityCheckAvailable() {
    return feasibilityCheckAvailable;
  }

  public void setFeasibilityCheckAvailable(boolean feasibilityCheckAvailable) {
    this.feasibilityCheckAvailable = feasibilityCheckAvailable;
  }

  private MetaData metaData;
  private CallNumber callNumber;
  private BillableUser billableUser;
  private GeoCallNumber geoCallNumber;
  private IndexationStatus idxStatus = IndexationStatus.NOT_AVAILABLE;
  private DISPLAY intendedUIDisplay;
  private long partyId;

  public long getPartyId() {
    return partyId;
  }

  public void setPartyId(long partyId) {
    this.partyId = partyId;
  }

  public enum DISPLAY {
    BROWSER, TABLE
  }

  public DISPLAY getIntendedUIDisplay() {
    return intendedUIDisplay;
  }

  public void setIntendedUIDisplay(DISPLAY intendedUIDisplay) {
    this.intendedUIDisplay = intendedUIDisplay;
  }

  @Override
  public String getText() {
    return "";
  }

  @Override
  public String getId() {
    return id;
  }

  @Override
  public void setId(String id) {
    this.id = id;
  }

  @Override
  public BaseNode getParent() {
    return parent;
  }

  @Override
  public void setParent(BaseNode parent) {
    this.parent = parent;
  }

  @Override
  public ArrayList<BaseNode> getChildren() {
    return children;
  }

  @Override
  public void setChildren(ArrayList<BaseNode> children) {
    this.children = children;
  }

  @Override
  public void addChild(BaseNode child) {
    if (children == null) {
      children = new ArrayList<BaseNode>();
    }
    children.add(child);
  }

  @Override
  public boolean hasParent() {
    return parent != null;
  }

  @Override
  public boolean hasChildren() {
    return children != null && !children.isEmpty();
  }

  @Override
  public MetaData getMetaData() {
    return metaData;
  }

  @Override
  public void setMetaData(MetaData metaData) {
    this.metaData = metaData;
  }

  protected String ellipsis(String input, int maxLen) {
    if (input == null) {
      return null;
    }
    if ((input.length() < maxLen) || (maxLen < 3)) {
      return input;
    }
    return input.substring(0, maxLen - 3) + "...";
  }

  public IndexationStatus getIdxStatus() {
    return idxStatus;
  }

  public void setIdxStatus(IndexationStatus idxStatus) {
    this.idxStatus = idxStatus;
  }

  public String getContractSegment() {
    return contractSegment;
  }

  public void setContractSegment(String contractSegment) {
    this.contractSegment = contractSegment;
  }

  public CallNumber getCallNumber() {
    return callNumber;
  }

  public void setCallNumber(CallNumber callNumber) {
    this.callNumber = callNumber;
  }

  public BillableUser getBillableUser() {
    return billableUser;
  }

  public void setBillableUser(BillableUser billableUser) {
    this.billableUser = billableUser;
  }

  public GeoCallNumber getGeoCallNumber() {
    return geoCallNumber;
  }

  public void setGeoCallNumber(GeoCallNumber geoCallNumber) {
    this.geoCallNumber = geoCallNumber;
  }

  public int getDepth() {
    return depth;
  }

  public void setDepth(int depth) {
    this.depth = depth;
  }

  public boolean isExpanded() {
    return expanded;
  }

  public void setExpanded(boolean expanded) {
    this.expanded = expanded;
  }

  public boolean isChildDetailsLoaded() {
    return childDetailsLoaded;
  }

  public void setChildDetailsLoaded(boolean childDetailsLoaded) {
    this.childDetailsLoaded = childDetailsLoaded;
  }

  public String getSubscriptionCallNumber() {
    return getCallNumber() != null ? (getCallNumber().getCountryCode() + getCallNumber().getOnkz() + getCallNumber().getTnum()) : "";
  }

  public String getGeoCallNumberText() {
    return (getGeoCallNumber() != null ? getGeoCallNumber().toString() : "").replaceAll("\\s+", "");
  }

  public String getLinkedSubscriptionId() {
    return linkedSubscriptionId;
  }

  public void setLinkedSubscriptionId(String linkedSubscriptionId) {
    this.linkedSubscriptionId = linkedSubscriptionId;
  }

  public int getEffectiveDepthForView() {
    return getParent() != null ? getParent().getEffectiveDepthForView() + 1 : (effectiveDepthForView == 0 ? getDepth() : effectiveDepthForView);
  }

  public void setEffectiveDepthForView(int effectiveDepthForView) {
    this.effectiveDepthForView = effectiveDepthForView;
  }

  public boolean isHavingIndirectParent() {
    return hasIndirectParent;
  }

  public void setHasIndirectParent(boolean hasIndirectParent) {
    this.hasIndirectParent = hasIndirectParent;
  }

}
