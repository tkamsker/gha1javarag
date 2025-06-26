package at.a1ta.cuco.core.dao.db.visitreport;

import java.util.Collection;

import at.a1ta.cuco.core.shared.dto.Attribute;
import at.a1ta.cuco.core.shared.dto.salesinfo.HistoryNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote.SalesInfoNoteType;
import at.a1ta.cuco.core.shared.dto.salesinfo.ToDoGroupNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.salesconvnote.ProductHistoryItem;
import at.a1ta.cuco.core.shared.dto.salesinfo.salesconvnote.SalesConvNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.DigitalSellingNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.generic.FileAttachment;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.generic.GenericNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSOrgUnit;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSProduct;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSProductNote;

public interface VisitReportDao {
  Collection<SBSProduct> loadSBSProducts(SalesInfoNoteType type);

  String loadSBSProductConfig(String productId, SalesInfoNoteType type);

  Collection<SBSProductNote> loadProductNotesByNote(long noteId, boolean experimentalModeEnabled);

  Collection<FileAttachment> loadFileAttachmentsByNote(long noteId);

  GenericNote loadGenericNoteByNoteId(long noteId);

  SBSNote loadSBSNoteByNoteId(long noteId, boolean isExperimentalModeEnabled);

  Collection<Attribute> loadSalesInfoAttributesByGrouping(String grouping);

  Collection<SalesInfoNote> loadNotesByPredecessorNoteId(long noteId);

  void insertSBSNote(SBSNote note);

  void insertGenericNote(GenericNote note);

  void insertSBSProductNote(SBSProductNote note);

  void insertSBSToDoGroupNote(ToDoGroupNote group);

  void insertFileAttachment(FileAttachment fileAttachment);

  void insertNoteAttribute(long noteId, long attributeId);

  void updateSBSNote(SBSNote note);

  void updateSBSProductNote(SBSProductNote note);

  void updateAttribute(Attribute attribute);

  void deleteFileAttachment(long fileAttachmentId);

  Collection<SBSOrgUnit> loadSBSOrgUnits();

  boolean hasSuccessorNote(long noteId);

  FileAttachment loadFileAttachmentById(long noteId, long attachmentId);

  void insertSalesConvNote(SalesConvNote note);

  void updateSalesConvNote(SalesConvNote note);

  SalesConvNote loadSalesConvNoteByNoteId(long noteId, boolean isExperimentalModeEnabled);

  void insertProductHistoryItem(ProductHistoryItem historyItem);

  String getTeamEmailAddress(long userId);

  void updateProductHistoryItem(ProductHistoryItem historyItem);

  void updateFileAttachmentNotesRelation(FileAttachment fileAttachment);

  void insertHistoryNote(HistoryNote historyNote);

  SalesInfoNote getNoteForHistoryByNoteId(Long predecessorSalesInfoNoteId);

  SalesInfoNote getProductNoteForHistoryByNoteId(Long predecessorSalesInfoNoteId);

  SalesInfoNote getToDoGroupNoteForHistoryByNoteId(Long predecessorSalesInfoNoteId);

  Collection<HistoryNote> getHistoryNotesByNoteId(Long predecessorSalesInfoNoteId);

  void insertSBSProduct(SBSProduct product);

  void updateSBSProduct(SBSProduct product);

  Collection<SBSProduct> loadAllSBSProducts();

  DigitalSellingNote loadDigitalSellingNoteByNoteId(long noteId);

  void insertDigitalSellingNote(DigitalSellingNote note);

}
