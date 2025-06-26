package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class MatrixPosition<T> implements Serializable {
  private long segment; // column
  private long category; // row
  private Integer sequence; // position inside the cell
  private T object;

  public long getSegment() {
    return segment;
  }

  public void setSegment(long segment) {
    this.segment = segment;
  }

  public long getCategory() {
    return category;
  }

  public void setCategory(long category) {
    this.category = category;
  }

  public T getObject() {
    return object;
  }

  public void setObject(T object) {
    this.object = object;
  }

  public void setSequence(Integer sequence) {
    this.sequence = sequence;
  }

  public Integer getSequence() {
    return sequence;
  }
}
