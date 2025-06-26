package at.a1ta.cuco.core.service.cron;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import at.a1ta.bite.core.server.cron.AbstractCronJob;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.EnvironmentProfiles;
import at.a1ta.cuco.core.dao.db.SalesInfoDao;
import at.a1ta.cuco.core.service.impl.MailService;
import at.a1ta.cuco.core.shared.dto.salesinfo.CompetitorNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;

@Profile(EnvironmentProfiles.TRUSTED)
@Component
public class SalesInfoReminderMailJob extends AbstractCronJob {

  private static final Logger logger = LoggerFactory.getLogger("mailings");

  @Autowired
  private SalesInfoDao salesInfoDao;

  @Autowired
  private MailService ms;

  @Autowired
  private SettingService settingService;

  @Override
  protected void process() {
    sendBindingPeriodReminderMails();
    sendTaskReminderMails();
    sendSalesConvNotesForReminderMail();
  }

  private void sendBindingPeriodReminderMails() {
    long numDays;
    String valueOrDefault = settingService.getValueOrDefault("binding.period.num.days", "90");
    try {
      numDays = Long.parseLong(valueOrDefault);
    } catch (NumberFormatException n) {
      numDays = 90L;
    }
    List<CompetitorNote> todaysNotes = salesInfoDao.getNotesForBindingPeriodReminderMail(numDays);
    for (CompetitorNote note : todaysNotes) {
      try {
        ms.sendBindingPeriodReminderMail(note);
      } catch (Exception e) {
        logger.error(e.getMessage(), e);
      }
    }

  }

  private void sendSalesConvNotesForReminderMail() {
    List<SalesInfoNote> todaysNotes = salesInfoDao.getSalesConvNotesForReminderMail();
    for (SalesInfoNote note : todaysNotes) {
      try {
        ms.sendSalesConvReminderMail(note);
      } catch (Exception e) {
        logger.error(e.getMessage(), e);
      }
    }
  }

  private void sendTaskReminderMails() {
    List<SalesInfoNote> todaysNotes = salesInfoDao.getNotesForReminderMail();
    for (SalesInfoNote note : todaysNotes) {
      try {
        ms.sendTaskReminderMail(note);
      } catch (Exception e) {
        logger.error(e.getMessage(), e);
      }
    }
  }

  @Override
  protected String getJobId() {
    return "salesInfoReminderMail";
  }
}
