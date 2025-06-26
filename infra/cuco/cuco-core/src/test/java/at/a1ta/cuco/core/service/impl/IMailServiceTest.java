package at.a1ta.cuco.core.service.impl;

import java.util.Date;
import java.util.List;

import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.dao.db.SalesInfoDao;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.Task;

@Ignore("Integration Test without asserts")
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:testApplicationContext-cuco-core.xml"})
public class IMailServiceTest {

  @Autowired
  MailService mailService;

  @Autowired
  SalesInfoDao salesInfoDao;

  @Test
  public void sendTestMail() throws Exception {

    BiteUser assigneeUser = new BiteUser();
    assigneeUser.setUsername("q379421");

    Task task = new Task();
    task.setStartDate(new Date());
    task.setEndDate(new Date());
    task.setAssigneeUser(assigneeUser);

    SalesInfoNote siNote = new SalesInfoNote();
    siNote.setTask(task);
    siNote.setNoteText("Das ist der Note Text");
    siNote.setPartyId(103303208L);
    siNote.setSalesInfoNoteId(123L);
    siNote.setLastModificationUser(assigneeUser);

    mailService.sendVcalMail(siNote);
  }

  @Test
  public void sendTestMailNullComment() throws Exception {

    BiteUser assigneeUser = new BiteUser();
    assigneeUser.setUsername("q379421");

    Task task = new Task();
    task.setStartDate(new Date());
    task.setEndDate(new Date());
    task.setAssigneeUser(assigneeUser);

    SalesInfoNote siNote = new SalesInfoNote();
    siNote.setTask(task);
    siNote.setNoteText(null);
    siNote.setPartyId(103303208L);
    siNote.setSalesInfoNoteId(123L);
    siNote.setLastModificationUser(assigneeUser);

    mailService.sendVcalMail(siNote);
  }

  @Test
  public void testTaskMailJob() {
    sendTaskReminderMails();
  }

  private void sendTaskReminderMails() {
    List<SalesInfoNote> todaysNotes = salesInfoDao.getNotesForReminderMail();
    for (SalesInfoNote note : todaysNotes) {
      try {
        mailService.sendTaskReminderMail(note);
      } catch (Exception e) {
        // logger.error(e.getMessage(), e);
      }
    }
  }

}
