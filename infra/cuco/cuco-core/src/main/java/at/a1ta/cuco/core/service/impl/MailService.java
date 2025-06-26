package at.a1ta.cuco.core.service.impl;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.TimeZone;

import org.apache.commons.lang.ArrayUtils;
import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

import at.a1ta.bite.core.mail.Mail;
import at.a1ta.bite.core.mail.MailSender;
import at.a1ta.bite.core.server.dao.PersonDao;
import at.a1ta.bite.core.server.exception.MissingSettingException;
import at.a1ta.bite.core.server.service.LocalSettingService;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.core.shared.dto.cd.CdPerson;
import at.a1ta.cuco.core.dao.db.PartyDao;
import at.a1ta.cuco.core.dao.db.SalesInfoDao;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.salesinfo.CompetitorNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;

/**
 * This class contains all functions for sending email to users
 * 
 * @author Rene Weidinger
 * @version 1.0
 */
@Component
public class MailService {

  private static final String THREAT_REPORT_MAIL_DEFAULT_HEADER = "Folgende Nutzer haben sich entgegen ihren Gewohnheiten verhalten:\r\n";

  private static final String THREAT_REPORT_MAIL_DEFAULT_FOOTER = "Automatisch generierte Mail, basierend auf einer Auswertung der letzten 14 Tage.";

  private static final String THREAT_REPORT_MAIL_DEFAULT_SUBJECT = "[CuCo]: Potential Data Theft Alert";

  private static final Logger mailLogger = LoggerFactory.getLogger("mailings");

  public static final String KEIN_BE = "Kein Be";

  private static SimpleDateFormat iCalendarDateFormat = new SimpleDateFormat("yyyyMMdd'T'HHmm00'Z'");
  private static SimpleDateFormat bindingDateFormat = new SimpleDateFormat("dd.MM.yyyy");

  private SettingService settingService;

  private LocalSettingService localSettingService;

  private PartyDao partyDao;

  private PersonDao personDao;

  private MailSender mailSender;

  private SalesInfoDao salesInfoDao;

  public void sendBindingPeriodReminderMail(CompetitorNote cpNote) throws Exception {
    mailLogger.debug("Send binding period reminder mail for SalesInfoNote: " + cpNote.getSalesInfoNoteId());
    Mail mail = prepareBindingPeriodEmail(cpNote);
    if (mail != null) {
      mailSender.sendMail(mail);
    }

    cpNote.setReminderMailSentDate(new Date());
    salesInfoDao.updateBindingPeriodReminderMailSentDate(cpNote);
  }

  public void sendTaskReminderMail(SalesInfoNote siNote) throws Exception {
    mailLogger.debug("Send task reminder mail for SalesInfoNote: " + siNote.toString());
    Mail mail = prepareTaskEmail(siNote);
    mailSender.sendMail(mail);

    siNote.getTask().setReminderMailSentDate(new Date());
    salesInfoDao.updateTaskReminderMailSentDate(siNote.getTask());
  }

  public void sendVcalMail(SalesInfoNote siNote) throws Exception {
    mailLogger.debug("Send Vcal mail for SalesInfoNote: " + siNote.getSalesInfoNoteId());
    Mail mail = prepareTaskEmail(siNote);
    mail = addVcalInvite(mail, siNote);
    mailSender.sendMail(mail);

    siNote.getTask().setvCalMailSentDate(new Date());
    siNote.getTask().setvCalMailTo(StringUtils.join(mail.getRecipients(), ";"));
    siNote.getTask().setvCalMailCC(StringUtils.join(mail.getCc(), ";"));
    salesInfoDao.updateTaskVcalMailSentInfo(siNote.getTask());
  }

  public void sendVcalCancelMail(SalesInfoNote siNote) throws Exception {
    mailLogger.debug("Send Vcal cancel mail for SalesInfoNote: " + siNote.getSalesInfoNoteId());
    Mail mail = prepareTaskEmail(siNote);
    if (mail != null) {
      mail = setPreviousRecipients(siNote, mail);
      mail = addVcalCancel(mail, siNote);
      mailSender.sendMail(mail);
    }
  }

  public void sendSalesConvReminderMail(SalesInfoNote siNote) throws Exception {
    mailLogger.debug("Send reminder mail for SalesConvNote: " + siNote.getSalesInfoNoteId());
    Mail mail = prepareSalesConvEmail(siNote);
    mailSender.sendMail(mail);

    salesInfoDao.updateLastReminderMailSentDateForSalesConvNote(siNote.getSalesInfoNoteId());
  }

