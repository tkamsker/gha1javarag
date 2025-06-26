package at.a1ta.cuco.core.service.impl;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.mail.Mail;
import at.a1ta.bite.core.mail.MailSender;
import at.a1ta.bite.core.server.dao.PersonDao;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.bite.core.shared.dto.cd.CdPerson;
import at.a1ta.bite.core.shared.util.CommonUtils;
import at.a1ta.cuco.core.service.POSService;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PointOfSaleInfo;
import at.a1ta.cuco.core.shared.dto.salesinfo.ToDoGroupNote;

@Service
public class POSServiceImpl implements POSService {
  private static final Logger logger = LoggerFactory.getLogger(POSServiceImpl.class);
  private static final Logger mailLogger = LoggerFactory.getLogger("mailings");
  @Autowired
  private MailSender mailSender;

  @Autowired
  private SettingService settingService;

  @Autowired
  private PersonDao personDao;

  @Override
  public void sendPOSChangeEmail(Party party, PointOfSaleInfo current, PointOfSaleInfo requested, String justification, UserInfo userInfo) {

    if (mailActivated()) {
      if (party == null || userInfo == null) {
        throw new RuntimeException("Party and/or UserInfo missing");
      }
      String template = mailTemplate();

      // [0] userId - fill in the CuCo logged in user
      // [1] userName - fill in the CuCo logged in user (lastname and firstname)
      // [2] partyId - fill in the current customer id
      // [3] partyName - fill in the last name, first name, company name of the customer
      // [4] currentDealerId - fill in the current dealer id of the customer
      // [5] currentDealerName - fill in the current dealer name of the customer
      // [6] suggestedDealerId - fill in the current dealer id of the customer (that has been selected in the popup)
      // [7] suggestedDealerName - fill in the current dealer name of the customer (that has been selected in the popup)
      // [8] reasonNote - fill in the given note of the textfield of the popup

      template = template.replace("[0]", userInfo.getUsername());
      template = template.replace("[1]", userInfo.getName());
      template = template.replace("[2]", "" + party.getId());
      template = template.replace("[3]", party.getName());
      template = template.replace("[4]", "" + current.getDealerId());
      template = template.replace("[5]", current.getDealerName());
      template = template.replace("[6]", "" + requested.getDealerId());
      template = template.replace("[7]", requested.getDealerName());
      template = template.replace("[8]", justification);

      Mail mail = new Mail();
      mail.setRecipients(mailAddresses());
      String executiveEmail = getExecutiveEmail(userInfo.getBiteUser());
      if (executiveEmail != null) {
        mail.setCc(new String[] {executiveEmail});
      } else {
        logger.warn("No Supervisor found for user " + userInfo.getUsername());
      }
      mail.setSubject(mailSubject());
      mail.setMessage(template);

      try {
        mailSender.sendMail(mail);
      } catch (Exception ex) {
        mailLogger.error(ex.getMessage(), ex);
        throw new RuntimeException(ex.getCause());
      }
    }

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

  private boolean mailActivated() {
    return settingService.getBooleanValue("mail.cuco.poschange.active", true);
  }

  private String mailSubject() {
    return settingService.getValue("mail.cuco.poschange.subject");
  }

  private String mailTemplate() {
    return settingService.getValue("mail.cuco.poschange.mail");
  }

  private String[] mailAddresses() {
    return settingService.getValuesIgnoreMissing("mail.cuco.poschange.adress");
  }

  @Override
  public void sendToDoAssignedToPOSEmail(Party party, ToDoGroupNote groupNote, PointOfSaleInfo requestedPOS, String justification, BiteUser user) {

    if (toDoAssignEmailActivated()) {
      try {
        if (party == null || user == null || requestedPOS == null || requestedPOS.getDelearEmailId() == null) {
          throw new RuntimeException("Required Details like Party(" + party + ")  and/or UserInfo(" + user + ") and/or POS (" + requestedPOS + ") Email Address("
              + (requestedPOS != null ? requestedPOS.getDelearEmailId() : "null") + ") Missing");
        }
        Mail mail = new Mail();
        mail.setRecipients(new String[] {requestedPOS.getDelearEmailId()});
        String executiveEmail = getExecutiveEmail(user);
        if (executiveEmail != null) {
          mail.setCc(new String[] {executiveEmail});
        } else {
          logger.warn("No Supervisor found for user " + user.getUsername());
        }
        mail.setSubject(toDoAssignMailSubject().replace("<CustomerNumber>", groupNote.getParty().getId() + ""));
        mail.setMessage(toDoAssignMailTemplate().replace("<CustomerNumber>", groupNote.getParty().getId() + "").replace("<CustomerName>", groupNote.getParty().getName())
            .replace("<Justification>", groupNote.getEmailAdditionalText()));

        mailSender.sendMail(mail);
        groupNote.setAssigneeNotes(CommonUtils.defaultString(groupNote.getAssigneeNotes()) + newLineBreak() + mail.getMessage().replaceAll("\\<.*?>", "") + newLineBreak());
      } catch (Exception ex) {
        mailLogger.error("Error while Sending ToDoAssignment Email for note ID  " + groupNote.getPredecessorSalesInfoNoteId() + " , party Id " + groupNote.getPartyId(), ex);
        groupNote.setAssigneeNotes(CommonUtils.defaultString(groupNote.getAssigneeNotes()) + newLineBreak()
            + getFailureMessage().replace("<DelearNameAddress>", groupNote.getAssignedToDelearInfo().getNameAddressString()) + newLineBreak());

      }
    }

  }

  @Override
  public void sendToDoCompletedToPOSEmail(Party party, ToDoGroupNote groupNote, PointOfSaleInfo requestedPOS, String justification, BiteUser user) {

    if (toDoCompletedEmailActivated()) {
      try {
        if (party == null || user == null || groupNote.getCreationUser() == null || groupNote.getCreationUser().getEmail() == null || groupNote.getCreationUser().getEmail().isEmpty()) {
          throw new RuntimeException("Required Details like Party (" + party + ") and/or UserInfo (" + user + ") and/or Creator (" + groupNote.getCreationUser() + ") Email Address ("
              + groupNote.getCreationUser().getEmail() + ") Missing");
        }
        Mail mail = new Mail();
        mail.setRecipients(new String[] {groupNote.getCreationUser().getEmail()});
        String executiveEmail = getExecutiveEmail(user);
        if (executiveEmail != null) {
          mail.setCc(new String[] {executiveEmail});
        } else {
          logger.warn("No Supervisor found for user " + user.getUsername());
        }
        mail.setSubject(toDoCompletedMailSubject().replace("<CustomerNumber>", groupNote.getParty().getId() + ""));
        mail.setMessage(toDoCompletedMailTemplate().replace("<CustomerNumber>", groupNote.getParty().getId() + "").replace("<CustomerName>", groupNote.getParty().getName())
            .replace("<Justification>", groupNote.getEmailAdditionalText()));

        mailSender.sendMail(mail);
        groupNote.setAssigneeNotes(CommonUtils.defaultString(groupNote.getAssigneeNotes()) + newLineBreak() + mail.getMessage().replaceAll("\\<.*?>", "") + newLineBreak());
      } catch (Exception ex) {
        mailLogger.error("Error while Sending ToDoCompletion Email for note ID  " + groupNote.getPredecessorSalesInfoNoteId() + " , party Id " + groupNote.getPartyId(), ex);
        groupNote.setAssigneeNotes(CommonUtils.defaultString(groupNote.getAssigneeNotes())
            + newLineBreak()
            + getFailureMessage().replace("<DelearNameAddress>",
                (groupNote.getAssignedToDelearInfo() != null ? groupNote.getAssignedToDelearInfo().getNameAddressString() : "delear id-" + groupNote.getAssigneeDealerId())) + newLineBreak());

      }
    }

  }

  private String newLineBreak() {
    return "\n===========================================\n";
  }

  private boolean toDoAssignEmailActivated() {
    return settingService.getBooleanValue("mail.cuco.assignToDo.mail.active", true);
  }

  private String toDoAssignMailTemplate() {
    return settingService.getValue("mail.cuco.assignToDo.mail_template");
  }

  private String toDoAssignMailSubject() {
    return settingService.getValue("mail.cuco.assignToDo.mail_subject");
  }

  private boolean toDoCompletedEmailActivated() {
    return settingService.getBooleanValue("mail.cuco.toDoCompleted.mail.active", true);
  }

  private String toDoCompletedMailTemplate() {
    return settingService.getValue("mail.cuco.toDoCompleted.mail_template");
  }

  private String toDoCompletedMailSubject() {
    return settingService.getValue("mail.cuco.toDoCompleted.mail_subject");
  }

  private String getFailureMessage() {
    // TODO Auto-generated method stub
    return settingService.getValue("mail.cuco.assignToDo.mail_failureMessageInNotes");
  }

}
