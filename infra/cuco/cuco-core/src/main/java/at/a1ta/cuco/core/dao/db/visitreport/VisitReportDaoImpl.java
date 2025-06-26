package at.a1ta.cuco.core.dao.db.visitreport;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.shared.dto.Attribute;
import at.a1ta.cuco.core.shared.dto.AttributeConfig;
import at.a1ta.cuco.core.shared.dto.AttributeConfig.Groupings;
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

public class VisitReportDaoImpl extends AbstractDao implements VisitReportDao {

  @Override
  public Collection<SBSProduct> loadSBSProducts(SalesInfoNoteType type) {
    return performListQuery("VisitReport.loadSBSProducts", type.name());
  }

  @Override
  public Collection<SBSProduct> loadAllSBSProducts() {
    return performListQuery("VisitReport.loadAllSBSProducts");
  }

  @Override
  public String loadSBSProductConfig(String productId, SalesInfoNoteType type) {
    HashMap<String, String> params = new HashMap<String, String>();
    params.put("productId", productId);
    params.put("siNoteClass", type.name());
    return performObjectQuery("VisitReport.loadSBSProductConfig", params);
  }

  @Override
  public Collection<SBSProductNote> loadProductNotesByNote(long noteId, boolean experimentalModeEnabled) {
    if (experimentalModeEnabled) {
      return performListQuery("VisitReport.loadProductNotesByNote_Experimental", noteId);
    }
    return performListQuery("VisitReport.loadProductNotesByNote", noteId);
  }

  @Override
  public Collection<FileAttachment> loadFileAttachmentsByNote(long noteId) {
    return performListQuery("VisitReport.loadFileAttachmentsByNote", noteId);
  }

  @Override
  public GenericNote loadGenericNoteByNoteId(long noteId) {
    return performObjectQuery("VisitReport.loadGenericNoteByNoteId", noteId);
  }

  @Override
  public SBSNote loadSBSNoteByNoteId(long noteId, boolean isExperimentalModeEnabled) {
    return performObjectQuery("VisitReport.loadSBSNoteByNoteId_Experimental", noteId);
  }

  @Override
  public Collection<Attribute> loadSalesInfoAttributesByGrouping(String grouping) {
    return performListQuery("VisitReport.loadSalesInfoAttributesByGrouping", grouping);
  }

  @Override
  public Collection<SalesInfoNote> loadNotesByPredecessorNoteId(long noteId) {
    return performListQuery("VisitReport.loadNotesByPredecessorNoteId", noteId);
  }

  @Override
  public void insertSBSNote(SBSNote note) {
    executeInsert("VisitReport.insertSBSNote", note);
  }

  @Override
  public void insertGenericNote(GenericNote note) {
    executeInsert("VisitReport.insertGenericNote", note);
  }

  @Override
  public void insertSBSProductNote(SBSProductNote note) {
    executeInsert("VisitReport.insertSBSProductNote", note);
  }

  @Override
  public void insertFileAttachment(FileAttachment fileAttachment) {
    executeInsert("VisitReport.insertFileAttachment", fileAttachment);
  }

  @Override
  public void updateFileAttachmentNotesRelation(FileAttachment fileAttachment) {
    executeInsert("VisitReport.updateFileAttachmentNotesRelation", fileAttachment);
  }

  @Override
  public void insertSBSProduct(SBSProduct product) {
    executeInsert("VisitReport.insertSBSProduct", product);
  }

  @Override
  public void updateSBSProduct(SBSProduct product) {
    executeUpdate("VisitReport.updateSBSProduct", product);
  }

  @Override
  public void insertNoteAttribute(long noteId, long attributeId) {
    Map<String, Object> params = new HashMap<String, Object>(2);
    params.put("noteId", Long.valueOf(noteId));
    params.put("attributeId", attributeId);
    executeInsert("VisitReport.insertNoteAttribute", params);
  }

  @Override
  public void updateSBSNote(SBSNote note) {
    executeUpdate("VisitReport.updateSBSNote", note);
  }

  @Override
  public void updateSBSProductNote(SBSProductNote note) {
    executeUpdate("VisitReport.updateSBSProductNote", note);
  }

  @Override
  public void updateAttribute(Attribute attribute) {
    executeUpdate("VisitReport.updateAttribute", attribute);
  }

  @Override
  public void deleteFileAttachment(long fileAttachmentId) {
    executeDelete("VisitReport.deleteFileAttachment", fileAttachmentId);
  }

