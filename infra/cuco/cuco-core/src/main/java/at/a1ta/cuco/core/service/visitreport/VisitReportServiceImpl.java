package at.a1ta.cuco.core.service.visitreport;

import java.io.File;
import java.io.IOException;
import java.io.StringReader;
import java.io.StringWriter;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Marshaller;
import javax.xml.bind.Unmarshaller;

import org.apache.commons.codec.binary.Base64;
import org.apache.commons.io.FileUtils;
import org.apache.xmlbeans.XmlException;
import org.joda.time.DateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import org.springframework.util.SerializationUtils;

import com.google.gson.Gson;
import com.telekomaustriagroup.esb.cuscocustomercontact.ErrorMessage;

import at.a1ta.bite.core.server.service.LocalSettingService;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.AuthorityHelper;
import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.bite.data.cusco.CusCoConfigurtationBean;
import at.a1ta.bite.data.cusco.CusCoMessage;
import at.a1ta.bite.data.cusco.CusCoMessageBuilder;
import at.a1ta.bite.data.cusco.service.CuscoCustomerContactService;
import at.a1ta.cuco.core.dao.db.AttributeDao;
import at.a1ta.cuco.core.dao.db.impl.PartyDaoImpl;
import at.a1ta.cuco.core.dao.db.visitreport.VisitReportDao;
import at.a1ta.cuco.core.service.POSService;
import at.a1ta.cuco.core.service.SalesInfoService;
import at.a1ta.cuco.core.service.impl.MailService;
import at.a1ta.cuco.core.service.impl.NoteMailHelper;
import at.a1ta.cuco.core.shared.dto.Attribute;
import at.a1ta.cuco.core.shared.dto.AttributeConfig;
import at.a1ta.cuco.core.shared.dto.AttributeConfig.Groupings;
import at.a1ta.cuco.core.shared.dto.Auth;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.SalesConvEmailData;
import at.a1ta.cuco.core.shared.dto.salesinfo.AppointmentNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.CompetitorNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.HistoryNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.HistoryNote.HistoryLevel;
import at.a1ta.cuco.core.shared.dto.salesinfo.HistoryNote.HistoryTitle;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote.SalesInfoNoteType;
import at.a1ta.cuco.core.shared.dto.salesinfo.SimpleNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.Task;
import at.a1ta.cuco.core.shared.dto.salesinfo.Task.TaskStatus;
import at.a1ta.cuco.core.shared.dto.salesinfo.ToDoGroupNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.VisitReportSuccessorExistsException;
import at.a1ta.cuco.core.shared.dto.salesinfo.salesconvnote.ProductHistoryItem;
import at.a1ta.cuco.core.shared.dto.salesinfo.salesconvnote.SalesConvNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.DigitalSellingNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.generic.FileAttachment;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.generic.GenericNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSOrgUnit;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSProduct;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSProductNote;
import net.sf.jasperreports.engine.JRException;
import net.sf.jasperreports.engine.JasperPrint;

@Service
public class VisitReportServiceImpl implements VisitReportService {

  private static final String OUTPUT_CHANNEL_EMAIL = "Email";
  private static final String SOURCE_SYSTEM_CUCO = "CuCo";
  private static final String DUMMY_PSWD = "no-password";

  public static final String noteAttachmentTemplateName = "salesInfo.note.attachment.template.name";
  public static final String noteAttachmentTemplate = "salesInfo.note.attachment.template";
  public static final String noteAttachmentTemplateAttachments = "salesInfo.note.attachment.template.attachments";
  private final static Logger logger = LoggerFactory.getLogger(VisitReportServiceImpl.class);
  private final Gson gson = new Gson();

  @Autowired
  private VisitReportDao visitReportDao;

  @Autowired
  private AttributeDao attributeDao;

  @Autowired
  private SalesInfoService salesInfoService;

  @Autowired
  private LocalSettingService localSettingService;

  @Autowired
  private SettingService settingService;

  @Autowired
  @Qualifier("cucoCustomerDao")
  PartyDaoImpl partyDao;

  @Autowired
  MailService mailService;

  @Autowired
  POSService posService;

  @Autowired
  CuscoCustomerContactService cuscoCustomerContactService;

  @Autowired
  VisitReportPrintService visitReportPrintService;

  @Override
  public Collection<SBSProduct> getSBSProducts() {
    return visitReportDao.loadSBSProducts(SalesInfoNoteType.SI_VR_SBS_PRODUCT_NOTE);
  }

  @Override
  public Collection<SBSProduct> getAllSBSProducts() {
    return visitReportDao.loadAllSBSProducts();
  }

  @Override
  public Collection<SBSProduct> getSalesConvProducts() {
    return visitReportDao.loadSBSProducts(SalesInfoNoteType.SI_SALES_CONV_PRODUCT_NOTE);
  }

  @Override
  public GenericNote getGenericNoteByNoteId(long noteId) {
    GenericNote note = visitReportDao.loadGenericNoteByNoteId(noteId);
    note.setParty(partyDao.loadParty(note.getPartyId()));
    return note;
  }

  @Override
  public SBSNote getSBSNoteByNoteId(long noteId) {
    SBSNote note = visitReportDao.loadSBSNoteByNoteId(noteId, settingService.getBooleanValue("salesInfo.note.visitReport.experimentalQueryActive", false));

    note.setParty(partyDao.loadParty(note.getPartyId()));

    ArrayList<SalesInfoNote> tasks = new ArrayList<SalesInfoNote>();
    for (SalesInfoNote task : note.getTasks()) {
      switch (task.getSalesInfoNoteType()) {
        case SI_COMPETITOR_NOTE:
          tasks.add(salesInfoService.getCompetitorNoteByNoteId(task.getSalesInfoNoteId()));
          break;
        case SI_SIMPLE_NOTE:
          tasks.add(salesInfoService.getSimpleNoteByNoteId(task.getSalesInfoNoteId()));
          break;
        default:
          break;
      }
    }
    note.setTasks(tasks);

    ArrayList<AppointmentNote> appointments = new ArrayList<AppointmentNote>();

    for (SalesInfoNote task : note.getAppointments()) {
      switch (task.getSalesInfoNoteType()) {
        case SI_APPOINTMENT_NOTE:
          appointments.add(salesInfoService.getAppointmentNoteByNoteId(task.getSalesInfoNoteId()));
          break;
        default:
          break;
      }
    }
    note.setAppointments(appointments);
    SBSNote savedNoteInstance = new SBSNote();
    try {
      savedNoteInstance = (SBSNote) SerializationUtils.deserialize(SerializationUtils.serialize(note));
    } catch (Exception e) {
      logger.warn("Error while cloaning SBS Note", e);
    } finally {
      note.setSavedInstance(savedNoteInstance);
    }
    return note;
  }

  @Override
  public Collection<Attribute> getSBSNoteTemplateReflection() {
    return visitReportDao.loadSalesInfoAttributesByGrouping(AttributeConfig.Groupings.VISITREPORT_SBS_REFLECTION.name());
  }

  @Override
  public Collection<Attribute> getSBSNoteTemplateFeedback() {
    return visitReportDao.loadSalesInfoAttributesByGrouping(AttributeConfig.Groupings.VISITREPORT_SBS_FEEDBACK.name());
  }

  @Override
  public Collection<Attribute> getSalesConvNoteTemplateFeedback() {
    return visitReportDao.loadSalesInfoAttributesByGrouping(AttributeConfig.Groupings.VISITREPORT_SALES_CONV_FEEDBACK.name());
  }

