package at.a1ta.cuco.core.service.customerequipment;

import java.io.OutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import org.apache.commons.lang.time.FastDateFormat;
import org.apache.poi.hssf.usermodel.HSSFCell;
import org.apache.poi.hssf.usermodel.HSSFCellStyle;
import org.apache.poi.hssf.usermodel.HSSFFont;
import org.apache.poi.hssf.usermodel.HSSFFooter;
import org.apache.poi.hssf.usermodel.HSSFPrintSetup;
import org.apache.poi.hssf.usermodel.HSSFRow;
import org.apache.poi.hssf.usermodel.HSSFSheet;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.hssf.usermodel.HeaderFooter;
import org.apache.poi.hssf.util.HSSFColor;
import org.apache.poi.ss.usermodel.CellStyle;
import org.apache.poi.ss.usermodel.CreationHelper;
import org.apache.poi.ss.usermodel.Font;
import org.apache.poi.ss.util.CellRangeAddress;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.customerequipment.Equipment;
import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentSum;
import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentTree;

@Service
public class CustomerEquipmentExcelHelper {
  private static final Logger logger = LoggerFactory.getLogger(CustomerEquipmentExcelHelper.class);

  private static final String BLANK = " ";
  private static final String EMPTY = "";

  // Font settings
  private static final short[] FONT_SIZES = new short[] {20, 18, 16, 14, 13, 12, 11, 10};
  private static final short DEFAULT_FONT_SIZE = 12;

  // Date cells
  private static final String DATE_FORMAT = "dd.mm.yyyy"; // Excel date format for warrenty dates
  private static final FastDateFormat SDF = FastDateFormat.getInstance("dd.MM.yyyy"); // birthdate

  // HSSFCellStyle styles
  private static final String STYLE_DEFAULT_TREE_PARENT = "defaultTreeParent";
  private static final String STYLE_MAIN_TITLE = "mainTitle";
  private static final String STYLE_BOLD = "bold";
  private static final String STYLE_GRAY_BOLD = "grayBackgroundAndBoldFont";
  private static final String STYLE_ALIGN_RIGHT = "alignRight";
  private static final String STYLE_DATE = "date";
  private static final String STYLE_PARENT_NODE_DATE = "dateParentNode";
  private static final String STYLE_PARENT_NODE = "parentNode";
  private static final String STYLE_EQUIPMENT_GROUP = "equipmentGroup";

  // Column and field captions
  private static final String COL_MATERIAL_TITLE = "Bezeichnung";
  private static final String COL_MATERIAL_ID = "Materialnummer";
  private static final String COL_MATERIAL_COUNT = "Anzahl";
  private static final String COL_TREE_TITLE = "Bezeichnung";
  private static final String COL_TREE_ID = "EquipmentNr.";
  private static final String COL_TREE_STATUS = "Status";
  private static final String COL_TREE_SERIAL = "Seriennr.";
  private static final String COL_TREE_WARRENTY_BEGIN = "Gewährl. Beginn";
  private static final String COL_TREE_WARRENTY_END = "Gewährl. Ende";
  private static final String CUSTOMER_BIRTH_DATE = "Geburtsdatum: ";

  private static final String CUSTOMER_SEG = "Seg.: ";
  private static final String CUSTOMER_FBNR = "FBNR: ";
  private static final String CUSTOMER_ZVR = "ZVR: ";
  private static final String CUSTOMER_TYPE_PER = "Per";
  private static final String CUSTOMER_TYPE_ORG = "Org";

  // Sheet captions and general
  private static final String FOOTER_PAGE = "Seite ";
  private static final String CAPTION_CUSTOMER_ID = "KdNr.: ";
  private static final String CAPTION_PARTNER = "Warenempfänger: ";
  private static final String SHEET_TREE = "Inventarbaum";
  private static final String SHEET_MATERIAL = "Equipmentsummen";
  private static final String SHEET_TREE_TITLE = "Equipmentdaten";