  private Mail setPreviousRecipients(SalesInfoNote siNote, Mail mail) {
    if (siNote.getTask().getvCalMailTo() != null) {
      String[] recipients = StringUtils.split(siNote.getTask().getvCalMailTo(), ";");
      mail.setRecipients(recipients);
    }
    if (siNote.getTask().getvCalMailCC() != null) {
      String[] cc = StringUtils.split(siNote.getTask().getvCalMailCC(), ";");
      mail.setCc(cc);
    }

    return mail;
  }

  private Mail prepareSalesConvEmail(SalesInfoNote siNote) {
    Party party = partyDao.loadParty(siNote.getPartyId());
    if (party == null) {
      mailLogger.error("Party is null for party id " + siNote.getPartyId() + " and si note id " + siNote.getSalesInfoNoteId() + " , cannot send email!");
      return null;
    }

    StringBuilder text = prepareSalesConvMailText(party, siNote.getLastModificationUser());
    Mail mail = new Mail();

    setSalesConvMailRecipients(siNote.getLastModificationUser(), mail);
    if (ArrayUtils.isEmpty(mail.getRecipients())) {
      return null;
    }
    mail.setSubject(readSetting("salesconv.mail.reminder.subject") + " " + siNote.getPartyId());
    mail.setMessage(text.toString());

    mailLogger.info("real mail recipient: " + ArrayUtils.toString(mail.getRecipients()));
    if (mail.getCc() != null) {
      mailLogger.info("real mail cc: " + ArrayUtils.toString(mail.getCc()));
    }
    return mail;
  }

  private Mail prepareTaskEmail(SalesInfoNote siNote) {
    Party party = partyDao.loadParty(siNote.getPartyId());
    if (party == null) {
      mailLogger.error("Party is null for party id " + siNote.getPartyId() + " and si note id " + siNote.getSalesInfoNoteId() + " , cannot send email!");
      return null;
    }
    if (siNote.getTask().getAssigneeUser() == null) {
      mailLogger.error(
          "Assignee user is null for party id " + siNote.getPartyId() + " and si note id " + siNote.getSalesInfoNoteId() + " ,task id is " + siNote.getTask().getTaskId() + ", cannot send email!");
      return null;
    }

    String productGroup = "KUNDENNOTIZ";
    String comment = siNote.getNoteText();

    StringBuilder text = prepareTaskMailText(productGroup, comment, party, siNote.getLastModificationUser());
    Mail mail = new Mail();

    setMailRecipientsForTasks(party, siNote.getTask().getAssigneeUser(), siNote.getLastModificationUser(), mail);
    if (ArrayUtils.isEmpty(mail.getRecipients())) {
      complementAlternateRecipients(mail);
      complementAlternateMessage(text);
    }
    mail.setSubject(readSetting("mail.reminder.subject") + " " + siNote.getPartyId());
    mail.setMessage(text.toString());

    mailLogger.info("real mail recipient: " + ArrayUtils.toString(mail.getRecipients()));
    if (mail.getCc() != null) {
      mailLogger.info("real mail cc: " + ArrayUtils.toString(mail.getCc()));
    }
    return mail;
  }

  private Mail prepareBindingPeriodEmail(CompetitorNote cpNote) {
    Party party = partyDao.loadParty(cpNote.getPartyId());
    if (party == null) {
      mailLogger.error("Can't send mail for unknown partyId: " + cpNote.getPartyId());
      return null;
    }

    CdPerson secondaryReceiver = personDao.getPerson(cpNote.getLastModificationUser().getUsername());

    StringBuilder text = prepareBindingPeriodMailText(cpNote, party, secondaryReceiver);
    Mail mail = new Mail();

    setMailRecipientsForBindingPeriodReminder(party, secondaryReceiver, mail);
    if (ArrayUtils.isEmpty(mail.getRecipients())) {
      complementAlternateRecipients(mail);
      complementAlternateMessage(text);
    }
    mail.setSubject(readSetting("binding.period.mail.reminder.subject"));
    mail.setMessage(text.toString());

    mailLogger.info("real mail recipient: " + ArrayUtils.toString(mail.getRecipients()));
    if (mail.getCc() != null) {
      mailLogger.info("real mail cc: " + ArrayUtils.toString(mail.getCc()));
    }
    return mail;
  }