  @Override
  public ArrayList<Attribute> getToDoGroupNoteTemplateToDos() {
    return new ArrayList<Attribute>(visitReportDao.loadSalesInfoAttributesByGrouping(AttributeConfig.Groupings.VISITREPORT_SBS_TODO_ITEM.name()));
  }

  @Override
  public void saveGenericNote(GenericNote note, String attachmentsFolderName) {
    if (note.getSalesInfoNoteId() == -1) {
      insertGenericNote(note, attachmentsFolderName);
    } else {
      updateGenericNote(note);
    }
  }

  private void insertGenericNote(GenericNote note, String attachmentsFolderName) {
    salesInfoService.insertSalesInfoNote(note);
    visitReportDao.insertGenericNote(note);
    for (FileAttachment attachment : note.getFileAttachments()) {
      attachment.setSalesInfoNoteId(note.getSalesInfoNoteId());
      visitReportDao.insertFileAttachment(attachment);
    }
    File tempLocation = new File(getTempUploadPath(attachmentsFolderName));
    File newLocation = new File(getUploadPath(note.getSalesInfoNoteId()));
    try {
      FileUtils.moveDirectory(tempLocation, newLocation);
    } catch (Exception e) {
    }

    if (note.getPredecessorSalesInfoNoteId() != null) {
      updateOriginalGenericNote(note);
    }
  }

  @Override
  public void saveQuotePdfAsFileAttachment(String fileName, byte[] quotePdfBytes, long salesConvNoteId, BiteUser currentUser) throws IOException {

    File quotePdf = new File(getUploadPath(salesConvNoteId) + fileName);

    byte[] decodeBase64 = Base64.decodeBase64(quotePdfBytes);

    FileUtils.writeByteArrayToFile(quotePdf, decodeBase64);

    FileAttachment attachment = new FileAttachment();
    attachment.setCreationTimestamp(new Date());
    attachment.setCreationUser(currentUser);
    attachment.setFileName(fileName);
    attachment.setSalesInfoNoteId(salesConvNoteId);

    visitReportDao.insertFileAttachment(attachment);
  }

  private void updateOriginalGenericNote(GenericNote note) {
    GenericNote predecessor = getGenericNoteByNoteId(note.getPredecessorSalesInfoNoteId());
    if (predecessor != null && !predecessor.isDeleted()) {
      for (FileAttachment attachment : predecessor.getFileAttachments()) {
        File predecessorFile = new File(getUploadPath(predecessor.getSalesInfoNoteId()) + attachment.getFileName());
        File successorFile = new File(getUploadPath(note.getSalesInfoNoteId()) + attachment.getFileName());
        try {
          FileUtils.copyFile(predecessorFile, successorFile);
        } catch (IOException e) {
        }
      }
    }
  }

  private void updateGenericNote(GenericNote note) {
    salesInfoService.updateSalesInfoNote(note);
    updateFileAttachments(note.getSalesInfoNoteId(), note.getFileAttachments());
  }

  private void updateFileAttachments(Long salesConvNoteId, List<FileAttachment> attachments) {
    Collection<FileAttachment> dbAttachments = visitReportDao.loadFileAttachmentsByNote(salesConvNoteId);
    for (FileAttachment dbAttachment : dbAttachments) {
      boolean found = false;
      for (FileAttachment attachment : attachments) {
        if (attachment.getFileAttachmentId() == dbAttachment.getFileAttachmentId()) {
          found = true;
          break;
        }
      }
      if (!found) {
        visitReportDao.deleteFileAttachment(dbAttachment.getFileAttachmentId());
        File attachmentFile = new File(getUploadPath(salesConvNoteId) + dbAttachment.getFileName());
        FileUtils.deleteQuietly(attachmentFile);
      }
    }
    for (FileAttachment attachment : attachments) {
      if (attachment.getFileAttachmentId() == -1) {
        attachment.setSalesInfoNoteId(salesConvNoteId);
        visitReportDao.insertFileAttachment(attachment);
      }
    }
  }

  private String getTempUploadPath(String uuid) {
    String path = localSettingService.getValue("application_salesInfoNote_filePath");
    if (!path.endsWith("/")) {
      path += "/";
    }
    path += uuid;
    if (!path.endsWith("/")) {
      path += "/";
    }
    return path;
  }

  private String getUploadPath(long salesInfoNoteId) {
    String path = localSettingService.getValue("application_salesInfoNote_filePath");
    if (!path.endsWith("/")) {
      path += "/";
    }
    path += String.valueOf(salesInfoNoteId);
    if (!path.endsWith("/")) {
      path += "/";
    }
    return path;
  }

  @Override
  public Collection<SBSOrgUnit> getSBSOrgUnits() {
    return visitReportDao.loadSBSOrgUnits();
  }

  @Override
  public SBSNote createSuccessorSBSNote(long noteId, BiteUser authenticatedUser) {
    SBSNote orgNote = getSBSNoteByNoteId(noteId);

    SBSNote newNote = new SBSNote();
    newNote.setSalesInfoNoteId(-1);
    newNote.setSalesInfoNoteType(orgNote.getSalesInfoNoteType());
    newNote.setPredecessorSalesInfoNoteId(noteId);
    newNote.setPartyId(orgNote.getPartyId());
    newNote.setNoteText(orgNote.getNoteText());

    // copy task
    DateTime taskStart = new DateTime();
    taskStart = taskStart.withSecondOfMinute(0);
    taskStart = taskStart.withMillisOfSecond(0);

    Task task = new Task();
    task.setActive(orgNote.getTask().isActive());
    task.setStatus(orgNote.getTask().getStatus());
    task.setType(orgNote.getTask().getType());
    task.setAssigneeUser(orgNote.getTask().getAssigneeUser());
    task.setStartDate(taskStart.toDate());
    task.setEndDate(taskStart.plusMinutes(15).toDate());
    task.setSendReminderMail(orgNote.getTask().isSendReminderMail());
    task.setSendVCalendarMail(orgNote.getTask().isSendVCalendarMail());
    task.setAddress(orgNote.getTask().getAddress());
    newNote.setTask(task);

    newNote.setCreationUser(authenticatedUser);
    newNote.setCreationTimestamp(new Date());
    newNote.setLastModificationUser(authenticatedUser);
    newNote.setLastModificationTimestamp(new Date());
    newNote.setDeleted(false);
    newNote.setCommunicationType(orgNote.getCommunicationType());
    newNote.setCommunicationChannel(orgNote.getCommunicationChannel());
    newNote.setContactType(orgNote.getContactType());
    newNote.setContactSource(orgNote.getContactSource());

    newNote.setContactPerson(orgNote.getContactPerson());

    // copy all product notes
    newNote.setProductNotes(new ArrayList<SBSProductNote>());
    for (SBSProductNote productNote : orgNote.getProductNotes()) {
      if (!productNote.isDeleted()) {
        productNote.setSalesInfoNoteId(-1);
        productNote.getTask().setTaskId(-1);
        newNote.getProductNotes().add(productNote);
      }
    }

    // copy not deleted and open tasks
    newNote.setTasks(new ArrayList<SalesInfoNote>());
    for (SalesInfoNote subTask : orgNote.getTasks()) {
      if (!subTask.isDeleted() && subTask.getTask() != null && (subTask.getTask().getStatus() == TaskStatus.OPEN || subTask.getTask().getStatus() == TaskStatus.WORKING)) {
        switch (subTask.getSalesInfoNoteType()) {
          case SI_COMPETITOR_NOTE:
            CompetitorNote competitorNote = salesInfoService.getCompetitorNoteByNoteId(subTask.getSalesInfoNoteId());
            competitorNote.setSalesInfoNoteId(-1);
            competitorNote.getTask().setTaskId(-1);
            newNote.getTasks().add(competitorNote);
            break;
          case SI_SIMPLE_NOTE:
            SimpleNote simpleNote = salesInfoService.getSimpleNoteByNoteId(subTask.getSalesInfoNoteId());
            simpleNote.setSalesInfoNoteId(-1);
            simpleNote.getTask().setTaskId(-1);
            newNote.getTasks().add(simpleNote);
            break;
          default:
            break;
        }
      }
    }

    newNote.setFeedbackAttributes(new ArrayList<Attribute>(visitReportDao.loadSalesInfoAttributesByGrouping(AttributeConfig.Groupings.VISITREPORT_SBS_FEEDBACK.name())));
    newNote.setReflectionAttributes(new ArrayList<Attribute>(visitReportDao.loadSalesInfoAttributesByGrouping(AttributeConfig.Groupings.VISITREPORT_SBS_REFLECTION.name())));

    return newNote;
  }

