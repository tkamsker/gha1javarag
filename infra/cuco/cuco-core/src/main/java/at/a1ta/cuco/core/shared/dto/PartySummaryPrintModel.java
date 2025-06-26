package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.ArrayList;

import at.a1ta.cuco.core.shared.dto.product.PartySummaryItem;

public class PartySummaryPrintModel implements Serializable {
  private static final long serialVersionUID = 1L;

  private Party party;

  public Party getParty() {
    return party;
  }

  public void setParty(Party party) {
    this.party = party;
  }

  public ArrayList<PartySummaryItem> getProducts() {
    return products;
  }

  public void setProducts(ArrayList<PartySummaryItem> products) {
    this.products = products;
  }

  public ArrayList<PartySummaryItem> getSubscriptions() {
    return subscriptions;
  }

  public void setSubscriptions(ArrayList<PartySummaryItem> subscriptions) {
    this.subscriptions = subscriptions;
  }

  public ArrayList<PartySummaryItem> getIctServices() {
    return ictServices;
  }

  public void setIctServices(ArrayList<PartySummaryItem> ictServices) {
    this.ictServices = ictServices;
  }

  ArrayList<PartySummaryItem> products;

  ArrayList<PartySummaryItem> subscriptions;

  ArrayList<PartySummaryItem> ictServices;

}