  private Mail addVcalInvite(Mail mail, SalesInfoNote siNote) {
    mail.setvCalendarContent(createVcalMessage(mail, siNote, VcalType.INVITE));
    return mail;
  }

  private Mail addVcalCancel(Mail mail, SalesInfoNote siNote) {
    mail.setvCalendarContent(createVcalMessage(mail, siNote, VcalType.CANCEL));
    return mail;
  }

  public void sendThreatReportMail(String message) throws Exception {
    Mail mail = prepareThreatReportMail(message);
    mailSender.sendMail(mail);
  }

  private Mail prepareThreatReportMail(String message) {
    Mail mail = new Mail();
    addRecipientsToThreatReportMail(mail);
    mail.setSubject(settingService.getValueOrDefault("data.theft.alert.mail.subject", THREAT_REPORT_MAIL_DEFAULT_SUBJECT));
    mail.setMessage(assembleThreatReportMailBody(message));
    return mail;
  }

  private void addRecipientsToThreatReportMail(Mail mail) {
    mail.setRecipients(settingService.getValuesIgnoreMissing("data.theft.alert.mail.to"));
    mail.setCc(settingService.getValuesIgnoreMissing("data.theft.alert.mail.cc"));
    mail.setBcc(settingService.getValuesIgnoreMissing("data.theft.alert.mail.bcc"));
  }

  private String assembleThreatReportMailBody(String message) {
    StringBuilder mailText = new StringBuilder(settingService.getValueOrDefault("data.theft.alert.mail.header", THREAT_REPORT_MAIL_DEFAULT_HEADER));
    mailText.append(message);
    mailText.append(settingService.getValueOrDefault("data.theft.alert.mail.footer", THREAT_REPORT_MAIL_DEFAULT_FOOTER));
    mailText.append("<br /><span style=\"font-size: 75%\">" + new Date().toString() + "</span>");
    return mailText.toString();
  }

  private StringBuilder prepareTaskMailText(String productGroup, String comment, Party party, BiteUser secondaryReciever) {
    StringBuilder text = new StringBuilder();
    appendhead(text);
    appendBody(productGroup, comment, party, secondaryReciever, text);
    appendfoot(text);
    return text;
  }

  private StringBuilder prepareSalesConvMailText(Party party, BiteUser secondaryReciever) {
    StringBuilder text = new StringBuilder();
    appendhead(text);
    appendBodySalesConv(party, secondaryReciever, text);
    appendfoot(text);
    return text;
  }

  private void appendBodySalesConv(Party party, BiteUser secondaryReciever, StringBuilder text) {
    StringBuffer name = createCustomerName(party);
    String street = party.getStreet() + " " + party.getHousenumber();
    String city = party.getPoBox() + " " + party.getCity();

    mailLogger.debug(localSettingService.getValue("app_url"));

    String link = localSettingService.getValue("app_url") + "?customerId=" + party.getId() + "&screen=salesInfo";

    String body = readSetting("salesconv.mail.reminder.text");
    body = body.replace("[0]", nonNull(name.toString()));
    body = body.replace("[1]", nonNull(street));
    body = body.replace("[2]", nonNull(city));
    body = body.replace("[6]", nonNull(link));
    text.append(body);
  }

  private StringBuilder prepareBindingPeriodMailText(CompetitorNote siNote, Party party, CdPerson creatorUser) {

    StringBuilder text = new StringBuilder();
    appendBindingPeriodHead(text);
    appendBindingPeriodBody(siNote, party, text);
    appendBindingPeriodFoot(text);
    return text;
  }

  private void appendBindingPeriodHead(StringBuilder buf) {
    buf.append(readSetting("binding.period.mail.header"));
  }

  private void appendBindingPeriodBody(CompetitorNote cpNote, Party party, StringBuilder text) {
    StringBuffer name = createCustomerName(party);
    String street = party.getStreet() + " " + party.getHousenumber();
    String city = party.getPoBox() + " " + party.getCity();

    mailLogger.debug(localSettingService.getValue("app_url"));

    String link = localSettingService.getValue("app_url") + "?customerId=" + party.getId();

    String body = readSetting("binding.period.mail.reminder.text");
    body = body.replace("[0]", bindingDateFormat.format(cpNote.getBindingDate()));
    body = body.replace("[1]", cpNote.getName() == null ? "" : cpNote.getName());
    body = body.replace("[2]", name == null ? "" : name.toString());
    body = body.replace("[3]", street);
    body = body.replace("[4]", city);
    body = body.replace("[5]", link);
    text.append(body);
  }