  @Override
  public boolean hasSuccessorNote(long noteId) {
    return visitReportDao.hasSuccessorNote(noteId);
  }

  @Override
  public GenericNote createSuccessorGenericNote(long noteId, BiteUser authenticatedUser) {
    GenericNote orgNote = getGenericNoteByNoteId(noteId);

    GenericNote newNote = new GenericNote();
    newNote.setSalesInfoNoteId(-1);
    newNote.setSalesInfoNoteType(orgNote.getSalesInfoNoteType());
    newNote.setPredecessorSalesInfoNoteId(noteId);
    newNote.setPartyId(orgNote.getPartyId());
    newNote.setNoteText(orgNote.getNoteText());

    // copy task
    DateTime taskStart = new DateTime();
    taskStart = taskStart.withSecondOfMinute(0);
    taskStart = taskStart.withMillisOfSecond(0);

    Task task = new Task();
    task.setActive(orgNote.getTask().isActive());
    task.setStatus(orgNote.getTask().getStatus());
    task.setType(orgNote.getTask().getType());
    task.setAssigneeUser(orgNote.getTask().getAssigneeUser());
    task.setStartDate(taskStart.toDate());
    task.setEndDate(taskStart.plusMinutes(15).toDate());
    task.setSendReminderMail(orgNote.getTask().isSendReminderMail());
    task.setSendVCalendarMail(orgNote.getTask().isSendVCalendarMail());
    task.setAddress(orgNote.getTask().getAddress());
    newNote.setTask(task);

    newNote.setCreationUser(authenticatedUser);
    newNote.setCreationTimestamp(new Date());
    newNote.setLastModificationUser(authenticatedUser);
    newNote.setLastModificationTimestamp(new Date());
    newNote.setDeleted(false);

    newNote.setFileAttachments(orgNote.getFileAttachments());

    return newNote;
  }

  @Override
  public void deleteGenericNote(SalesInfoNote note, UserInfo currentUser) throws VisitReportSuccessorExistsException {
    if (visitReportDao.hasSuccessorNote(note.getSalesInfoNoteId()) && !AuthorityHelper.hasAuthority(currentUser, Auth.SI_VR_SBS_NOTE_ADMIN)) {
      throw new VisitReportSuccessorExistsException();
    }
    // create .deleted file in folder
    String path = getUploadPath(note.getSalesInfoNoteId());
    File deletedFile = new File(path + ".deleted");
    try {
      deletedFile.createNewFile();
    } catch (Exception e) {
    }
  }

  @Override
  public void deleteSBSNote(SalesInfoNote note, UserInfo currentUser) throws VisitReportSuccessorExistsException {
    if (visitReportDao.hasSuccessorNote(note.getSalesInfoNoteId()) && !AuthorityHelper.hasAuthority(currentUser, Auth.SI_VR_GENERIC_NOTE_ADMIN)) {
      throw new VisitReportSuccessorExistsException();
    }

    // delete child notes
    SBSNote sbsNote = getSBSNoteByNoteId(note.getSalesInfoNoteId());
    for (SBSProductNote productNote : sbsNote.getProductNotes()) {
      productNote.setDeleted(true);
      productNote.setLastModificationTimestamp(new Date());
      productNote.setLastModificationUser(currentUser.getBiteUser());
      salesInfoService.updateSalesInfoNote(productNote);
    }
    for (SalesInfoNote task : sbsNote.getTasks()) {
      task.setDeleted(true);
      task.setLastModificationTimestamp(new Date());
      task.setLastModificationUser(currentUser.getBiteUser());
      salesInfoService.updateSalesInfoNote(task);
    }
  }

  @Override
  public void deleteSalesConvNote(SalesInfoNote note, UserInfo currentUser) {

    // delete child notes
    SalesConvNote salesConvNote = getSalesConvNoteByNoteId(note.getSalesInfoNoteId());
    for (SBSProductNote productNote : salesConvNote.getProductNotes()) {
      productNote.setDeleted(true);
      productNote.setLastModificationTimestamp(new Date());
      if (currentUser != null) {
        productNote.setLastModificationUser(currentUser.getBiteUser());
      } else {
        productNote.setLastModificationUser(note.getLastModificationUser());
      }
      visitReportDao.updateSBSProductNote(productNote);
      salesInfoService.updateSalesInfoNote(productNote);
    }
  }

  public void deleteSalesConvNoteWithoutTimeUpdates(SalesInfoNote note) {

    // delete child notes
    SalesConvNote salesConvNote = getSalesConvNoteByNoteId(note.getSalesInfoNoteId());
    for (SBSProductNote productNote : salesConvNote.getProductNotes()) {
      productNote.setDeleted(true);
      visitReportDao.updateSBSProductNote(productNote);
      salesInfoService.updateSalesInfoNote(productNote);
    }
  }

  public void deleteSBSNoteWithoutTimeUpdates(SalesInfoNote note) {

    // delete child notes
    SBSNote sbsNote = getSBSNoteByNoteId(note.getSalesInfoNoteId());
    for (SBSProductNote productNote : sbsNote.getProductNotes()) {
      productNote.setDeleted(true);
      salesInfoService.updateSalesInfoNote(productNote);
    }

    for (ToDoGroupNote todoGroup : sbsNote.getProductNoteGroups()) {
      todoGroup.setDeleted(true);
      salesInfoService.updateSalesInfoNote(todoGroup);

      for (SBSProductNote productNote : todoGroup.getRelatedNotes()) {
        productNote.setDeleted(true);
        salesInfoService.updateSalesInfoNote(productNote);
        for (SalesInfoNote historyNote : productNote.getHistoryNotes()) {
          historyNote.setDeleted(true);
          salesInfoService.updateSalesInfoNote(historyNote);
        }
      }
      for (SalesInfoNote historyNote : todoGroup.getHistoryNotes()) {
        historyNote.setDeleted(true);
        salesInfoService.updateSalesInfoNote(historyNote);
      }
    }
    for (SalesInfoNote product : sbsNote.getProductNotes()) {
      product.setDeleted(true);
      salesInfoService.updateSalesInfoNote(product);
      for (SalesInfoNote historyNote : product.getHistoryNotes()) {
        historyNote.setDeleted(true);
        salesInfoService.updateSalesInfoNote(historyNote);
      }
    }

    for (SalesInfoNote historyNote : sbsNote.getHistoryNotes()) {
      if (((HistoryNote) historyNote).getLevel() == HistoryLevel.NOTE) {
        historyNote.setDeleted(true);
        salesInfoService.updateSalesInfoNote(historyNote);
      }
    }

    for (SalesInfoNote appointmentNote : sbsNote.getAppointments()) {
      appointmentNote.setDeleted(true);
      salesInfoService.updateSalesInfoNote(appointmentNote);
    }

    for (SalesInfoNote task : sbsNote.getTasks()) {
      task.setDeleted(true);
      salesInfoService.updateSalesInfoNote(task);
    }
  }

