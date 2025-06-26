package at.a1ta.cuco.core.shared.dto;

public class VipExport {
  public static final String SEARCH_VIP_STATUS = "vipStatus";
  public static final String SEARCH_REPORTER = "search";
  public static final String SEARCH_TO = "to";
  public static final String SEARCH_FROM = "from";
  public static final String SERIALIZATION_DATE_PATTERN = "dd.MM.yyyy.HH.mm.ss.SSS";
  public static final Object[] EXPORT_ROW_TITLES = new Object[] {"Kundennummer", "Titel", "Nachname", "Vorname", "VIP Status", "Reporter",
      "Anlege Datum", "Segment", "PLZ", "Ort", "Strasse", "Hausnummer", "E-Mail", "Geburtsdatum", "Geschlecht", "Branche"};
  public static final String EXPORT_ACTION_CSV_BY_SEARCH = "csvBySearch";
  public static final String EXPORT_CSV_EXT = ".csv";
  public static final String EXPORT_CSV_CONTENT_TYPE = "application/CSV";
  public static final String EXPORT_DATE_PATTERN = "dd.MM.yyyy HH:mm";
  public static final String EXPORT_DATE_FILE_PATTERN = "dd-MM-yyyy_HH-mm";
}
