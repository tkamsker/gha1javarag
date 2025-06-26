package at.a1ta.cuco.core.shared.dto;

import java.util.ArrayList;
import java.util.List;

import at.a1ta.bite.core.shared.dto.KeyValuePair;
import at.a1ta.cuco.core.shared.dto.nbo.VBMProductDetails;
import at.a1ta.cuco.core.shared.model.DualSegment;

public class CustomerFilter {

  public static final String VIP_ID = "vip";
  public static final String TURNOVERREGIONS_ID = "turnoverRegions";
  public static final String CUSTOMERWORTHCLASS_ID = "customerWorthClass";
  public static final String DUALSEGMENTS_ID = "dualSegments";
  public static final String FLASHINFO_ID = "flashInfo";
  public static final String CHURNRISK_ID = "churnRisk";
  public static final String PARTY_ID = "partyId";
  public static final String PLZ = "plz";
  public static final String INDEXATION = "indexation";
  public static final String VBM_PRODUCTS = "vbm";

  // public static final String VBM = "availableVbmProducts";

  public enum Churn {
    ALL, DANGER, NODANGER
  }

  public enum FlashInfo {
    ALL, NOFLASH, FLASH
  }

  public enum Vip {
    ALL, NOVIP, VIP
  }

  public enum WorthClass {
    ALL, GOLD, SILBER, BRONZE, BLEI, UNKNOWN
  }

  public enum Indexation {
    ALL, MitIndexierung, MitIndexanpassung, OhneIndexierung
  }

  /*
   * public enum Vbm {
   * ALL_PROD, NO_PROD_FILTER
   * }
   */

  private Churn churn;
  private FlashInfo flashInfo;
  private Vip vip;
  private Indexation indexation;
  private List<DualSegment> dualSegments;
  private List<WorthClass> worthClasses;
  private List<String> turnoverRanges;
  private List<String> vbmProducts;
  private String partyId;
  private String plz;
  private List<VBMProductDetails> productDetailsFilter;

  public Churn getChurn() {
    return churn;
  }

  public void setChurn(Churn churn) {
    this.churn = churn;
  }

  public FlashInfo getFlashInfo() {
    return flashInfo;
  }

  public void setFlashInfo(FlashInfo flashInfo) {
    this.flashInfo = flashInfo;
  }

  public Vip getVip() {
    return vip;
  }

  public void setVip(Vip vip) {
    this.vip = vip;
  }

  public Indexation getIndexation() {
    return indexation;
  }

  public void setIndexation(Indexation indexation) {
    this.indexation = indexation;
  }

  public List<DualSegment> getDualSegments() {
    return dualSegments;
  }

  public void setDualSegments(List<DualSegment> dualSegments) {
    this.dualSegments = dualSegments;
  }

  public void setDualSegmentsByKeyValuePairs(List<KeyValuePair> dualSegmentKeyValuePairs) {
    dualSegments = new ArrayList<DualSegment>();
    for (KeyValuePair dualSegmentKeyValuePair : dualSegmentKeyValuePairs) {
      dualSegments.add(DualSegment.valueOf(dualSegmentKeyValuePair.getKey()));
    }
  }

  public void addDualSegment(DualSegment dualSegment) {
    if (dualSegments == null) {
      dualSegments = new ArrayList<DualSegment>();
    }
    dualSegments.add(dualSegment);
  }

  public List<WorthClass> getWorthClasses() {
    return worthClasses;
  }

  public void setWorthClasses(List<WorthClass> worthClasses) {
    this.worthClasses = worthClasses;
  }

  public void setWorthClassesByKeyValuePairs(List<KeyValuePair> worthClassKeyValuePairs) {
    worthClasses = new ArrayList<WorthClass>();
    for (KeyValuePair worthClassKeyValuePair : worthClassKeyValuePairs) {
      worthClasses.add(WorthClass.valueOf(worthClassKeyValuePair.getKey()));
    }
  }

  public void addWorthClass(WorthClass worthClass) {
    if (worthClasses == null) {
      worthClasses = new ArrayList<WorthClass>();
    }
    worthClasses.add(worthClass);
  }

  public List<String> getTurnoverRanges() {
    return turnoverRanges;
  }

  public void setTurnoverRanges(List<String> turnoverRanges) {
    this.turnoverRanges = turnoverRanges;
  }

  public void setTurnoverRangesByKeyValuePairs(List<KeyValuePair> turnoverRangeKeyValuePairs) {
    turnoverRanges = new ArrayList<String>();
    for (KeyValuePair turnoverRangeKeyValuePair : turnoverRangeKeyValuePairs) {
      turnoverRanges.add(turnoverRangeKeyValuePair.getKey());
    }
  }

  public void addTurnoverRange(String turnoverRange) {
    if (turnoverRanges == null) {
      turnoverRanges = new ArrayList<String>();
    }
    turnoverRanges.add(turnoverRange);
  }

  public void setPartyId(String partyId) {
    this.partyId = partyId;
  }

  public String getPartyId() {
    return partyId;
  }

  public List<VBMProductDetails> getProductDetailsFilter() {
    return productDetailsFilter;
  }

  public void setProductDetailsFilter(List<VBMProductDetails> productDetailsFilter) {
    this.productDetailsFilter = productDetailsFilter;
  }

  public List<String> getVbmProducts() {
    return vbmProducts;
  }

  public void setVbmProducts(List<String> vbmProducts) {
    this.vbmProducts = vbmProducts;
  }

  public String getPlz() {
    return plz;
  }

  public void setPlz(String plz) {
    this.plz = plz;
  }
}