  private SBSProductNote getSBSProductConfig(String productId, SalesInfoNoteType type) {
    String config = visitReportDao.loadSBSProductConfig(productId, type);

    if (config != null) {
      return gson.fromJson(config, SBSProductNote.class);
    }
    return new SBSProductNote();
  }

  @Override
  public SBSProductNote getSBSProductConfig(String productId) {
    return getSBSProductConfig(productId, SalesInfoNoteType.SI_VR_SBS_PRODUCT_NOTE);
  }

  @Override
  public SBSProductNote getSalesConvProductConfig(String productId) {
    return getSBSProductConfig(productId, SalesInfoNoteType.SI_SALES_CONV_PRODUCT_NOTE);
  }

  @Override
  public SalesConvNote getSalesConvNoteByNoteId(long noteId) {
    SalesConvNote note = visitReportDao.loadSalesConvNoteByNoteId(noteId, settingService.getBooleanValue("salesInfo.note.visitReport.experimentalQueryActive", false));
    note.setParty(partyDao.loadParty(note.getPartyId()));
    return note;
  }

  @Override
  public Collection<SBSProductNote> getProductNotesByNoteId(long noteId) {
    Collection<SBSProductNote> productNotes = visitReportDao.loadProductNotesByNote(noteId, settingService.getBooleanValue("salesInfo.note.visitReport.experimentalQueryActive", false));

    return productNotes;
  }

  @Override
  public void saveSalesConvNote(SalesConvNote note, String attachmentsFolderName, BiteUser authenticatedUser) throws Exception {
    modifySalesConvNote(note, attachmentsFolderName, authenticatedUser);
  }

  private void modifySalesConvNote(SalesConvNote note, String attachmentsFolderName, BiteUser authenticatedUser) throws Exception {
    boolean isUpdateScenario = false;
    // CMSYS-721 create new note entry for each modification
    if (note.getSalesInfoNoteId() > -1) {
      if (note.isDeleted()) {
        // if note is deleted,no need to perform any other operation
        salesInfoService.markNoteAsDeleted(note);
        deleteSalesConvNoteWithoutTimeUpdates(note);
        return;
      }
      isUpdateScenario = true;
      // Mark existing notes deleted and save a new records for them to track history
      note.setDeleted(true);
      ArrayList<Long> alreadyDeletedNotes = new ArrayList<Long>();
      for (SBSProductNote productNote : note.getProductNotes()) {
        if (productNote.isDeleted()) {
          alreadyDeletedNotes.add(productNote.getSalesInfoNoteId());
        }
        productNote.setDeleted(true);
      }
      salesInfoService.markNoteAsDeleted(note);
      deleteSalesConvNoteWithoutTimeUpdates(note);

      // Now save new record of sales conv note and product notes
      note.setDeleted(false);
      note.setPredecessorSalesInfoNoteId(note.getSalesInfoNoteId());
      note.setSalesInfoNoteId(-1);

      List<SBSProductNote> notesForRemoval = new ArrayList<SBSProductNote>();
      for (SBSProductNote productNote : note.getProductNotes()) {
        // CMSYS-721 create new note entry for each modification, already removed note should not be added again.
        if (alreadyDeletedNotes.contains(productNote.getSalesInfoNoteId())) {
          notesForRemoval.add(productNote);
          continue;
        }
        productNote.setSalesInfoNoteId(-1);
        productNote.setDeleted(false);
      }
      note.getProductNotes().removeAll(notesForRemoval);
    }
    note.setLastModificationTimestamp(new Date());
    note.setLastModificationUser(authenticatedUser);
    for (Attribute attribute : note.getFeedbackAttributes()) {
      attribute.setLastModifier(authenticatedUser);
      attribute.setLastUpdate(new Date());
    }

    salesInfoService.insertSalesInfoNote(note);
    NoteMailHelper noteMailHelper = new NoteMailHelper(this, salesInfoService, mailService);
    noteMailHelper.sendInsertMails(note);

    visitReportDao.insertSalesConvNote(note);
    for (SBSProductNote productNote : note.getProductNotes()) {
      productNote.setPredecessorSalesInfoNoteId(note.getSalesInfoNoteId());
      salesInfoService.insertSalesInfoNote(productNote);
      visitReportDao.insertSBSProductNote(productNote);
      insertNewHistoryItems(productNote);
    }
    for (Attribute attribute : note.getFeedbackAttributes()) {
      attributeDao.insert(attribute);
      visitReportDao.insertNoteAttribute(note.getSalesInfoNoteId(), attribute.getAttributeId());
    }

    for (FileAttachment attachment : note.getFileAttachments()) {
      attachment.setSalesInfoNoteId(note.getSalesInfoNoteId());
      if (isUpdateScenario && attachment.getFileAttachmentId() > -1) {
        visitReportDao.updateFileAttachmentNotesRelation(attachment);
      } else {
        visitReportDao.insertFileAttachment(attachment);
      }
    }

    File tempLocation = new File(getTempUploadPath(attachmentsFolderName));
    File newLocation = new File(getUploadPath(note.getSalesInfoNoteId()));
    try {
      FileUtils.moveDirectory(tempLocation, newLocation);
    } catch (Exception e) {
    }

    if (isUpdateScenario) {
      File oldNoteAttachmentFolder = new File(getUploadPath(note.getPredecessorSalesInfoNoteId()));
      File newNoteAttachmentFolder = new File(getUploadPath(note.getSalesInfoNoteId()));
      try {
        FileUtils.moveDirectory(oldNoteAttachmentFolder, newNoteAttachmentFolder);
      } catch (Exception e) {
      }
    }
  }

  private void insertNewHistoryItems(SBSProductNote productNote) {
    for (ProductHistoryItem historyItem : productNote.getHistoryItems()) {
      if (historyItem.getId() == null) {
        historyItem.setProductNoteId(productNote.getSalesInfoNoteId());
        visitReportDao.insertProductHistoryItem(historyItem);
      } else {
        historyItem.setProductNoteId(productNote.getSalesInfoNoteId());
        visitReportDao.updateProductHistoryItem(historyItem);
      }
    }
  }

