package at.a1ta.cuco.core.shared.dto.chart;

public enum ChartColor {
  RED(255, 10, 10), GREEN(60, 190, 50), BLUE(10, 10, 255), BLACK(0, 0, 0);

  public final int r;
  public final int g;
  public final int b;

  private ChartColor(int r, int g, int b) {
    this.r = r;
    this.g = g;
    this.b = b;
  }

}