  @Override
  public Collection<SBSOrgUnit> loadSBSOrgUnits() {
    return performListQuery("VisitReport.loadSBSOrgUnits");
  }

  @Override
  public boolean hasSuccessorNote(long noteId) {
    return (Integer) performObjectQuery("VisitReport.hasSuccessorNote", noteId) > 0;
  }

  @Override
  public FileAttachment loadFileAttachmentById(long noteId, long attachmentId) {
    Map<String, Object> params = new HashMap<String, Object>(2);
    params.put("noteId", noteId);
    params.put("attachmentId", attachmentId);
    return performObjectQuery("VisitReport.loadFileAttachmentById", params);
  }

  @Override
  public void insertSalesConvNote(SalesConvNote note) {
    executeInsert("VisitReport.insertSalesConvNote", note);
  }

  @Override
  public void updateSalesConvNote(SalesConvNote note) {
    executeUpdate("VisitReport.updateSalesConvNote", note);
  }

  @Override
  public SalesConvNote loadSalesConvNoteByNoteId(long noteId, boolean isExperimentalModeEnabled) {
    if (isExperimentalModeEnabled) {
      return performObjectQuery("VisitReport.loadSalesConvNoteByNoteId_Experimental", noteId);
    }
    return performObjectQuery("VisitReport.loadSalesConvNoteByNoteId", noteId);
  }

  @Override
  public void insertProductHistoryItem(ProductHistoryItem historyItem) {
    executeInsert("VisitReport.insertProductHistoryItem", historyItem);
  }

  @Override
  public void updateProductHistoryItem(ProductHistoryItem historyItem) {
    executeUpdate("VisitReport.updateProductHistoryItemProductNoteID", historyItem);
  }

  @Override
  public String getTeamEmailAddress(long userId) {
    return performObjectQuery("VisitReport.getTeamEmailAddress", userId);
  }

  @Override
  public void insertSBSToDoGroupNote(ToDoGroupNote group) {
    executeInsert("VisitReport.insertToDoGroupNote", group);
  }

  @Override
  public void insertHistoryNote(HistoryNote historyNote) {
    executeInsert("VisitReport.insertHistoryNote", historyNote);
  }

  @Override
  public SalesInfoNote getNoteForHistoryByNoteId(Long predecessorSalesInfoNoteId) {
    return performObjectQuery("VisitReport.loadSBSNoteForHistoryByNoteId", predecessorSalesInfoNoteId);
  }

  @Override
  public SalesInfoNote getProductNoteForHistoryByNoteId(Long predecessorSalesInfoNoteId) {
    return performObjectQuery("VisitReport.loadProductNoteForHistoryByProductNoteId", predecessorSalesInfoNoteId);
  }

  @Override
  public SalesInfoNote getToDoGroupNoteForHistoryByNoteId(Long predecessorSalesInfoNoteId) {
    return performObjectQuery("VisitReport.getToDoGroupNoteForHistoryById", predecessorSalesInfoNoteId);
  }

  @Override
  public Collection<HistoryNote> getHistoryNotesByNoteId(Long predecessorSalesInfoNoteId) {
    return performListQuery("VisitReport.getHistoryNotesForVisitReportByVisitReportNoteId", predecessorSalesInfoNoteId);
  }

  @Override
  public DigitalSellingNote loadDigitalSellingNoteByNoteId(long noteId) {
    DigitalSellingNote note = performObjectQuery("VisitReport.loadDigitalSellingNoteByNoteId", noteId);
    if (note != null) {
      note.setAttributes(getDigitalSellingNoteAttributes(note.getSalesInfoNoteId()));
    }
    return note;
  }

  private ArrayList<Attribute> getDigitalSellingNoteAttributes(long noteId) {
    ArrayList<Attribute> attributes = new ArrayList<Attribute>();
    for (Groupings grouping : AttributeConfig.Groupings.values()) {
      if (grouping.name().startsWith("DIGITAL_SELLING_")) {
        HashMap<String, Object> params = new HashMap<String, Object>();
        params.put("si_note_id", noteId);
        params.put("grouping", grouping.name());
        Collection<? extends Attribute> groupAttributes = performListQuery("VisitReport.loadSalesInfoNoteAttributesByNoteIdAndGrouping", params);
        attributes.addAll(groupAttributes);
      }
    }
    return attributes;
  }

  @Override
  public void insertDigitalSellingNote(DigitalSellingNote note) {
    executeInsert("VisitReport.insertDigitalSellingNote", note);
  }

}