  @Override
  public boolean sendAttachmentEmail(SalesConvEmailData emailData, UserInfo authenticatedUser) throws IOException, URISyntaxException, XmlException, ErrorMessage {

    emailData.setSender(visitReportDao.getTeamEmailAddress(authenticatedUser.getId()));

    String emailTemplate = settingService.getValue(noteAttachmentTemplate);

    emailTemplate = emailTemplate.replaceAll("\\{sender\\}", emailData.getSender());
    emailTemplate = emailTemplate.replaceAll("\\{receiver\\}", emailData.getRecipient());
    emailTemplate = emailTemplate.replaceAll("\\{subject\\}", emailData.getSubject());
    emailTemplate = emailTemplate.replaceAll("\\{message\\}", emailData.getMessage());
    emailTemplate = emailTemplate.replaceAll("\\{attachments\\}", formatAttachments(emailData.getAttachmentUrls()));

    CusCoMessage cuscoMessage = createCuscoMessage(emailData, emailTemplate);

    return cuscoCustomerContactService.sendEmailDocument(cuscoMessage);
  }

  private CusCoMessage createCuscoMessage(SalesConvEmailData emailData, String xmlData) {
    CusCoConfigurtationBean configBean = new CusCoConfigurtationBean(SOURCE_SYSTEM_CUCO, DUMMY_PSWD);
    CusCoMessageBuilder builder = new CusCoMessageBuilder(configBean);
    CusCoMessage cuscoMessage = builder.createForOperation("SALESNOTE");
    cuscoMessage.setOutputChannel(OUTPUT_CHANNEL_EMAIL);
    cuscoMessage.setTemplateId(settingService.getValue(noteAttachmentTemplateName));
    cuscoMessage.getParameterMap().put("XmlData", xmlData);
    cuscoMessage.getParameterMap().put("partyId", emailData.getPartyId());
    cuscoMessage.getParameterMap().put("sender", emailData.getSender());
    cuscoMessage.getParameterMap().put("recipient", emailData.getRecipient());

    return cuscoMessage;
  }

  private String formatAttachments(Map<String, String> attachmentUrls) {
    String attachmentsBlock = "";
    String attachmentTemplate = settingService.getValue(noteAttachmentTemplateAttachments);
    for (Entry<String, String> url : attachmentUrls.entrySet()) {
      String template = attachmentTemplate;
      template = template.replaceAll("\\{attachmentName\\}", url.getKey());
      template = template.replaceAll("\\{attachmentUrl\\}", url.getValue());
      attachmentsBlock += template;
    }

    return attachmentsBlock;
  }

  @Override
  public void saveSBSNote(SBSNote note, String attachmentsFolderName, BiteUser authenticatedUser) {
    saveSBSNotesWithHistory(note, authenticatedUser);
  }

  private void updateOriginalSBSNote(SBSNote note, BiteUser authenticatedUser) {
    SBSNote predecessor = getSBSNoteByNoteId(note.getPredecessorSalesInfoNoteId());
    if (predecessor != null && !predecessor.isDeleted()) {
      // set status of tasks
      for (SalesInfoNote task : predecessor.getTasks()) {
        if (!task.isDeleted() && task.getTask() != null && (task.getTask().getStatus() == TaskStatus.OPEN || task.getTask().getStatus() == TaskStatus.WORKING)) {
          task.getTask().setStatus(TaskStatus.OBSOLESCED_BY_SUCCESSOR);
          task.getTask().setActive(false);
          task.setLastModificationUser(authenticatedUser);
          task.setLastModificationTimestamp(new Date());
          salesInfoService.updateSalesInfoNote(task);
        }
      }
      // set status of appointment
      for (SalesInfoNote appointment : predecessor.getAppointments()) {
        if (!appointment.isDeleted() && appointment.getTask() != null && (appointment.getTask().getStatus() == TaskStatus.OPEN || appointment.getTask().getStatus() == TaskStatus.WORKING)) {
          appointment.getTask().setStatus(TaskStatus.OBSOLESCED_BY_SUCCESSOR);
          appointment.getTask().setActive(false);
          appointment.setLastModificationUser(authenticatedUser);
          appointment.setLastModificationTimestamp(new Date());
          salesInfoService.updateSalesInfoNote(appointment);
        }
      }
      // remove reminder date of product notes
      for (SBSProductNote productNote : predecessor.getProductNotes()) {
        if (!productNote.isDeleted()) {
          productNote.getTask().setStatus(TaskStatus.OBSOLESCED_BY_SUCCESSOR);
          productNote.getTask().setActive(false);
          productNote.setLastModificationUser(authenticatedUser);
          productNote.setLastModificationTimestamp(new Date());
          salesInfoService.updateSalesInfoNote(productNote);
        }
      }

      for (ToDoGroupNote groupNote : predecessor.getProductNoteGroups()) {
        for (SBSProductNote productNote : groupNote.getRelatedNotes()) {
          if (!productNote.isDeleted()) {
            productNote.getTask().setStatus(TaskStatus.OBSOLESCED_BY_SUCCESSOR);
            productNote.getTask().setActive(false);
            productNote.setLastModificationUser(authenticatedUser);
            productNote.setLastModificationTimestamp(new Date());
            salesInfoService.updateSalesInfoNote(productNote);
          }
        }

      }
    }
  }

