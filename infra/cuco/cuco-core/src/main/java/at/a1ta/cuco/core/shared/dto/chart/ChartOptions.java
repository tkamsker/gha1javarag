package at.a1ta.cuco.core.shared.dto.chart;

import java.io.Serializable;

public class ChartOptions implements Serializable {
  public static final ChartOptions defaultSmall = new ChartOptions(500, 300);
  public static final ChartOptions defaultBig = new ChartOptions(600, 400);

  private int width = 400;
  private int height = 400;

  private String imgMapId;

  private ChartColor[] colors = new ChartColor[] {ChartColor.BLUE, ChartColor.GREEN, ChartColor.RED};

  public ChartOptions() {}

  public ChartOptions(int width, int height) {
    this.width = width;
    this.height = height;
  }

  public int getWidth() {
    return width;
  }

  public void setWidth(int width) {
    this.width = width;
  }

  public int getHeight() {
    return height;
  }

  public void setHeight(int height) {
    this.height = height;
  }

  public ChartColor[] getColors() {
    return colors;
  }

  public void setColors(ChartColor[] colors) {
    this.colors = colors;
  }

  public String getImgMapId() {
    return imgMapId;
  }

  public void setImgMapId(String imgMapId) {
    this.imgMapId = imgMapId;
  }
}
