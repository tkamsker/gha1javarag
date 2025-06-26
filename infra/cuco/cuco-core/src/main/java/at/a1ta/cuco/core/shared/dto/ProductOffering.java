package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.ArrayList;

public enum ProductOffering implements Serializable {

  A1BN(1, "a1bn"), MOBILE_INTERNET_ET_GT(2, "etgt"), FIB(3, "fib"), BIZKO(4, "bizko"), BPB(5, "bpb"), A1CML(6, "a1cml"), PSHC(7, "pshc"), A1TVRES(8, "a1tvres"), A1BI(9, "a1bi"), A1PS(10,
      "a1ps"), A1VOIP(11, "a1voip"), DAAS(12, "daas"), MARKETPLACE(13, "marketplace"), BFW(14, "bfw"), A1BIP(15, "a1bip"), CCS(16,"ccs"), ALL(99, "");

  private static final long serialVersionUID = 1L;

  private long id;
  private String packageName;

  private ArrayList<String> variables;

  private ProductOffering(long id, String packageName) {
    this.id = id;
    this.packageName = packageName;
  }

  public long getId() {
    return id;
  }

  public void setId(long id) {
    this.id = id;
  }

  public String getPackageName() {
    return packageName;
  }

  public void setPackageName(String packageName) {
    this.packageName = packageName;
  }

  public static ProductOffering valueOf(long id) {
    for (ProductOffering po : values()) {
      if (po.getId() == id) {
        return po;
      }
    }
    return null;
  }

  public ArrayList<String> getVariables() {
    return variables;
  }

  public void setVariables(ArrayList<String> variables) {
    this.variables = variables;
  }

  public static boolean hasMarketingProductConfiguration(ProductOffering productOffering) {
    return productOffering == MARKETPLACE || productOffering == A1PS || productOffering == A1BN || productOffering == A1BI || productOffering == MOBILE_INTERNET_ET_GT || productOffering == CCS;
  }

  public static boolean supportsAdminConfiguration(ProductOffering productOffering) {
    return productOffering == A1BIP || productOffering == BFW;
  }

}