  // This method will save new record on each activity performed on SBS note to maintain the history of the changes done by the user
  private void saveSBSNotesWithHistory(SBSNote note, BiteUser authenticatedUser) {
    boolean isUpdateScenario = false;
    if (note.getSalesInfoNoteId() > -1) {
      isUpdateScenario = true;
      if (note.isDeleted()) {
        // if note is deleted,no need to perform any other operation
        salesInfoService.markNoteAsDeleted(note);
        deleteSBSNoteWithoutTimeUpdates(note);
        return;
      }
      // start Mark existing notes deleted and save a new records for them to track history
      note.setDeleted(true);
      ArrayList<Long> alreadyDeletedNotes = new ArrayList<Long>();
      for (SBSProductNote productNote : note.getProductNotes()) {
        if (productNote.isDeleted()) {
          alreadyDeletedNotes.add(productNote.getSalesInfoNoteId());
        }
        productNote.setDeleted(true);

        for (SalesInfoNote historyNote : productNote.getHistoryNotes()) {
          if (historyNote.isDeleted()) {
            alreadyDeletedNotes.add(historyNote.getSalesInfoNoteId());
          }
          historyNote.setDeleted(true);

        }
      }

      for (ToDoGroupNote groupNote : note.getProductNoteGroups()) {

        if (groupNote.isDeleted()) {
          alreadyDeletedNotes.add(groupNote.getSalesInfoNoteId());
          groupNote.setDeleted(true);
          // returning as deleted noted will be handled in sbsnote.getproductNotes
          continue;
        }

        for (SalesInfoNote historyNote : groupNote.getHistoryNotes()) {
          if (historyNote.isDeleted()) {
            alreadyDeletedNotes.add(historyNote.getSalesInfoNoteId());
          }
          historyNote.setDeleted(true);
        }

        for (SBSProductNote productNote : groupNote.getRelatedNotes()) {
          if (productNote.isDeleted()) {
            alreadyDeletedNotes.add(productNote.getSalesInfoNoteId());
          }
          productNote.setDeleted(true);

          for (SalesInfoNote historyNote : productNote.getHistoryNotes()) {
            if (historyNote.isDeleted()) {
              alreadyDeletedNotes.add(historyNote.getSalesInfoNoteId());
            }
            historyNote.setDeleted(true);
          }
        }

      }
      for (SalesInfoNote taskNote : note.getTasks()) {
        if (taskNote.isDeleted()) {
          alreadyDeletedNotes.add(taskNote.getSalesInfoNoteId());
        }
        taskNote.setDeleted(true);
      }
      for (SalesInfoNote appointmentNote : note.getAppointments()) {
        if (appointmentNote.isDeleted()) {
          alreadyDeletedNotes.add(appointmentNote.getSalesInfoNoteId());
        }
        appointmentNote.setDeleted(true);
      }
      salesInfoService.markNoteAsDeleted(note);
      deleteSBSNoteWithoutTimeUpdates(note);
      // End - Mark existing notes deleted and save a new records for them to track history
      // Now save new record of sales conv note and product notes
      note.setDeleted(false);
      note.setPredecessorSalesInfoNoteId(note.getSalesInfoNoteId());
      note.setSalesInfoNoteId(-1);

      List<SBSProductNote> notesForRemoval = new ArrayList<SBSProductNote>();
      for (SBSProductNote productNote : note.getProductNotes()) {
        // create new note entry for each modification, already removed note should not be added again.
        if (alreadyDeletedNotes.contains(productNote.getSalesInfoNoteId())) {
          notesForRemoval.add(productNote);
          continue;
        }
        productNote.setSalesInfoNoteId(-1);
        productNote.setDeleted(false);

        List<HistoryNote> historyNotesForRemoval = new ArrayList<HistoryNote>();
        for (HistoryNote historyNote : productNote.getHistoryNotes()) {
          if (alreadyDeletedNotes.contains(historyNote.getSalesInfoNoteId())) {
            historyNotesForRemoval.add(historyNote);
            continue;
          }
          historyNote.setSalesInfoNoteId(-1);
          historyNote.setDeleted(false);
        }
        productNote.getHistoryNotes().removeAll(historyNotesForRemoval);
      }
      note.getProductNotes().removeAll(notesForRemoval);

      List<ToDoGroupNote> groupsForRemoval = new ArrayList<ToDoGroupNote>();
      for (ToDoGroupNote groupNote : note.getProductNoteGroups()) {
        // create new note entry for each modification, already removed note should not be added again.
        if (alreadyDeletedNotes.contains(groupNote.getSalesInfoNoteId())) {
          groupsForRemoval.add(groupNote);
          continue;
        }
        groupNote.setSalesInfoNoteId(-1);
        groupNote.setDeleted(false);

        List<HistoryNote> historyNotesForRemoval = new ArrayList<HistoryNote>();
        for (HistoryNote historyNote : groupNote.getHistoryNotes()) {
          if (alreadyDeletedNotes.contains(historyNote.getSalesInfoNoteId())) {
            historyNotesForRemoval.add(historyNote);
            continue;
          }
          historyNote.setSalesInfoNoteId(-1);
          historyNote.setDeleted(false);
        }
        groupNote.getHistoryNotes().removeAll(historyNotesForRemoval);

        List<SBSProductNote> pnForRemoval = new ArrayList<SBSProductNote>();
        for (SBSProductNote productNote : groupNote.getRelatedNotes()) {
          // create new note entry for each modification, already removed note should not be added again.
          if (alreadyDeletedNotes.contains(productNote.getSalesInfoNoteId())) {
            pnForRemoval.add(productNote);
            continue;
          }
          productNote.setSalesInfoNoteId(-1);
          productNote.setDeleted(false);

          List<HistoryNote> prodHistoryNotesForRemoval = new ArrayList<HistoryNote>();
          for (HistoryNote historyNote : productNote.getHistoryNotes()) {
            if (alreadyDeletedNotes.contains(historyNote.getSalesInfoNoteId())) {
              prodHistoryNotesForRemoval.add(historyNote);
              continue;
            }
            historyNote.setSalesInfoNoteId(-1);
            historyNote.setDeleted(false);
          }
          productNote.getHistoryNotes().removeAll(prodHistoryNotesForRemoval);
        }
        groupNote.getRelatedNotes().removeAll(pnForRemoval);
      }
      note.getProductNoteGroups().removeAll(groupsForRemoval);

      List<SalesInfoNote> tasksForRemoval = new ArrayList<SalesInfoNote>();
      for (SalesInfoNote taskNote : note.getTasks()) {
        // create new note entry for each modification, already removed note should not be added again.
        if (alreadyDeletedNotes.contains(taskNote.getSalesInfoNoteId())) {
          tasksForRemoval.add(taskNote);
          continue;
        }
        taskNote.setSalesInfoNoteId(-1);
        taskNote.setDeleted(false);
      }
      note.getTasks().removeAll(tasksForRemoval);

      List<SalesInfoNote> appointmentsForRemoval = new ArrayList<SalesInfoNote>();
      for (SalesInfoNote appointmentNote : note.getAppointments()) {
        // create new note entry for each modification, already removed note should not be added again.
        if (alreadyDeletedNotes.contains(appointmentNote.getSalesInfoNoteId())) {
          appointmentsForRemoval.add(appointmentNote);
          continue;
        }
        appointmentNote.setSalesInfoNoteId(-1);
        appointmentNote.setDeleted(false);
      }
      note.getAppointments().removeAll(appointmentsForRemoval);
    }

    salesInfoService.insertSalesInfoNote(note);
    visitReportDao.insertSBSNote(note);
    for (SBSProductNote productNote : note.getProductNotes()) {
      productNote.setPredecessorSalesInfoNoteId(note.getSalesInfoNoteId());

      salesInfoService.insertSalesInfoNote(productNote);
      visitReportDao.insertSBSProductNote(productNote);

      for (HistoryNote historyNote : productNote.getHistoryNotes()) {
        historyNote.setPredecessorSalesInfoNoteId(productNote.getSalesInfoNoteId());
        if (historyNote.getHistoryNoteId() == null || historyNote.getHistoryNoteId() < 1) {
          historyNote.setHistoryNoteId(productNote.getSalesInfoNoteId());
        }
        salesInfoService.insertSalesInfoNote(historyNote);
        visitReportDao.insertHistoryNote(historyNote);
      }

      // save attachments

      for (FileAttachment attachment : productNote.getFileAttachments()) {
        attachment.setSalesInfoNoteId(productNote.getSalesInfoNoteId());
        if (isUpdateScenario && attachment.getFileAttachmentId() > -1) {
          visitReportDao.updateFileAttachmentNotesRelation(attachment);
        } else {
          visitReportDao.insertFileAttachment(attachment);

          File currentFileName = new File(getUploadPath(productNote.getPartyId()) + "/" + attachment.getFileName());
          File newFileName = new File(getUploadPath(productNote.getPartyId()) + "/" + attachment.getFileAttachmentId());
          try {
            currentFileName.renameTo(newFileName);
          } catch (Exception ex) {
            logger.error("Error while Trying to move file location from " + currentFileName.getAbsolutePath() + "  to " + newFileName.getAbsolutePath(), ex);
          }
        }
      }

    }
    for (Attribute attribute : note.getReflectionAttributes()) {
      attributeDao.insert(attribute);
      visitReportDao.insertNoteAttribute(note.getSalesInfoNoteId(), attribute.getAttributeId());
    }
    for (Attribute attribute : note.getFeedbackAttributes()) {
      attributeDao.insert(attribute);
      visitReportDao.insertNoteAttribute(note.getSalesInfoNoteId(), attribute.getAttributeId());
    }
    for (SalesInfoNote task : note.getTasks()) {
      task.setPredecessorSalesInfoNoteId(note.getSalesInfoNoteId());
      salesInfoService.insertSalesInfoNote(task);
      for (HistoryNote historyNote : task.getHistoryNotes()) {
        historyNote.setPredecessorSalesInfoNoteId(note.getSalesInfoNoteId());
        if (historyNote.getHistoryNoteId() == null || historyNote.getHistoryNoteId() < 1) {
          historyNote.setHistoryNoteId(task.getSalesInfoNoteId());
        }
        salesInfoService.insertSalesInfoNote(historyNote);
        visitReportDao.insertHistoryNote(historyNote);
      }
    }
    for (SalesInfoNote appointments : note.getAppointments()) {
      appointments.setPredecessorSalesInfoNoteId(note.getSalesInfoNoteId());
      salesInfoService.insertSalesInfoNote(appointments);

      for (HistoryNote historyNote : appointments.getHistoryNotes()) {
        historyNote.setPredecessorSalesInfoNoteId(note.getSalesInfoNoteId());
        if (historyNote.getHistoryNoteId() == null || historyNote.getHistoryNoteId() < 1) {
          historyNote.setHistoryNoteId(appointments.getSalesInfoNoteId());
        }
        salesInfoService.insertSalesInfoNote(historyNote);
        visitReportDao.insertHistoryNote(historyNote);
      }
    }

    for (HistoryNote historyNote : note.getHistoryNotes()) {
      // only process history notes at sbsnote level, others will be handled individually
      if (historyNote.getLevel() == HistoryLevel.NOTE) {
        historyNote.setPredecessorSalesInfoNoteId(note.getSalesInfoNoteId());
        if (historyNote.getHistoryNoteId() == null || historyNote.getHistoryNoteId() < 1) {
          historyNote.setHistoryNoteId(note.getSalesInfoNoteId());
        }
        salesInfoService.insertSalesInfoNote(historyNote);
        visitReportDao.insertHistoryNote(historyNote);
      }
    }

    for (ToDoGroupNote groupNote : note.getProductNoteGroups()) {
      if (groupNote.isDeleted()) {
        continue;
      }
      groupNote.setPredecessorSalesInfoNoteId(note.getSalesInfoNoteId());
      // Check if assignee is changed, if so, send reminder email
      if (groupNote.isSendCompletionEmail()) {
        posService.sendToDoCompletedToPOSEmail(note.getParty(), groupNote, groupNote.getAssignedToDelearInfo(), groupNote.getEmailAdditionalText(), authenticatedUser);
      }
      if (groupNote.isSendAssignmentEmail()) {
        posService.sendToDoAssignedToPOSEmail(note.getParty(), groupNote, groupNote.getAssignedToDelearInfo(), groupNote.getEmailAdditionalText(), authenticatedUser);
      }
      salesInfoService.insertSalesInfoNote(groupNote);
      visitReportDao.insertSBSToDoGroupNote(groupNote);

      for (HistoryNote historyNote : groupNote.getHistoryNotes()) {
        historyNote.setPredecessorSalesInfoNoteId(groupNote.getSalesInfoNoteId());
        if (historyNote.getHistoryNoteId() == null || historyNote.getHistoryNoteId() < 1) {
          historyNote.setHistoryNoteId(groupNote.getSalesInfoNoteId());
        }
        salesInfoService.insertSalesInfoNote(historyNote);
        visitReportDao.insertHistoryNote(historyNote);
      }

      for (SBSProductNote productNote : groupNote.getRelatedNotes()) {
        if (productNote.isDeleted()) {
          continue;
        }
        productNote.setPredecessorSalesInfoNoteId(note.getSalesInfoNoteId());
        productNote.setTodoGroupNoteId(groupNote.getSalesInfoNoteId());

        salesInfoService.insertSalesInfoNote(productNote);
        visitReportDao.insertSBSProductNote(productNote);

        for (HistoryNote historyNote : productNote.getHistoryNotes()) {
          historyNote.setPredecessorSalesInfoNoteId(productNote.getSalesInfoNoteId());
          if (historyNote.getHistoryNoteId() == null || historyNote.getHistoryNoteId() < 1) {
            historyNote.setHistoryNoteId(productNote.getSalesInfoNoteId());
          }
          salesInfoService.insertSalesInfoNote(historyNote);
          visitReportDao.insertHistoryNote(historyNote);
        }

        // save attachments
        for (FileAttachment attachment : productNote.getFileAttachments()) {
          attachment.setSalesInfoNoteId(productNote.getSalesInfoNoteId());
          if (isUpdateScenario && attachment.getFileAttachmentId() > -1) {
            visitReportDao.updateFileAttachmentNotesRelation(attachment);
          } else {
            visitReportDao.insertFileAttachment(attachment);
            File currentFileName = new File(getUploadPath(productNote.getPartyId()) + "/" + attachment.getFileName());
            File newFileName = new File(getUploadPath(productNote.getPartyId()) + "/" + attachment.getFileAttachmentId());
            try {
              currentFileName.renameTo(newFileName);
            } catch (Exception ex) {
              logger.error("For GroupNote: Error while Trying to move file location from " + currentFileName.getAbsolutePath() + "  to " + newFileName.getAbsolutePath(), ex);
            }
          }
        }
      }

      for (Attribute attribute : groupNote.getAttributes()) {
        attribute.setLastModifier(authenticatedUser);
        attribute.setLastUpdate(new Date());
        attribute.setKundeId(groupNote.getPartyId());
        attributeDao.insert(attribute);
        visitReportDao.insertNoteAttribute(groupNote.getSalesInfoNoteId(), attribute.getAttributeId());
      }
    }

    if (note.getPredecessorSalesInfoNoteId() != null) {
      updateOriginalSBSNote(note, note.getCreationUser());
    }
  }

