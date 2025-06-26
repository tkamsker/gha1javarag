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

import java.text.MessageFormat;
import java.util.Iterator;
import java.util.List;

import org.joda.time.LocalDate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;
import org.springframework.util.ClassUtils;
import org.springframework.util.CollectionUtils;

import at.a1ta.bite.core.server.cron.AbstractCronJob;
import at.a1ta.bite.core.server.dto.TimeSpan;
import at.a1ta.bite.core.server.dto.UserActionRecord;
import at.a1ta.bite.core.server.dto.UserRecordActionType;
import at.a1ta.bite.core.server.service.UserTrackingService;
import at.a1ta.bite.core.shared.EnvironmentProfiles;
import at.a1ta.cuco.core.service.impl.MailService;
import at.a1ta.cuco.core.service.report.UserActionStatistics;
import at.a1ta.cuco.core.service.report.UserActionStatistics.ActionRecordStatistics;

@Profile(EnvironmentProfiles.UNTRUSTED)
@Component
public class DataTheftRapidAlertJob extends AbstractCronJob {

  private static final Logger logger = LoggerFactory.getLogger(DataTheftRapidAlertJob.class);

  private static final String REPORT_LINE = "<li>Benutzer {0} hat {1,number,#.##} Kunden aufgerufen. [Durchschnitt: {2,number,#.##} | Erlaubt: {3,number,#.##}]</li>";

  private UserTrackingService trackingService;
  private MailService mailService;

  @Value(value = "${data.theft.observation.period.in.days:14}")
  private int observationPeriod = 14;

  @Autowired
  public DataTheftRapidAlertJob(UserTrackingService trackingService, MailService mailService) {
    this.trackingService = trackingService;
    this.mailService = mailService;
  }

  @Override
  protected void process() {
    List<ActionRecordStatistics> potentialThreats = identifyPotentialThreats();
    reportThreatsToExecutives(potentialThreats);
  }

  private List<ActionRecordStatistics> identifyPotentialThreats() {
    List<UserActionRecord> referenceRecords = loadReferenceRecords();
    UserActionStatistics stats = new UserActionStatistics(referenceRecords);
    return stats.findSuspicious(loadCompareRecords());
  }

  void reportThreatsToExecutives(List<ActionRecordStatistics> potentialThreats) {
    if (CollectionUtils.isEmpty(potentialThreats)) {
      return;
    }
    String mailBody = prepareMessage(potentialThreats);
    sendMail(mailBody);
  }

  private String prepareMessage(List<ActionRecordStatistics> potentialThreats) {
    StringBuilder sb = new StringBuilder();
    Iterator<ActionRecordStatistics> it = potentialThreats.iterator();
    sb.append("<ul>");
    while (it.hasNext()) {
      ActionRecordStatistics ars = it.next();
      String line = MessageFormat.format(REPORT_LINE, ars.getActionRecord().getLogin(), ars.getActionCount(), ars.getMean(), ars.getAllowedMax());
      sb.append(line);
    }
    sb.append("</ul>");
    return sb.toString();
  }

  private void sendMail(String mailbody) {
    try {
      logger.info("Attempt sending Threat Report \r\n" + mailbody);
      mailService.sendThreatReportMail(mailbody);
    } catch (Exception e) {
      logger.error("Threat Report could not be sent.", e);
    }
  }

  private List<UserActionRecord> loadReferenceRecords() {
    TimeSpan span = TimeSpan.startingAt(LocalDate.now().minusDays(observationPeriod).toDate()).to(LocalDate.now().minusDays(1).toDate());
    return findCustomerLoadRecords(span);
  }

  private List<UserActionRecord> loadCompareRecords() {
    TimeSpan span = TimeSpan.startingAt(LocalDate.now().toDate()).toInfinite();
    return findCustomerLoadRecords(span);
  }

  private List<UserActionRecord> findCustomerLoadRecords(TimeSpan timeSpan) {
    return this.trackingService.findUserActionsForDateGroupByAction(timeSpan, UserRecordActionType.LOAD_CUSTO);
  }

  @Override
  protected String getJobId() {
    return ClassUtils.getShortNameAsProperty(this.getClass());
  }

}
