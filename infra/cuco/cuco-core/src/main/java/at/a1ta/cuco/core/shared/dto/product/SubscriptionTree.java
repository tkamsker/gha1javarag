package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;
import java.util.ArrayList;

public class SubscriptionTree implements Serializable {
  private ArrayList<BaseNode> productNodes;
  private DefaultSubscriptionNode subscriptionNode;

  public ArrayList<BaseNode> getProductNodes() {
    return productNodes;
  }

  public void setProductNodes(ArrayList<BaseNode> productNodes) {
    this.productNodes = productNodes;
  }

  public DefaultSubscriptionNode getSubscriptionNode() {
    return subscriptionNode;
  }

  public void setSubscriptionNode(DefaultSubscriptionNode subscriptionNode) {
    this.subscriptionNode = subscriptionNode;
  }

}
