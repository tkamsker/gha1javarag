package at.a1ta.cuco.core.shared.dto.chart;

import java.io.Serializable;
import java.util.Collection;
import java.util.LinkedHashMap;

public class ChartData<K, V> implements Serializable {
  private LinkedHashMap<String, ChartDataSet<K, V>> data = new LinkedHashMap<String, ChartDataSet<K, V>>();

  public ChartDataSet<K, V> getDataSet(final String dataSetKey) {
    if (data.containsKey(dataSetKey)) {
      return data.get(dataSetKey);
    }

    final ChartDataSet<K, V> dataSet = new ChartDataSet<K, V>();
    dataSet.setId(dataSetKey);
    data.put(dataSetKey, dataSet);
    return dataSet;
  }

  public Collection<ChartDataSet<K, V>> getDataSets() {
    return data.values();
  }
}
