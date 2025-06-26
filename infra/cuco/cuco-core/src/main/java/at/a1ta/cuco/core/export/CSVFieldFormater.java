package at.a1ta.cuco.core.export;

public class CSVFieldFormater implements Formater {

  // Good example for formating and escaping CSV values: http://en.wikipedia.org/wiki/Comma-separated_values#Example

  public static final String SEPERATOR_DEFAULT_RFC4180 = ",";

  public static final String SEPERATOR = ";";

  private static final String EMPTY = "";

  // private static final String REGEX_LINE_FEEDS = "\\r|\\n";

  private static final String CR = "\r";

  private static final String LF = "\n";

  private static final String QUOTE = "\"";

  private static final String QUOTE_ESCAPED = "\"\"";

  @Override
  public String format(final Object object) {
    return escapeText(object) + SEPERATOR; // TODO escape the seperator
  }

  private String escapeText(final Object original) {
    if (original == null) {
      return null;
    }
    String escaped = original.toString();
    // escaoe a COMMA
    if (escaped.contains(QUOTE)) {
      escaped = escaped.replaceAll(QUOTE, QUOTE_ESCAPED);
    }

    // sorround the field by COMMAs when a seperator or a CRLF or a LF is part of the field or the field is an empty string
    if (escaped.contains(SEPERATOR_DEFAULT_RFC4180) || escaped.contains(SEPERATOR) || escaped.contains(LF) || escaped.contains(CR)
        || escaped.contains(QUOTE) || escaped.equals(EMPTY)) {
      escaped = QUOTE + escaped + QUOTE;
    }

    return escaped;
  }
}
