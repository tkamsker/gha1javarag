/*
 * Copyright 2009 - 2013 by A1 Telekom Austria AG
 * All Rights Reserved.
 * 
 * The Software is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * All information contained herein is, and remains the property of
 * A1 Telekom Austria AG and its suppliers, if any.
 * The intellectual and technical concepts contained herein are proprietary
 * to A1 Telekom Austria AG and its suppliers and may be covered by
 * intertional or national patents, patents in process, and are protected
 * by trade secret or copyright law. Dissemination of this information or
 * reproduction of this material is strictly forbidden unless prior written
 * permission is obtained from A1 Telekom Austria AG.
 */
package at.a1ta.cuco.core.service.report;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics;
import org.apache.commons.math3.stat.descriptive.SynchronizedDescriptiveStatistics;
import org.springframework.util.CollectionUtils;

import at.a1ta.bite.core.server.dto.ActionRecord;

public abstract class ActionStatisticBase<T extends ActionRecord> {

  private final Map<String, DescriptiveStatistics> stats;

  protected ActionStatisticBase(Collection<T> data) {
    stats = new HashMap<String, DescriptiveStatistics>();
    initStatistics(data);
  }

  private void initStatistics(Iterable<T> data) {
    for (T record : data) {
      addRecordToStatistic(record);
    }
  }

  protected void addRecordToStatistic(T record) {
    findOrCreateStatsForAction(record).addValue(record.getActionCount());
  }

  private DescriptiveStatistics findOrCreateStatsForAction(T record) {
    return findOrCreateStatsForAction(createKey(record));
  }

  private DescriptiveStatistics findOrCreateStatsForAction(String key) {
    if (!stats.containsKey(key)) {
      stats.put(key, new SynchronizedDescriptiveStatistics());
    }
    return stats.get(key);
  }

  public DescriptiveStatistics getStatistics(String key) {
    return findOrCreateStatsForAction(key);
  }

  public boolean hasValues() {
    return CollectionUtils.isEmpty(stats);
  }

  abstract String createKey(T record);

}
