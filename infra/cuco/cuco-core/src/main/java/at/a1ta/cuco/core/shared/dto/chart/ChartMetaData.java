package at.a1ta.cuco.core.shared.dto.chart;

import java.io.Serializable;

public class ChartMetaData implements Serializable {
  private String imageMap;
  private String imageMapId;
  private String hash;

  public ChartMetaData() {}

  public ChartMetaData(String imageMapId, String imageMap, String hash) {
    this.imageMap = imageMap;
    this.setImageMapId(imageMapId);
    this.hash = hash;
  }

  public String getImageMap() {
    return imageMap;
  }

  public void setImageMap(String imageMap) {
    this.imageMap = imageMap;
  }

  public void setImageMapId(String imageMapId) {
    this.imageMapId = imageMapId;
  }

  public String getImageMapId() {
    return imageMapId;
  }

  public String getHash() {
    return hash;
  }

  public void setHash(String hash) {
    this.hash = hash;
  }

}
