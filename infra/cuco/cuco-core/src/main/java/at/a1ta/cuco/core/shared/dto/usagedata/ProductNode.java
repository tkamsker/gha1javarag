package at.a1ta.cuco.core.shared.dto.usagedata;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;

public class ProductNode implements Product, Serializable {
  private String label;
  private String value;
  private Party party;
  private ProductType type;
  private NetworkProvider provider;
  private ProductNode parent;
  private PhoneNumberStructure phoneNumberStructure;
  private ArrayList<ProductNode> children = new ArrayList<ProductNode>();

  public static ProductNode createProduct(Party party, ProductType type, NetworkProvider provider, String value, String label) {
    ProductNode product = new ProductNode();
    product.setParty(party);
    product.setType(type);
    product.setProvider(provider);
    product.setValue(value);
    product.setLabel(label);
    return product;
  }

  public String getLabel() {
    return label;
  }

  public void setLabel(String label) {
    this.label = label;
  }

  @Override
  public String getValue() {
    return value;
  }

  @Override
  public String getParentValue() {
    return parent != null ? parent.value : null;
  }

  public void setValue(String value) {
    this.value = value;
  }

  @Override
  public Party getParty() {
    return party;
  }

  public void setParty(Party party) {
    this.party = party;
  }

  @Override
  public ProductType getType() {
    return type;
  }

  public void setType(ProductType type) {
    this.type = type;
  }

  @Override
  public NetworkProvider getProvider() {
    return provider;
  }

  public void setProvider(NetworkProvider provider) {
    this.provider = provider;
  }

  public ProductNode getParent() {
    return parent;
  }

  public void setParent(ProductNode parent) {
    this.parent = parent;
  }

  public ArrayList<ProductNode> getChildren() {
    return children;
  }

  public void addChild(ProductNode child) {
    children.add(child);
    child.parent = this;
  }

  public void addChildren(List<ProductNode> children) {
    for (ProductNode child : children) {
      addChild(child);
    }
  }

  @Override
  public boolean isProductGroup() {
    return !hasParent() || (!parent.hasParent() && !parent.hasParty());
  }

  @Override
  public boolean hasParty() {
    return party != null;
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
  public ArrayList<Long> getPartyIds() {
    if (!hasParty()) {
      final ArrayList<Long> partyIds = new ArrayList<Long>();
      for (final ProductNode child : children) {
        partyIds.add(child.party.getId());
      }
      return partyIds;
    }

    return new ArrayList<Long>(Arrays.asList(party.getId()));

  }

  public boolean isANB() {
    return NetworkProvider.ANB == provider;
  }

  public boolean isType(ProductType type) {
    return type == this.type;
  }

  @Override
  public PhoneNumberStructure getPhoneNumberStructure() {
    return phoneNumberStructure;
  }

  public void setPhoneNumberStructure(PhoneNumberStructure phoneNumberStructure) {
    this.phoneNumberStructure = phoneNumberStructure;
  }

}