  private static final String TOTAL_SUM = "Gesamtanzahl:";
  private static final String PREFIX_GROUP = "Übergeordnetes Equipment: ";

  /**
   * Writes the given EquipmentData object to an output stream using the the Excel format
   * 
   * @param out
   * @param data
   */
  public void streamExcelFile(final OutputStream stream, final EquipmentTree tree) {
    try {
      final HSSFWorkbook workbook = new HSSFWorkbook();
      final HSSFSheet sheetTree = workbook.createSheet(SHEET_TREE);
      final HSSFSheet sheetMaterial = workbook.createSheet(SHEET_MATERIAL);
      final Map<Object, HSSFCellStyle> styleMap = generateStyles(workbook);

      // Sheet: Tree
      initTreeSheet(sheetTree);

      buildTreeColumnHeaders(tree, sheetTree, styleMap);
      final ArrayList<Equipment> topLevels = tree.getChildren();
      for (final Equipment topLevel : topLevels) {
        visitTree(topLevel, sheetTree, workbook, styleMap);
      }
      autoSizeColumns(sheetTree, 6);

      // Sheet: Material
      buildMaterialColumnHeaders(sheetMaterial, styleMap);
      final ArrayList<EquipmentSum> materials = tree.getEquipmentSums();
      for (final EquipmentSum m : materials) {
        visitMaterial(m, sheetMaterial, workbook);
      }

      buildMaterialSums(sheetMaterial, styleMap);
      autoSizeColumns(sheetMaterial, 3);

      // write servlet response stream
      workbook.write(stream);
      stream.flush();
      stream.close();
    } catch (Exception e) {
      logger.error(e.getMessage(), e);
    } finally {
      try {
        stream.flush();
        stream.close();
      } catch (Exception e) {
        logger.error(e.getMessage(), e);
      }
    }
  }