  @Override
  public void sendAssignToDoEmail(Party party, SBSNote sbsNote, ToDoGroupNote groupNote, BiteUser biteUserFromSession) {
    // TODO Auto-generated method stub

  }

  @Override
  public SalesInfoNote getNoteForHistoryByNoteId(HistoryNote historyNote) {
    if (historyNote.getLevel() == HistoryLevel.NOTE) {
      if (historyNote.getHistoryTitle() == HistoryTitle.PRODUCT_DELETED) {
        return visitReportDao.getProductNoteForHistoryByNoteId(historyNote.getHistoryNoteId());
      } else if (historyNote.getHistoryTitle() == HistoryTitle.PRODUCT_GROUP_DELETED) {
        return visitReportDao.getToDoGroupNoteForHistoryByNoteId(historyNote.getHistoryNoteId());
      } else if (historyNote.getHistoryTitle() == HistoryTitle.TERMIN_CREATED || historyNote.getHistoryTitle() == HistoryTitle.TERMIN_DELETED
          || historyNote.getHistoryTitle() == HistoryTitle.TERMIN_MIGRATED) {
        return salesInfoService.getAppointmentNoteForHistoryByNoteId(historyNote.getHistoryNoteId());
      } else if (historyNote.getHistoryTitle() == HistoryTitle.TASK_CREATD || historyNote.getHistoryTitle() == HistoryTitle.TASK_MODIFIED
          || historyNote.getHistoryTitle() == HistoryTitle.TASK_DELETED) {
        return salesInfoService.getTaskNoteForHistoryByNoteId(historyNote.getHistoryNoteId());
      }
      return visitReportDao.getNoteForHistoryByNoteId(historyNote.getHistoryNoteId());
    } else if (historyNote.getLevel() == HistoryLevel.PRODUCT_NOTE) {
      return visitReportDao.getProductNoteForHistoryByNoteId(historyNote.getHistoryNoteId());
    } else if (historyNote.getLevel() == HistoryLevel.TODO_GROUP_NOTE) {
      return visitReportDao.getToDoGroupNoteForHistoryByNoteId(historyNote.getHistoryNoteId());
    }
    return null;
  }

