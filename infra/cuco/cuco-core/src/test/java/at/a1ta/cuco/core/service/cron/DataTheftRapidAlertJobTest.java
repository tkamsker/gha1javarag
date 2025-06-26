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
package at.a1ta.cuco.core.service.cron;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.List;

import org.apache.commons.lang.time.DateUtils;
import org.joda.time.LocalDate;
import org.joda.time.LocalDateTime;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Matchers;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.core.server.dto.TimeSpan;
import at.a1ta.bite.core.server.dto.UserActionRecord;
import at.a1ta.bite.core.server.dto.UserRecordActionType;
import at.a1ta.bite.core.server.service.UserTrackingService;
import at.a1ta.cuco.core.service.impl.MailService;
import at.a1ta.cuco.core.service.report.UserActionStatistics.ActionRecordStatistics;

@RunWith(MockitoJUnitRunner.class)
public class DataTheftRapidAlertJobTest {

  @Mock
  private UserTrackingService trackingServiceMock;

  @Mock
  private MailService mailServiceMock;

  private DataTheftRapidAlertJob job;

  @Before
  public void setUp() {
    job = new DataTheftRapidAlertJob(trackingServiceMock, mailServiceMock);
  }

  @Test
  public void testGetJobIdReturnsClassNameInPropertyStyle() {
    Assert.assertEquals("dataTheftRapidAlertJob", job.getJobId());
  }

  @Test
  public void testProcessLoadsDataCorrectly() {
    ArgumentCaptor<TimeSpan> captor = ArgumentCaptor.forClass(TimeSpan.class);
    job.process();

    Mockito.verify(trackingServiceMock, Mockito.times(2)).findUserActionsForDateGroupByAction(captor.capture(), Matchers.any(UserRecordActionType.class));
    Assert.assertTrue(DateUtils.isSameDay(new Date(), captor.getValue().getStart()));
    Assert.assertTrue(DateUtils.isSameDay(LocalDate.now().minusDays(14).toDate(), captor.getAllValues().get(0).getStart()));
    Assert.assertTrue(DateUtils.isSameDay(LocalDateTime.now().minusDays(1).toDate(), captor.getAllValues().get(0).getEnd()));
  }

  @Test
  public void testReportThreatsToExceutivesWorksCorrectlyWhenDataAvailable() throws Exception {
    List<ActionRecordStatistics> satisticRecords = new ArrayList<ActionRecordStatistics>();
    satisticRecords.add(createRecordStatistics("user-1"));

    ArgumentCaptor<String> captor = ArgumentCaptor.forClass(String.class);
    job.reportThreatsToExecutives(satisticRecords);

    Mockito.verify(mailServiceMock, Mockito.times(1)).sendThreatReportMail(captor.capture());
    Assert.assertEquals("<ul><li>Benutzer user-1 hat 100 Kunden aufgerufen. [Durchschnitt: 25 | Erlaubt: 50]</li></ul>", captor.getValue());
  }

  @Test
  public void testReportThreatsDoesNotSendMailWhenNoDataAvailable() throws Exception {
    job.reportThreatsToExecutives(Collections.<ActionRecordStatistics> emptyList());

    Mockito.verifyZeroInteractions(mailServiceMock);
  }

  @Test
  public void testReportThreatsDoesNotSendMailWhenNullPassedIn() throws Exception {
    job.reportThreatsToExecutives(null);

    Mockito.verifyZeroInteractions(mailServiceMock);
  }

  private ActionRecordStatistics createRecordStatistics(String username) {
    ActionRecordStatistics stats = new ActionRecordStatistics(createUserActionRecord(username));
    stats.setAllowedMax(50);
    stats.setDeviation(5);
    stats.setMean(25);
    return stats;
  }

  private UserActionRecord createUserActionRecord(String username) {
    UserActionRecord record = new UserActionRecord();
    record.setLogin(username);
    record.setActionCount(100L);
    record.setDate(new Date());
    record.setAction("action");

    return record;
  }
}