  private void appendBindingPeriodFoot(StringBuilder buf) {
    buf.append(readSetting("binding.period.mail.footer"));
  }

  private void complementAlternateMessage(StringBuilder text) {
    text.insert(0, readSetting("mail.reminder.alternatetext"));
  }

  private void complementAlternateRecipients(Mail mail) {
    mail.setRecipients(readSetting("mail.reminder.alternateteams").split(";"));
  }

  private void setMailRecipientsForBindingPeriodReminder(Party party, CdPerson secondaryReceiver, Mail mail) {
    String email = null;
    String cc = null;

    mailLogger.debug(party.getSupportUserId());
    if (KEIN_BE.equals(party.getSupportUserId())) {
      email = StringUtils.trimToNull(secondaryReceiver.getEmail());
      if (email != null && secondaryReceiver.getExecutive() != null) {
        cc = personDao.getPerson(secondaryReceiver.getExecutive()).getEmail();
      }
    } else {
      CdPerson supporter = personDao.getPerson(party.getSupportUserId());
      email = StringUtils.trimToNull(supporter.getEmail());
      if (email != null && supporter.getExecutive() != null) {
        cc = personDao.getPerson(supporter.getExecutive()).getEmail();
      }
    }

    mail.setRecipients((email == null) ? null : new String[] {email});
    mail.setCc((cc == null) ? null : new String[] {cc});
  }

  private void setSalesConvMailRecipients(BiteUser primaryReceiver, Mail mail) {
    String email = null;
    String cc = null;

    if (primaryReceiver != null && primaryReceiver.getEmail() != null) {
      email = primaryReceiver.getEmail();
      if (email != null) {
        cc = getExecutiveEmail(primaryReceiver);
      }
    }

    mail.setRecipients((email == null) ? null : new String[] {email});
    mail.setCc((cc == null) ? null : new String[] {cc});
  }

  private void setMailRecipientsForTasks(Party party, BiteUser primaryReceiver, BiteUser secondaryReceiver, Mail mail) {
    String email = null;
    String cc = null;

    if (primaryReceiver != null && primaryReceiver.getEmail() != null) {
      email = primaryReceiver.getEmail();
      if (email != null) {
        cc = getExecutiveEmail(primaryReceiver);
      }
    } else {
      if (KEIN_BE.equals(party.getSupportUserId())) {
        email = secondaryReceiver.getEmail();
        if (email != null) {
          cc = getExecutiveEmail(secondaryReceiver);
        }
      } else {
        CdPerson supporter = personDao.getPerson(party.getSupportUserId());
        email = StringUtils.trimToNull(supporter.getEmail());
        if (email != null && supporter.getExecutive() != null) {
          cc = personDao.getPerson(supporter.getExecutive()).getEmail();
        }
      }
    }

    mail.setRecipients((email == null) ? null : new String[] {email});
    mail.setCc((cc == null) ? null : new String[] {cc});
  }

  private String getExecutiveEmail(BiteUser user) {
    if (user.isPartnerCenterUser()) {
      return null;
    }
    CdPerson person = personDao.getPerson(user.getUsername());
    if (person.getExecutive() != null) {
      return personDao.getPerson(person.getExecutive()).getEmail();
    }
    return null;
  }

  private void appendBody(String productGroup, String comment, Party party, BiteUser secondaryReciever, StringBuilder text) {
    StringBuffer name = createCustomerName(party);
    String street = party.getStreet() + " " + party.getHousenumber();
    String city = party.getPoBox() + " " + party.getCity();
    String creator = secondaryReciever.getName();

    mailLogger.debug(localSettingService.getValue("app_url"));

    String link = localSettingService.getValue("app_url") + "?customerId=" + party.getId();

    String body = readSetting("mail.reminder.text");
    body = body.replace("[0]", nonNull(name.toString()));
    body = body.replace("[1]", nonNull(street));
    body = body.replace("[2]", nonNull(city));
    body = body.replace("[3]", nonNull(productGroup));
    body = body.replace("[4]", nonNull(comment));
    body = body.replace("[5]", nonNull(creator));
    body = body.replace("[6]", nonNull(link));
    text.append(body);
  }

  private String nonNull(String str) {
    return str == null ? "" : str;
  }

  private enum VcalType {
    INVITE, CANCEL
  }