  /**
   * Generates all needed HSSF styles
   * 
   * @param wb
   * @return HSSF Style map
   */
  private Map<Object, HSSFCellStyle> generateStyles(final HSSFWorkbook workbook) {
    final Map<Object, HSSFCellStyle> styleMap = new HashMap<Object, HSSFCellStyle>();
    final CreationHelper ch = workbook.getCreationHelper();

    // The tree sheet's main title style
    final HSSFCellStyle styleMainTitle = workbook.createCellStyle();
    final HSSFFont styleMainTitleFont = workbook.createFont();
    styleMainTitleFont.setFontHeightInPoints((short) 18);
    styleMainTitleFont.setBoldweight(Font.BOLDWEIGHT_BOLD);
    styleMainTitle.setFont(styleMainTitleFont);

    // Date style
    final HSSFCellStyle styleDate = workbook.createCellStyle();
    styleDate.setDataFormat(ch.createDataFormat().getFormat(DATE_FORMAT));

    // Gray background and bold
    final HSSFCellStyle styleGrayAndBold = workbook.createCellStyle();
    final HSSFFont hssfFontNormal = workbook.createFont();
    hssfFontNormal.setBoldweight(Font.BOLDWEIGHT_BOLD);
    styleGrayAndBold.setFont(hssfFontNormal);
    styleGrayAndBold.setFillPattern(CellStyle.SOLID_FOREGROUND);
    styleGrayAndBold.setFillForegroundColor(HSSFColor.GREY_25_PERCENT.index);

    // Equipment group
    final HSSFCellStyle styleEquipmentGroup = workbook.createCellStyle();
    final HSSFFont hssfFontSmall = workbook.createFont();
    hssfFontSmall.setFontHeightInPoints((short) 7);
    styleEquipmentGroup.setFont(hssfFontSmall);
    styleEquipmentGroup.setFillPattern(CellStyle.SOLID_FOREGROUND);
    styleEquipmentGroup.setFillForegroundColor(HSSFColor.GREY_25_PERCENT.index);

    // Equipment parent node
    final HSSFCellStyle styleParentNode = workbook.createCellStyle();
    styleParentNode.setFillPattern(CellStyle.SOLID_FOREGROUND);
    styleParentNode.setFillForegroundColor(HSSFColor.GREY_25_PERCENT.index);

    // styleParentNodeDate
    final HSSFCellStyle styleParentNodeDate = workbook.createCellStyle();
    styleParentNodeDate.setDataFormat(ch.createDataFormat().getFormat(DATE_FORMAT));
    styleParentNodeDate.setFillPattern(CellStyle.SOLID_FOREGROUND);
    styleParentNodeDate.setFillForegroundColor(HSSFColor.GREY_25_PERCENT.index);

    // Align right
    final HSSFCellStyle styleAlignRight = workbook.createCellStyle();
    styleAlignRight.setAlignment(CellStyle.ALIGN_RIGHT);

    // Bold
    final HSSFCellStyle styleBold = workbook.createCellStyle();
    final HSSFFont hssfFontBold = workbook.createFont();
    hssfFontBold.setBoldweight(Font.BOLDWEIGHT_BOLD);
    styleBold.setFont(hssfFontBold);

    styleMap.put(STYLE_MAIN_TITLE, styleMainTitle);
    styleMap.put(STYLE_DATE, styleDate);
    styleMap.put(STYLE_GRAY_BOLD, styleGrayAndBold);
    styleMap.put(STYLE_EQUIPMENT_GROUP, styleEquipmentGroup);
    styleMap.put(STYLE_ALIGN_RIGHT, styleAlignRight);
    styleMap.put(STYLE_BOLD, styleBold);
    styleMap.put(STYLE_PARENT_NODE, styleParentNode);
    styleMap.put(STYLE_PARENT_NODE_DATE, styleParentNodeDate);

    // Default tree parent style (will be taken when a deep tree level is given)
    final HSSFCellStyle styleDefaultParent = workbook.createCellStyle();
    final HSSFFont fontDefaultParent = workbook.createFont();
    fontDefaultParent.setFontHeightInPoints(DEFAULT_FONT_SIZE);
    fontDefaultParent.setBoldweight(Font.BOLDWEIGHT_BOLD);
    styleDefaultParent.setFont(fontDefaultParent);
    styleDefaultParent.setFillPattern(CellStyle.SOLID_FOREGROUND);
    styleDefaultParent.setFillForegroundColor(HSSFColor.GREY_25_PERCENT.index);
    styleMap.put(STYLE_DEFAULT_TREE_PARENT, styleDefaultParent);

    for (int i = 0; i < FONT_SIZES.length; i++) {
      final HSSFCellStyle treeLevelStyle = workbook.createCellStyle();
      final HSSFFont hssfFont = workbook.createFont();
      // calculate the font point size depending on the node's level in the tree
      final short height = i > (FONT_SIZES.length - 1) ? DEFAULT_FONT_SIZE : FONT_SIZES[i];
      hssfFont.setFontHeightInPoints(height);
      hssfFont.setBoldweight(Font.BOLDWEIGHT_BOLD);
      treeLevelStyle.setFont(hssfFont);
      treeLevelStyle.setFillPattern(CellStyle.SOLID_FOREGROUND);
      treeLevelStyle.setFillForegroundColor(HSSFColor.GREY_25_PERCENT.index);
      styleMap.put(i, treeLevelStyle);
    }

    return styleMap;
  }

  /**
   * Creates a new cell
   * 
   * @param treeLevel
   * @param styleMap
   * @return
   */
  private HSSFCellStyle getHSSFCellStyle(final int treeLevel, final Map<Object, HSSFCellStyle> styleMap) {
    if (treeLevel >= FONT_SIZES.length) {
      return styleMap.get(STYLE_DEFAULT_TREE_PARENT);
    }
    return styleMap.get(treeLevel);
  }

