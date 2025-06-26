package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class ProductOverviewConfigurations implements Serializable {
  private String amountOfSubscriptionToPreload;
  private String depthOfProductTree;
  private String mode;
  private String whitelist;
  private String blacklist;
  private static final long serialVersionUID = 1L;

  public String getAmountOfSubscriptionToPreload() {
    return amountOfSubscriptionToPreload;
  }

  public void setAmountOfSubscriptionToPreload(String amountOfSubscriptionToPreload) {
    this.amountOfSubscriptionToPreload = amountOfSubscriptionToPreload;
  }

  public String getDepthOfProductTree() {
    return depthOfProductTree;
  }

  public void setDepthOfProductTree(String depthOfProductTree) {
    this.depthOfProductTree = depthOfProductTree;
  }

  public String getMode() {
    return mode;
  }

  public void setMode(String mode) {
    this.mode = mode;
  }

  public String getWhitelist() {
    return whitelist;
  }

  public void setWhitelist(String whitelist) {
    this.whitelist = whitelist;
  }

  public String getBlacklist() {
    return blacklist;
  }

  public void setBlacklist(String blacklist) {
    this.blacklist = blacklist;
  }

}
