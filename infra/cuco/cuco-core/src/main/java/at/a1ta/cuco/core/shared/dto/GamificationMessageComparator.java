package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Comparator;

public class GamificationMessageComparator implements Comparator<GamificationMessage>, Serializable {
  private static final long serialVersionUID = 1L;

  @Override
  public int compare(GamificationMessage o1, GamificationMessage o2) {
    try {
      return o2.getTimestampDateFormat().compareTo(o1.getTimestampDateFormat());
    } catch (Exception e) {
      return o2.getMessageUid().compareTo(o1.getMessageUid());
    }
  }
}
