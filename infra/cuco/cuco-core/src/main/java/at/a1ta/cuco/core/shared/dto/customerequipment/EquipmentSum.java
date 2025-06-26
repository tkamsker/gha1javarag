package at.a1ta.cuco.core.shared.dto.customerequipment;

import java.io.Serializable;

public class EquipmentSum implements Serializable, Comparable<EquipmentSum> {
  private static final String EMPTY = "";

  private String id;
  private String title;
  private long count;

  public EquipmentSum() {}

  public EquipmentSum(final String id, final String title, final long count) {
    this.id = id;
    this.title = title;
    this.count = count;
  }

  public String getId() {
    return id;
  }

  public void setId(final String id) {
    this.id = id;
  }

  public String getTitle() {
    return title;
  }

  public void setTitle(final String title) {
    this.title = title;
  }

  public long getCount() {
    return count;
  }

  public void setCount(long count) {
    this.count = count;
  }

  public void incrementCount() {
    count++;
  }

  @Override
  public int compareTo(final EquipmentSum o) {
    final String thisTitle = this.title == null ? EMPTY : this.title;
    final String otherTitle = o.title == null ? EMPTY : o.title;
    return thisTitle.compareTo(otherTitle);
  }
}
