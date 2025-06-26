package at.a1ta.cuco.core.shared.dto.chart;

import java.io.Serializable;
import java.util.LinkedHashMap;

public class ChartDataSet<K, V> implements Serializable {
  private String id;
  private LinkedHashMap<K, V> data = new LinkedHashMap<K, V>();

  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  public LinkedHashMap<K, V> getData() {
    return data;
  }

  public void add(K key, V value) {
    data.put(key, value);
  }
}
