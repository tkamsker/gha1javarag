package at.a1ta.cuco.core.shared.dto.product;

import at.a1ta.cuco.core.shared.dto.product.DefaultProductNode.ProductType;

public class NodeHelper {
  public static PartyNode getPartyNode(Node node) {
    if (node instanceof PartyNode) {
      return (PartyNode) node;
    }
    if (!node.hasParent()) {
      return null;
    }
    if (node.getParent() instanceof PartyNode) {
      return (PartyNode) node.getParent();
    }
    return getPartyNode(node.getParent());
  }

  public static LocationNode getLocationNode(Node node) {
    if (node instanceof LocationNode) {
      return (LocationNode) node;
    }
    if (!node.hasParent()) {
      return null;
    }
    if (node.getParent() instanceof LocationNode) {
      return (LocationNode) node.getParent();
    }
    return getLocationNode(node.getParent());
  }

  public static SubscriptionNode getSubscriptionNode(Node node) {
    if (node instanceof SubscriptionNode) {
      return (SubscriptionNode) node;
    }
    if (!node.hasParent()) {
      return null;
    }
    if (node.getParent() instanceof SubscriptionNode) {
      return (SubscriptionNode) node.getParent();
    }
    return getSubscriptionNode(node.getParent());
  }

  public static DefaultProductNode getDefaultProductNode(Node node) {
    if (node instanceof DefaultProductNode) {
      return (DefaultProductNode) node;
    }
    if (!node.hasParent()) {
      return null;
    }
    if (node.getParent() instanceof DefaultProductNode) {
      return (DefaultProductNode) node.getParent();
    }
    return getDefaultProductNode(node.getParent());
  }

  public static boolean hasChildProductNodeOfType(BaseNode node, ProductType type) {
    if (node.getChildren() != null) {
      for (Node child : node.getChildren()) {
        if (child instanceof DefaultProductNode) {
          DefaultProductNode productNode = (DefaultProductNode) child;
          if (type.equals(productNode.getVoiceProductType())) {
            return true;
          } else if (hasChildProductNodeOfType(productNode, type)) {
            return true;
          }
        } else if (hasChildProductNodeOfType((BaseNode) child, type)) {
          return true;
        }
      }
    }
    return false;
  }

  public static DefaultSubscriptionNode getFirstChildSubscriptionNode(Node node) {
    if (node.getChildren() != null) {
      for (Node child : node.getChildren()) {
        if (child instanceof DefaultSubscriptionNode) {
          return (DefaultSubscriptionNode) child;
        }
        return getFirstChildSubscriptionNode(child);
      }
    }
    return null;
  }

}
