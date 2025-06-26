package at.a1ta.cuco.core.shared.dto.usagedata;

import java.io.Serializable;
import java.util.ArrayList;

import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;

public class ProductChartRequest implements Product, Serializable {
  private Party party;
  private ProductType type;
  private NetworkProvider provider;
  private String value;
  private String parentValue;
  private boolean isProductGroup;
  private boolean hasParty;
  private boolean hasParent;
  private boolean hasChildren;
  private ArrayList<Long> partyIds;
  private PhoneNumberStructure phoneNumberStructure;
  private boolean anb;

  private ProductChartRequest() {}

  public static ProductChartRequest create(ProductNode product) {
    return create(product, product.getType());
  }

  public static ProductChartRequest create(ProductNode product, ProductType overrideType) {
    ProductChartRequest clone = new ProductChartRequest();
    clone.party = product.getParty();
    clone.type = overrideType;
    clone.provider = product.getProvider();
    clone.value = product.getValue();
    clone.parentValue = product.getParentValue();
    clone.isProductGroup = product.isProductGroup();
    clone.hasParty = product.hasParty();
    clone.hasParent = product.hasParent();
    clone.hasChildren = product.hasChildren();
    clone.partyIds = product.getPartyIds();
    clone.phoneNumberStructure = product.getPhoneNumberStructure();
    return clone;
  }

  @Override
  public Party getParty() {
    return party;
  }

  @Override
  public ProductType getType() {
    return type;
  }

  @Override
  public NetworkProvider getProvider() {
    return provider;
  }

  @Override
  public String getValue() {
    return value;
  }

  @Override
  public String getParentValue() {
    return parentValue;
  }

  @Override
  public boolean isProductGroup() {
    return isProductGroup;
  }

  @Override
  public boolean hasParty() {
    return hasParty;
  }

  @Override
  public boolean hasParent() {
    return hasParent;
  }

  @Override
  public boolean hasChildren() {
    return hasChildren;
  }

  @Override
  public ArrayList<Long> getPartyIds() {
    return partyIds;
  }

  @Override
  public PhoneNumberStructure getPhoneNumberStructure() {
    return phoneNumberStructure;
  }

  public boolean isAnb() {
    return anb;
  }

  public void setAnb(boolean anb) {
    this.anb = anb;
  }

}
