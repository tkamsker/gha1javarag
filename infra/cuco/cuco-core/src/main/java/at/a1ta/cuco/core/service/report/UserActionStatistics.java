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

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics;
import org.springframework.util.CollectionUtils;

import at.a1ta.bite.core.server.dto.UserActionRecord;

public class UserActionStatistics extends ActionStatisticBase<UserActionRecord> {

  private static double DEFAULT_MAX_VARIATION = 25;

  public UserActionStatistics(Collection<UserActionRecord> data) {
    super(data);
  }

  public List<ActionRecordStatistics> findSuspicious(List<UserActionRecord> raw) {
    if (hasValues() || CollectionUtils.isEmpty(raw)) {
      return Collections.emptyList();
    }

    List<ActionRecordStatistics> list = new ArrayList<ActionRecordStatistics>();
    for (UserActionRecord record : raw) {
      DescriptiveStatistics userStatistics = getStatistics(createKey(record));
      if (record.getActionCount() > DEFAULT_MAX_VARIATION) {
        double max = getActionLimit(userStatistics);
        if (record.getActionCount() > max) {
          ActionRecordStatistics ars = new ActionRecordStatistics(record);
          ars.setAllowedMax(max);
          ars.setDeviation(userStatistics.getStandardDeviation());
          ars.setMean(userStatistics.getMean());
          list.add(ars);
        }
      }
    }
    return list;
  }

  double getActionLimit(DescriptiveStatistics statistics) {
    return statistics.getMean() + calculateMaxVariation(statistics.getStandardDeviation());
  }

  double calculateMaxVariation(double standardDeviation) {

    if (Double.isNaN(standardDeviation) || standardDeviation <= 2.0D) {
      return DEFAULT_MAX_VARIATION;
    }

    if (standardDeviation <= 3.9D) {
      return standardDeviation * 8D;
    } else if (standardDeviation <= 7.9D) {
      return standardDeviation * 6D;
    } else if (standardDeviation <= 12.9D) {
      return standardDeviation * 4;
    }
    return standardDeviation * 2.0D;

  }

  public Map<Integer, Double> getMaximumDistribution(int limit) {
    HashMap<Integer, Double> values = new HashMap<Integer, Double>(limit);
    for (int i = 1; i <= limit; i++) {
      values.put(Integer.valueOf(i), calculateMaxVariation(i));
    }
    return values;
  }

  @Override
  String createKey(UserActionRecord record) {
    return createKey(record.getLogin(), record.getAction());
  }

  String createKey(String user, String action) {
    return user + "#" + action;
  }

  public static class ActionRecordStatistics {

    private final UserActionRecord actionRecord;

    public String getAction() {
      return actionRecord.getAction();
    }

    public Long getActionCount() {
      return actionRecord.getActionCount();
    }

    private double mean;
    private double deviation;
    private double allowedMax;

    public ActionRecordStatistics(UserActionRecord actionRecord) {
      this.actionRecord = actionRecord;
    }

    public double getMean() {
      return mean;
    }

    public void setMean(double mean) {
      this.mean = mean;
    }

    public double getDeviation() {
      return deviation;
    }

    public void setDeviation(double deviation) {
      this.deviation = deviation;
    }

    public double getAllowedMax() {
      return allowedMax;
    }

    public void setAllowedMax(double allowedMax) {
      this.allowedMax = allowedMax;
    }

    public UserActionRecord getActionRecord() {
      return actionRecord;
    }

  }

}
