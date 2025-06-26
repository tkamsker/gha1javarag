package at.a1ta.cuco.core.shared.dto.chart;

import at.a1ta.cuco.core.bean.File;

public class Chart extends File {
  private String imageMap;
  private String imageMapId;

  public Chart() {
    setMimeType(MIMEType.PNG);
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

}
