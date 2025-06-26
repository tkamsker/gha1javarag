package at.a1ta.cuco.core.shared.dto.nbo;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import at.a1ta.cuco.core.shared.dto.Party;

public class VBMProduct implements Serializable {
  private Long customerId;
  private String productId;
  private String monthYearPeriod;
  private Party party;
  private Long scoringTotal;
  private VBMProductDetails productDetails = new VBMProductDetails();
  private VBMProductFeedback productFeedback;
  private List<VBMDeclineReason> availableDeclineReasons = new ArrayList<VBMDeclineReason>();

  public Long getCustomerId() {
    return customerId;
  }

  public void setCustomerId(Long customerId) {
    this.customerId = customerId;
  }

  public String getMonthYearPeriod() {
    return monthYearPeriod;
  }

  public void setMonthYearPeriod(String monthYearPeriod) {
    this.monthYearPeriod = monthYearPeriod;
  }

  public Long getScoringTotal() {
    return scoringTotal;
  }

  public void setScoringTotal(Long scoringTotal) {
    this.scoringTotal = scoringTotal;
  }

  public List<VBMDeclineReason> getAvailableDeclineReasons() {
    return availableDeclineReasons;
  }

  public void setAvailableDeclineReasons(List<VBMDeclineReason> availableDeclineReasons) {
    this.availableDeclineReasons = availableDeclineReasons;
  }

  public boolean isAvailable() {
    // for later implementation
    return true;
  }

  public String getProductId() {
    return productId;
  }

  public void setProductId(String productId) {
    this.productId = productId;
  }

  public VBMProductDetails getProductDetails() {
    return productDetails;
  }

  public void setProductDetails(VBMProductDetails productDetails) {
    this.productDetails = productDetails;
  }

  public VBMProductFeedback getProductFeedback() {
    return productFeedback;
  }

  public void setProductFeedback(VBMProductFeedback productFeedback) {
    this.productFeedback = productFeedback;
  }

  public Party getParty() {
    return party;
  }

  public void setParty(Party party) {
    this.party = party;
  }
}