  /**
   * Creates a new cell
   * 
   * @param rowIdx
   * @param cellIdx
   * @param sheet
   * @return
   */
  private HSSFCell getCell(final int rowIdx, final int cellIdx, final HSSFSheet sheet) {
    return getCell(rowIdx, cellIdx, sheet, null);
  }

  private HSSFCell getCell(final int rowIdx, final int cellIdx, final HSSFSheet sheet, final HSSFCellStyle style) {
    HSSFRow row = sheet.getRow(rowIdx);
    if (row == null) {
      row = sheet.createRow(rowIdx);
    }
    HSSFCell cell = row.getCell(cellIdx);
    if (cell == null) {
      cell = row.createCell(cellIdx);
    }
    if (style != null) {
      cell.setCellStyle(style);
    }
    return cell;
  }

  /**
   * Builds one Equipment material row
   * 
   * @param material
   * @param sheet
   * @param wb
   */
  private void visitMaterial(final EquipmentSum material, final HSSFSheet sheet, final HSSFWorkbook wb) {
    final int rowCo = sheet.getLastRowNum() + 1;
    getCell(rowCo, 0, sheet).setCellValue(material.getTitle());
    getCell(rowCo, 1, sheet).setCellValue(material.getId());
    getCell(rowCo, 2, sheet).setCellValue(material.getCount());
  }

  /**
   * Build one Equipment item row and invokes the recursive visitTree method for its children items
   * 
   * @param node
   * @param sheet
   * @param wb
   * @param styleMap
   */
  private void visitTree(final Equipment node, final HSSFSheet sheet, final HSSFWorkbook wb, final Map<Object, HSSFCellStyle> styleMap) {
    int rowCo = sheet.getLastRowNum() + 1;

    if (node.hasChildren()) {
      final HSSFCellStyle parentNodeStyle = styleMap.get(STYLE_PARENT_NODE);
      final HSSFCellStyle parentNodeDateStyle = styleMap.get(STYLE_PARENT_NODE_DATE);
      final HSSFCellStyle parentNodeTitleStyle = getHSSFCellStyle(node.calculateTreeLevel(), styleMap);

      rowCo++; // empty line before every group
      setCells(rowCo, sheet, node, parentNodeTitleStyle, parentNodeStyle, parentNodeDateStyle);

      final Equipment myParent = node.getParent();
      if (myParent != null) {
        final HSSFCellStyle groupStyle = styleMap.get(STYLE_EQUIPMENT_GROUP);
        getCell(++rowCo, 0, sheet, groupStyle).setCellValue(PREFIX_GROUP + myParent.getName() + "; " + myParent.getId());
        getCell(rowCo, 1, sheet, groupStyle);
        getCell(rowCo, 2, sheet, groupStyle);
        getCell(rowCo, 3, sheet, groupStyle);
        getCell(rowCo, 4, sheet, groupStyle);
        getCell(rowCo, 5, sheet, groupStyle);
        sheet.getRow(rowCo).setHeightInPoints(11.0F);
      }

      final ArrayList<Equipment> children = node.getChildren();
      for (final Equipment child : children) {
        visitTree(child, sheet, wb, styleMap);
      }
    } else {
      setCells(rowCo, sheet, node, null, null, styleMap.get(STYLE_DATE));
    }
  }

