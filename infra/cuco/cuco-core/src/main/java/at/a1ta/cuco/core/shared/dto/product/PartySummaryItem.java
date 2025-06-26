package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

@SuppressWarnings("serial")
public class PartySummaryItem implements Serializable {
  private String name;
  private String url;
  private long count;

  public PartySummaryItem(String name, int count) {
    this.setName(name);
    this.setCount(count);
  }

  public PartySummaryItem(String name, String url) {
    this.setName(name);
    this.setUrl(url);
  }

  public PartySummaryItem() {
    super();
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

  public String getUrl() {
    return url;
  }

  public void setUrl(String url) {
    this.url = url;
  }
}
