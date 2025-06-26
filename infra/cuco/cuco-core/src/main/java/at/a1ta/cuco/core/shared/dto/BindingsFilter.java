package at.a1ta.cuco.core.shared.dto;

import java.util.Date;

public class BindingsFilter {
  public static final String CONTRACT_ID = "contract";
  public static final String CONTRACT_START_ID = "contractStart";
  public static final String PARTY_ID = "partyId";
  public static final String PRODUCT_DESCRIPTION_ID = "productDescription";

  public enum Contract {
    ALL, ALL_EXPIRED, ALL_EXPIRING, TIMERANGE_1, TIMERANGE_2, TIMERANGE_3, LARGER_TIMERANGE_3
  }

  private String partyId;
  private String productDescription;
  private Date contractStart;
  private Contract contractEnd;

  public String getPartyId() {
    return partyId;
  }

  public void setPartyId(String partyId) {
    this.partyId = partyId;
  }

  public Contract getContractEnd() {
    return contractEnd;
  }

  public void setContract(Contract contractEnd) {
    this.contractEnd = contractEnd;
  }

  public void setProductDescription(String productDescription) {
    this.productDescription = productDescription;
  }

  public String getProductDescription() {
    return productDescription;
  }

  public void setContractStart(Date contractStart) {
    this.contractStart = contractStart;
  }

  public Date getContractStart() {
    return contractStart;
  }

}
