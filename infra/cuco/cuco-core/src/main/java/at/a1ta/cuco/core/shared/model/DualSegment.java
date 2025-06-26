package at.a1ta.cuco.core.shared.model;

import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;

public enum DualSegment {
  ALL(8, "Alle"), WIRED(1, "Festnetz"), MOBILE(2, "Mobilfunk"), DUAL(3, "Dual"), CONVERGENT(4, "Konvergent"), CONVERGENTWIRED(5, "Festnetz & konvergent"), CONVERGENTMOBILE(6, "Mobilfunk & konvergent"), DUALCONVERGENT(7, "Dual & konvergent"), NONCUSTOMER(9, "Nicht-Kunden"), UNKNOWN(-1, "Unbekannt");

  private static final Map<Integer, DualSegment> lookup = new HashMap<Integer, DualSegment>();

  static {
    for (DualSegment dualSegment : EnumSet.allOf(DualSegment.class)) {
      lookup.put(dualSegment.getCode(), dualSegment);
    }
  }

  private int code;
  private String title;

  private DualSegment(int code, String title) {
    this.code = code;
    this.title = title;
  }

  public int getCode() {
    return code;
  }

  public String getTitle() {
    return title;
  }

  public static DualSegment get(int code) {
    DualSegment segment = lookup.get(code);
    if (segment == null) {
      segment = UNKNOWN;
    }
    return segment;
  }

}
