package at.a1ta.cuco.core.export;

import org.apache.commons.lang.StringUtils;

public class CSVRowFormater implements Formater {

  private static final String LINE_BREAK = "\r\n";

  private final String seperator;

  public CSVRowFormater() {
    this(LINE_BREAK);
  }

  public CSVRowFormater(final String seperator) {
    this.seperator = seperator;
  }

  @Override
  public String format(final Object object) {
    String str = (object == null ? StringUtils.EMPTY : object.toString());
    final int lastSepIdx = str.lastIndexOf(CSVFieldFormater.SEPERATOR);
    if (lastSepIdx >= 0) {
      str = str.substring(0, lastSepIdx);
    }
    return str + seperator;
  }
}
