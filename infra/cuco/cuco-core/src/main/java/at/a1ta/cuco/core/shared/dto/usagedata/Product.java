package at.a1ta.cuco.core.shared.dto.usagedata;

import java.util.ArrayList;

import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;

public interface Product {
  public Party getParty();

  public ProductType getType();

  public NetworkProvider getProvider();

  public String getValue();

  public String getParentValue();

  public boolean isProductGroup();

  public boolean hasParty();

  public boolean hasParent();

  public boolean hasChildren();

  public ArrayList<Long> getPartyIds();

  public PhoneNumberStructure getPhoneNumberStructure();
}
