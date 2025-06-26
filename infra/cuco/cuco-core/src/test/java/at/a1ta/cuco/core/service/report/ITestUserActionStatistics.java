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

import java.util.List;

import org.junit.Assert;
import org.junit.Test;

import at.a1ta.bite.core.server.dto.UserActionRecord;
import at.a1ta.cuco.core.service.report.UserActionStatistics.ActionRecordStatistics;

public class ITestUserActionStatistics extends UserActionStatisticsTestBase {

  @Test
  public void testActionCountExceedsAllowedMaximum() {
    List<UserActionRecord> historicalData = readRecordsFromFile("weeklyUserActionData.txt");
    UserActionStatistics stats = new UserActionStatistics(historicalData);

    List<UserActionRecord> currentData = readRecordsFromFile("dailyUserActionData.txt");

    List<ActionRecordStatistics> pThreat = stats.findSuspicious(currentData);
    for (ActionRecordStatistics rec : pThreat) {
      Assert.assertTrue(rec.getActionCount() > rec.getAllowedMax());
    }

  }

}