  /**
   * Builds one row for an Equipment item
   * 
   * @param rowCo
   * @param sheet
   * @param node
   * @param nameStyle
   * @param otherStyle
   * @param dateStyle
   */
  private void setCells(final int rowCo, final HSSFSheet sheet, final Equipment node, final HSSFCellStyle nameStyle,
      final HSSFCellStyle otherStyle, final HSSFCellStyle dateStyle) {
    final HSSFCell name = getCell(rowCo, 0, sheet, nameStyle);
    final HSSFCell id = getCell(rowCo, 1, sheet, otherStyle);
    final HSSFCell status = getCell(rowCo, 2, sheet, otherStyle);
    final HSSFCell serial = getCell(rowCo, 3, sheet, otherStyle);
    final HSSFCell warrentyBegin = getCell(rowCo, 4, sheet, dateStyle);
    final HSSFCell warrentyEnd = getCell(rowCo, 5, sheet, dateStyle);

    if (node.getName() != null) {
      name.setCellValue(node.getName());
    }
    if (node.getId() != null) {
      id.setCellValue(node.getId());
    }
    if (node.getStatus() != null) {
      status.setCellValue(node.getStatus());
    }
    if (node.getSerialNumber() != null) {
      serial.setCellValue(node.getSerialNumber());
    }
    if (node.getWarrentyBegin() != null) {
      warrentyBegin.setCellValue(node.getWarrentyBegin());
    }
    if (node.getWarrentyEnd() != null) {
      warrentyEnd.setCellValue(node.getWarrentyEnd());
    }
  }

  private void initTreeSheet(final HSSFSheet sheet) {
    final HSSFPrintSetup ps = sheet.getPrintSetup();
    ps.setFitHeight(Short.MAX_VALUE); // if less than Short.MAX_VALUE pages are available than the available page count is the value
    ps.setFitWidth((short) 1);
    ps.setLandscape(true);
    sheet.setAutobreaks(true);
    sheet.setFitToPage(true);

    final HSSFFooter footer = sheet.getFooter();
    footer.setRight(FOOTER_PAGE + HeaderFooter.page() + " / " + HeaderFooter.numPages());
  }

  /**
   * Equipment material sheet - build SUM formular
   * 
   * @param sheetMaterial
   * @param styleMap
   */
  private void buildMaterialSums(final HSSFSheet sheetMaterial, final Map<Object, HSSFCellStyle> styleMap) {
    final HSSFCellStyle styleGrayBold = styleMap.get(STYLE_GRAY_BOLD);
    final int rowCo = sheetMaterial.getLastRowNum() + 1;
    getCell(rowCo, 0, sheetMaterial, styleGrayBold);
    getCell(rowCo, 1, sheetMaterial, styleGrayBold).setCellValue(TOTAL_SUM);
    getCell(rowCo, 2, sheetMaterial, styleGrayBold).setCellFormula("SUM(C2:C" + rowCo + ")");
  }

  /**
   * Auto size columns on a sheet
   * 
   * @param sheet
   * @param count
   */
  private void autoSizeColumns(final HSSFSheet sheet, final int count) {
    for (int i = 0; i < count; i++) {
      sheet.autoSizeColumn(i);
    }
  }

  /**
   * Builds a nice readable customer name
   * 
   * @param customer
   * @return
   */
  private String getCustomerName(final Party customer) {
    String name = EMPTY;
    if (customer.getSalutation() != null) {
      name += customer.getSalutation() + BLANK;
    }
    if (customer.getTitle() != null) {
      name += customer.getTitle() + BLANK;
    }
    if (customer.getFirstname() != null) {
      name += customer.getFirstname() + BLANK;
    }
    if (customer.getLastname() != null) {
      name += customer.getLastname();
    }
    return name;
  }