  public String createVcalMessage(Mail mail, SalesInfoNote siNote, VcalType type) {

    // mailsender alters the recipient & CC, therefore get the altered list
    String from = mailSender.determineSenderAddress();
    String[] realRecipients = mailSender.getRealRecipients(mail);
    String[] realCCs = mailSender.getRealCC(mail);

    Date start = siNote.getTask().getStartDate();
    iCalendarDateFormat.setTimeZone(TimeZone.getTimeZone("UTC"));

    Date end = siNote.getTask().getEndDate();

    // check the icalendar spec in order to build a more complicated meeting request
    StringBuilder calendarContent = new StringBuilder();
    calendarContent.append("BEGIN:VCALENDAR\n");

    if (type == VcalType.INVITE) {
      calendarContent.append("METHOD:REQUEST\n");
    } else if (type == VcalType.CANCEL) {
      calendarContent.append("METHOD:CANCEL\n");
      calendarContent.append("STATUS:CANCELLED\n");
    }
    calendarContent.append("PRODID:A1\n");
    calendarContent.append("VERSION:2.0\n");
    calendarContent.append("BEGIN:VEVENT\n");
    calendarContent.append("DTSTAMP:" + iCalendarDateFormat.format(new Date()) + "\n");
    if (start != null) {
      calendarContent.append("DTSTART:" + iCalendarDateFormat.format(start) + "\n");
    }
    if (end != null) {
      calendarContent.append("DTEND:" + iCalendarDateFormat.format(end) + "\n");
    }
    calendarContent.append("SUMMARY:" + readSetting("mail.reminder.subject") + " " + siNote.getPartyId() + "\n");
    calendarContent.append("UID:" + siNote.getSalesInfoNoteId() + "\n");
    for (String cc : realCCs) {
      calendarContent.append("ATTENDEE;ROLE=NON-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE:MAILTO:" + cc + "\n");
    }
    for (String to : realRecipients) {
      calendarContent.append("ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE:MAILTO:" + to + "\n");
    }
    calendarContent.append("ORGANIZER:MAILTO:" + from + "\n");
    calendarContent.append("LOCATION:-\n");
    calendarContent.append("DESCRIPTION:TODO\n");
    calendarContent.append("SEQUENCE:0\n");
    calendarContent.append("PRIORITY:5\n" + "CLASS:PUBLIC\n");
    calendarContent.append("STATUS:CONFIRMED\n");
    calendarContent.append("TRANSP:OPAQUE\n");
    calendarContent.append("BEGIN:VALARM\n");
    calendarContent.append("ACTION:DISPLAY\n");
    calendarContent.append("DESCRIPTION:REMINDER\n");
    calendarContent.append("TRIGGER;RELATED=START:-PT00H15M00S\n");
    calendarContent.append("END:VALARM\n");
    calendarContent.append("END:VEVENT\n");
    calendarContent.append("END:VCALENDAR");

    return calendarContent.toString();
  }

  /**
   * reads the setting with the key.
   * 
   * @param setting key
   * @throws MissingSettingException if the setting is missing.
   */
  private String readSetting(String settingKey) {
    String value = settingService.getValue(settingKey);
    if (value == null) {
      throw new MissingSettingException(settingKey);
    }
    return value;
  }

  private void appendhead(StringBuilder buf) {
    buf.append(readSetting("mail.header"));
  }

  private void appendfoot(StringBuilder buf) {
    buf.append(readSetting("mail.footer"));
  }

  private StringBuffer createCustomerName(Party c) {
    StringBuffer name = new StringBuffer();
    if (c.getSalutation() != null) {
      name.append(c.getSalutation());
      name.append(" ");
    }
    if (c.getFirstname() != null) {
      name.append(c.getFirstname());
      name.append(" ");
    }
    name.append(c.getLastname());
    return name;
  }

  @Autowired
  @Qualifier("cucoCustomerDao")
  public void setPartyDao(PartyDao partyDao) {
    this.partyDao = partyDao;
  }

  @Autowired
  public void setPersonDao(PersonDao personDao) {
    this.personDao = personDao;
  }

  @Autowired
  public void setSettingService(SettingService settingService) {
    this.settingService = settingService;
  }

  @Autowired
  public void setLocalSettingService(LocalSettingService localSettingService) {
    this.localSettingService = localSettingService;
  }

  @Autowired
  public void setMailSender(MailSender mailSender) {
    this.mailSender = mailSender;
  }

  @Autowired
  public void setSalesInfoDao(SalesInfoDao salesInfoDao) {
    this.salesInfoDao = salesInfoDao;
  }
}