  @Override
  public Collection<HistoryNote> getHistoryNotesByNoteId(Long predecessorSalesInfoNoteId) {
    return visitReportDao.getHistoryNotesByNoteId(predecessorSalesInfoNoteId);
  }

  @Override
  public void insertSBSProduct(SBSProduct product) {
    visitReportDao.insertSBSProduct(product);
  }

  @Override
  public void updateSBSProduct(SBSProduct product) {
    visitReportDao.updateSBSProduct(product);
  }

  @Override
  public DigitalSellingNote getDigitalSellingNoteByNoteId(long noteId) {
    DigitalSellingNote note = visitReportDao.loadDigitalSellingNoteByNoteId(noteId);

    DigitalSellingNote xmlNote = null;
    if (note.getContent() != null) {
      xmlNote = unmarshalDigitalSellingNote(note.getContent());
    }
    if (xmlNote != null) {
      note.setHousehold(xmlNote.getHousehold());
      note.setInternetSpeed(xmlNote.getInternetSpeed());
      note.setTv(xmlNote.getTv());
      note.setMobilePhone(xmlNote.getMobilePhone());
      note.setMobileTariff(xmlNote.getMobileTariff());
      note.setMusic(xmlNote.getMusic());
      note.setSecurity(xmlNote.getSecurity());
      note.setSmartHome(xmlNote.getSmartHome());
      note.setPayment(xmlNote.getPayment());
      note.setServices(xmlNote.getServices());
      note.setSumNew(xmlNote.getSumNew());
      note.setSumOld(xmlNote.getSumOld());
      note.setComment(xmlNote.getComment());
    }
    note.setSavedInstance(xmlNote);
    note.setParty(partyDao.loadParty(note.getPartyId()));
    return note;
  }

  @Override
  public DigitalSellingNote createSuccessorDigitalSellingNote(long noteId, BiteUser authenticatedUser) {
    DigitalSellingNote orgNote = getDigitalSellingNoteByNoteId(noteId);

    DigitalSellingNote newNote = new DigitalSellingNote();
    newNote.setSalesInfoNoteId(-1);
    newNote.setSalesInfoNoteType(orgNote.getSalesInfoNoteType());
    newNote.setPredecessorSalesInfoNoteId(noteId);
    newNote.setPartyId(orgNote.getPartyId());
    newNote.setNoteText(orgNote.getNoteText());

    // copy task
    DateTime taskStart = new DateTime();
    taskStart = taskStart.withSecondOfMinute(0);
    taskStart = taskStart.withMillisOfSecond(0);

    Task task = new Task();
    task.setActive(orgNote.getTask().isActive());
    task.setStatus(orgNote.getTask().getStatus());
    task.setType(orgNote.getTask().getType());
    task.setAssigneeUser(orgNote.getTask().getAssigneeUser());
    task.setStartDate(taskStart.toDate());
    task.setEndDate(taskStart.plusMinutes(15).toDate());
    task.setSendReminderMail(orgNote.getTask().isSendReminderMail());
    task.setSendVCalendarMail(orgNote.getTask().isSendVCalendarMail());
    task.setAddress(orgNote.getTask().getAddress());
    newNote.setTask(task);

    newNote.setCreationUser(authenticatedUser);
    newNote.setCreationTimestamp(new Date());
    newNote.setLastModificationUser(authenticatedUser);
    newNote.setLastModificationTimestamp(new Date());
    newNote.setDeleted(false);

    return newNote;
  }

  @Override
  public void saveDigitalSellingNote(DigitalSellingNote note, BiteUser authenticatedUser) {
    if (note.getSalesInfoNoteId() > -1) {
      if (note.isDeleted()) {
        // if note is deleted, no need to perform any other operation
        salesInfoService.markNoteAsDeleted(note);
        deleteSBSNoteWithoutTimeUpdates(note);
        return;
      }

      note.setDeleted(true);
      salesInfoService.markNoteAsDeleted(note);

      note.setDeleted(false);
      note.setPredecessorSalesInfoNoteId(note.getSalesInfoNoteId());
      note.setSalesInfoNoteId(-1);
    }
    note.setContent(marshalDigitalSellingNote(note));
    insertDigitalSellingNote(note);
    insertDigitalSellingAttributes(note, authenticatedUser);

    for (HistoryNote historyNote : note.getHistoryNotes()) {
      // only process history notes at digital selling level, others will be handled individually
      if (historyNote.getLevel() == HistoryLevel.NOTE) {
        historyNote.setPredecessorSalesInfoNoteId(note.getSalesInfoNoteId());
        if (historyNote.getHistoryNoteId() == null || historyNote.getHistoryNoteId() < 1) {
          historyNote.setHistoryNoteId(note.getSalesInfoNoteId());
        }
        salesInfoService.insertSalesInfoNote(historyNote);
        visitReportDao.insertHistoryNote(historyNote);
      }
    }
  }

  private void insertDigitalSellingAttributes(DigitalSellingNote note, BiteUser authenticatedUser) {
    for (Attribute attribute : note.getAttributes()) {
      attribute.setLastModifier(authenticatedUser);
      attribute.setLastUpdate(new Date());
      attribute.setKundeId(note.getPartyId());
      attributeDao.insert(attribute);
      visitReportDao.insertNoteAttribute(note.getSalesInfoNoteId(), attribute.getAttributeId());
    }
  }

  private void insertDigitalSellingNote(DigitalSellingNote note) {
    salesInfoService.insertSalesInfoNote(note);
    visitReportDao.insertDigitalSellingNote(note);
  }

  protected String marshalDigitalSellingNote(final DigitalSellingNote digitalSellingNote) {
    try {
      JAXBContext jc = JAXBContext.newInstance(DigitalSellingNote.class);
      final Marshaller marshaller = jc.createMarshaller();

      final StringWriter sw = new StringWriter();
      marshaller.marshal(digitalSellingNote, sw);
      return sw.toString();
    } catch (JAXBException e) {
      logger.error("Error while marshalling digital selling note", e);
    }
    return null;
  }

  protected DigitalSellingNote unmarshalDigitalSellingNote(final String input) {
    try {
      final JAXBContext jc = JAXBContext.newInstance(DigitalSellingNote.class);
      final Unmarshaller unmarshaller = jc.createUnmarshaller();
      return (DigitalSellingNote) unmarshaller.unmarshal(new StringReader(input));
    } catch (JAXBException e) {
      logger.error("Error while unmarshalling digital selling note", e);
    }
    return null;
  }

  @Override
  public ArrayList<Attribute> getDigitalSellingNoteAttributes() {
    ArrayList<Attribute> attributes = new ArrayList<Attribute>();
    for (Groupings grouping : AttributeConfig.Groupings.values()) {
      if (grouping.name().startsWith("DIGITAL_SELLING_")) {
        attributes.addAll(visitReportDao.loadSalesInfoAttributesByGrouping(grouping.name()));
      }
    }
    return attributes;
  }

  @Override
  public JasperPrint generatePartyDataReport(DigitalSellingNote note, String nameOfUser) throws JRException {
    return visitReportPrintService.generateDigitalSellingNoteReport(note, nameOfUser);
  }
}
