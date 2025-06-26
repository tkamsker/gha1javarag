package at.a1ta.cuco.core.service.visitreport;

import java.io.IOException;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.Collection;

import org.apache.xmlbeans.XmlException;

import com.telekomaustriagroup.esb.cuscocustomercontact.ErrorMessage;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.cuco.core.shared.dto.Attribute;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.SalesConvEmailData;
import at.a1ta.cuco.core.shared.dto.salesinfo.HistoryNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.ToDoGroupNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.VisitReportSuccessorExistsException;
import at.a1ta.cuco.core.shared.dto.salesinfo.salesconvnote.SalesConvNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.DigitalSellingNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.generic.GenericNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSOrgUnit;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSProduct;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSProductNote;
import net.sf.jasperreports.engine.JRException;
import net.sf.jasperreports.engine.JasperPrint;

public interface VisitReportService {

  Collection<SBSProduct> getSBSProducts();

  GenericNote getGenericNoteByNoteId(long noteId);

  SBSNote getSBSNoteByNoteId(long noteId);

  Collection<Attribute> getSBSNoteTemplateReflection();

  Collection<Attribute> getSBSNoteTemplateFeedback();

  void saveSBSNote(SBSNote note, String attachmentsFolderName, BiteUser biteUser);

  void saveGenericNote(GenericNote note, String attachmentsFolderName);

  Collection<SBSOrgUnit> getSBSOrgUnits();

  SBSNote createSuccessorSBSNote(long noteId, BiteUser authenticatedUser);

  boolean hasSuccessorNote(long noteId);

  GenericNote createSuccessorGenericNote(long noteId, BiteUser authenticatedUser);

  void deleteSBSNote(SalesInfoNote note, UserInfo currentUser) throws VisitReportSuccessorExistsException;

  void deleteGenericNote(SalesInfoNote note, UserInfo currentUser) throws VisitReportSuccessorExistsException;

  void deleteSalesConvNote(SalesInfoNote note, UserInfo currentUser);

  SBSProductNote getSBSProductConfig(String productId);

  SalesConvNote getSalesConvNoteByNoteId(long noteId);

  void saveSalesConvNote(SalesConvNote note, String attachmentsFolderName, BiteUser biteUser) throws Exception;

  SBSProductNote getSalesConvProductConfig(String productId);

  Collection<SBSProduct> getSalesConvProducts();

  Collection<Attribute> getSalesConvNoteTemplateFeedback();

  boolean sendAttachmentEmail(SalesConvEmailData emailData, UserInfo authenticatedUser) throws IOException, URISyntaxException, XmlException, ErrorMessage;

  void saveQuotePdfAsFileAttachment(String fileName, byte[] quotePdfBytes, long salesConvNoteId, BiteUser currentUser) throws IOException;

  Collection<SBSProductNote> getProductNotesByNoteId(long noteId);

  ArrayList<Attribute> getToDoGroupNoteTemplateToDos();

  void sendAssignToDoEmail(Party party, SBSNote sbsNote, ToDoGroupNote groupNote, BiteUser biteUserFromSession);

  SalesInfoNote getNoteForHistoryByNoteId(HistoryNote historyNote);

  Collection<HistoryNote> getHistoryNotesByNoteId(Long predecessorSalesInfoNoteId);

  void insertSBSProduct(SBSProduct product);

  void updateSBSProduct(SBSProduct product);

  Collection<SBSProduct> getAllSBSProducts();

  DigitalSellingNote getDigitalSellingNoteByNoteId(long noteId);

  DigitalSellingNote createSuccessorDigitalSellingNote(long noteId, BiteUser authenticatedUser);

  void saveDigitalSellingNote(DigitalSellingNote note, BiteUser authenticatedUser);

  ArrayList<Attribute> getDigitalSellingNoteAttributes();

  JasperPrint generatePartyDataReport(final DigitalSellingNote note, final String nameOfUser) throws JRException;
}
