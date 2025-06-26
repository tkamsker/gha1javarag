package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class CustomerBlock implements Serializable {
  private long id = -1;
  private String name;
  private long count;
  private boolean imported;
  private String data;
  private FlashInfo flashInfo;

  public long getId() {
    return id;
  }

  public void setId(long id) {
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public long getCount() {
    return count;
  }

  public void setCount(long count) {
    this.count = count;
  }

  public boolean isImported() {
    return imported;
  }

  public void setImported(boolean imported) {
    this.imported = imported;
  }

  public String getData() {
    return data;
  }

  public void setData(String data) {
    this.data = data;
  }

  public FlashInfo getFlashInfo() {
    return flashInfo;
  }

  public void setFlashInfo(FlashInfo flashInfo) {
    this.flashInfo = flashInfo;
  }
}