  /**
   * Equipment tree sheet - build column headers
   * 
   * @param info
   * @param sheet
   * @param styleMap
   */
  private void buildTreeColumnHeaders(final EquipmentTree data, final HSSFSheet sheet, final Map<Object, HSSFCellStyle> styleMap) {
    // Kundennr,Warenempfänger,Informationen merged cells
    sheet.addMergedRegion(new CellRangeAddress(0, 0, 0, 5));
    sheet.addMergedRegion(new CellRangeAddress(1, 1, 0, 5));
    sheet.addMergedRegion(new CellRangeAddress(2, 2, 0, 5));
    sheet.addMergedRegion(new CellRangeAddress(3, 3, 0, 5));
    sheet.addMergedRegion(new CellRangeAddress(4, 4, 0, 5));
    sheet.addMergedRegion(new CellRangeAddress(5, 5, 0, 5));
    sheet.addMergedRegion(new CellRangeAddress(6, 6, 0, 5));
    sheet.addMergedRegion(new CellRangeAddress(7, 7, 0, 5));
    sheet.addMergedRegion(new CellRangeAddress(8, 8, 0, 5));
    sheet.addMergedRegion(new CellRangeAddress(9, 9, 0, 5));
    sheet.addMergedRegion(new CellRangeAddress(10, 10, 0, 5));
    sheet.addMergedRegion(new CellRangeAddress(11, 11, 0, 5));

    final HSSFCellStyle styleBold = styleMap.get(STYLE_BOLD);

    int rowCo = 0;
    getCell(rowCo++, 0, sheet, styleMap.get(STYLE_MAIN_TITLE)).setCellValue(SHEET_TREE_TITLE);
    // getCell(rowCo++, 0, sheet).setCellValue(CAPTION_INFO + data.getInfoDetails());

    if (data.getEquipmentConsignee() != null) {
      rowCo++;
      getCell(rowCo++, 0, sheet, styleBold).setCellValue(CAPTION_PARTNER);
      getCell(rowCo++, 0, sheet).setCellValue(data.getEquipmentConsignee().getSummary());
    }

    final Party customer = data.getParty();
    if (customer != null) {
      rowCo++;
      getCell(rowCo++, 0, sheet).setCellValue(CAPTION_CUSTOMER_ID + customer.getCustomerNumber());
      getCell(rowCo++, 0, sheet).setCellValue(CUSTOMER_SEG + customer.getBusinessSegment());

      if (CUSTOMER_TYPE_PER.equals(customer.getCustomerType())) {
        getCell(rowCo++, 0, sheet).setCellValue(CUSTOMER_BIRTH_DATE + SDF.format(customer.getBirthdate()));

      } else if (CUSTOMER_TYPE_ORG.equals(customer.getCustomerType())) {
        if (customer.getCommercialRegisterNumber() != null) {
          getCell(rowCo++, 0, sheet).setCellValue(CUSTOMER_FBNR + customer.getCommercialRegisterNumber());
        }
        if (customer.getCentralAssociationNumber() != null) {
          getCell(rowCo++, 0, sheet).setCellValue(CUSTOMER_ZVR + customer.getCentralAssociationNumber());
        }
      }

      rowCo++;
      getCell(rowCo++, 0, sheet, styleBold).setCellValue(getCustomerName(customer));
      getCell(rowCo++, 0, sheet).setCellValue(customer.getAddressLine1() + BLANK + customer.getAddressLine2());
    }

    // Column captions
    getCell(++rowCo, 0, sheet, styleBold).setCellValue(COL_TREE_TITLE);
    getCell(rowCo, 1, sheet, styleBold).setCellValue(COL_TREE_ID);
    getCell(rowCo, 2, sheet, styleBold).setCellValue(COL_TREE_STATUS);
    getCell(rowCo, 3, sheet, styleBold).setCellValue(COL_TREE_SERIAL);
    getCell(rowCo, 4, sheet, styleBold).setCellValue(COL_TREE_WARRENTY_BEGIN);
    getCell(rowCo++, 5, sheet, styleBold).setCellValue(COL_TREE_WARRENTY_END);
  }

  /**
   * Equipment material sheet - build column headers
   * 
   * @param sheet
   * @param styleMap
   */
  private void buildMaterialColumnHeaders(final HSSFSheet sheet, final Map<Object, HSSFCellStyle> styleMap) {
    final HSSFCellStyle styleGrayBold = styleMap.get(STYLE_GRAY_BOLD);

    // Column captions
    getCell(0, 0, sheet, styleGrayBold).setCellValue(COL_MATERIAL_TITLE);
    getCell(0, 1, sheet, styleGrayBold).setCellValue(COL_MATERIAL_ID);
    getCell(0, 2, sheet, styleGrayBold).setCellValue(COL_MATERIAL_COUNT);
  }
}
