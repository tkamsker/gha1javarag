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

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import at.a1ta.bite.core.server.dto.UserActionRecord;
import at.a1ta.cuco.core.service.report.UserActionStatistics.ActionRecordStatistics;

public class UserActionStatisticsTest extends UserActionStatisticsTestBase {

  private final String LOW_USAGE_USER = "lowUsageUser";
  private final String MEDIUM_USAGE_USER = "mediumUsageUser";
  private final String HIGH_USAGE_USER = "highUsageUser";

  /* @formatter:off */
  private final String [] REFERENCE_DATA_LINES = {
      //mean: ; standardDeviation: ;
      LOW_USAGE_USER+","+ACTION+",01.08.2013,5",
      LOW_USAGE_USER+","+ACTION+",29.07.2013,10",
      LOW_USAGE_USER+","+ACTION+",30.07.2013,5",
      LOW_USAGE_USER+","+ACTION+",31.07.2013,20",
      HIGH_USAGE_USER+","+ACTION+",01.08.2013,20",
      HIGH_USAGE_USER+","+ACTION+",29.07.2013,70",
      HIGH_USAGE_USER+","+ACTION+",30.07.2013,50",
      HIGH_USAGE_USER+","+ACTION+",31.07.2013,60",
      MEDIUM_USAGE_USER+","+ACTION+",01.08.2013,30",
      MEDIUM_USAGE_USER+","+ACTION+",29.07.2013,32",
      MEDIUM_USAGE_USER+","+ACTION+",30.07.2013,27",
      MEDIUM_USAGE_USER+","+ACTION+",31.07.2013,29"};
  /* @formatter:on */

  private final String VIOLATING_DATA_LINE = (LOW_USAGE_USER + "," + ACTION + ",02.08.2013,55");
  private final String NON_VIOLATING_DATA_LINE = (MEDIUM_USAGE_USER + "," + ACTION + ",02.08.2013,31");

  private UserActionStatistics stats;

  @Before
  public void setUp() {
    stats = new UserActionStatistics(generate());
  }

  @Test
  public void testGetStatisticsForUserAndAction() {
    DescriptiveStatistics statistics = stats.getStatistics(stats.createKey(LOW_USAGE_USER, ACTION));
    Assert.assertEquals(4, statistics.getN());
  }

  @Test
  public void testGetStatisticsForUserAndActionReturnsEmptyStatisticWhenNoDataForUserAvailable() {
    DescriptiveStatistics statistics = stats.getStatistics(stats.createKey("NoDataAvailable", ACTION));
    Assert.assertNotNull(statistics);
    Assert.assertEquals(0, statistics.getN());
  }

  @Test
  public void testGetStatisticsForUserAndActionReturnsEmptyStatisticWhenNoDataForActionAvailable() {
    DescriptiveStatistics statistics = stats.getStatistics(stats.createKey(LOW_USAGE_USER, "NoDataAvailable"));
    Assert.assertNotNull(statistics);
    Assert.assertEquals(0, statistics.getN());
  }

  @Test
  public void testFindSuspicousReturnsEmptyListIfNoDataAvailable() {
    stats = new UserActionStatistics(Collections.<UserActionRecord> emptyList());
    Assert.assertTrue(stats.findSuspicious(Arrays.asList(new UserActionRecord())).isEmpty());
  }

  @Test
  public void testFindSuspicousReturnsEmptyListIfRequestedForEmptyList() {
    Assert.assertTrue(stats.findSuspicious(Collections.<UserActionRecord> emptyList()).isEmpty());
  }

  @Test
  public void testFindSuspicousReturnsCorrectUsers() {
    List<UserActionRecord> violating = Arrays.asList(createActionRecordFromDataLine(VIOLATING_DATA_LINE), createActionRecordFromDataLine(NON_VIOLATING_DATA_LINE));

    List<ActionRecordStatistics> result = stats.findSuspicious(violating);
    Assert.assertEquals(1, result.size());
  }

  private List<UserActionRecord> generate() {
    return generate(Arrays.asList(REFERENCE_DATA_LINES));
  }

}
