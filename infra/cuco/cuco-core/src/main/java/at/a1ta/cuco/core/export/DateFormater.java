package at.a1ta.cuco.core.export;

import org.apache.commons.lang.time.FastDateFormat;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DateFormater implements Formater {

  private static final Logger log = LoggerFactory.getLogger(DateFormater.class);

  protected static final String DEFAULT_PATTERN = "dd.MM.yyy hh:mm";

  protected static final String DEFAULT_VALUE = "";

  private final FastDateFormat sdf;

  private final String defaultValue;

  public DateFormater() {
    this(DEFAULT_PATTERN, DEFAULT_VALUE);
  }

  public DateFormater(final String dateFormat, final String defaultValue) {
    this.sdf = FastDateFormat.getInstance(dateFormat);
    this.defaultValue = defaultValue;
  }

  @Override
  public String format(final Object object) {
    try {
      return sdf.format(object);
    } catch (Exception e) {
      log.warn("Could not parse value: " + object, e);
      return defaultValue;
    }
  }

}
