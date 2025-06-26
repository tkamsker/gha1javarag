package at.a1ta.cuco.core.export;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class BooleanFormater implements Formater {

  private static final Logger log = LoggerFactory.getLogger(BooleanFormater.class);

  private static final String DEFAULT_TRUE = "ja";

  private static final String DEFAULT_FALSE = "nein";

  private static final String DEFAULT_VALUE = "";

  private final String trueValue;

  private final String falseValue;

  private final String defaultValue;

  public BooleanFormater() {
    this(DEFAULT_TRUE, DEFAULT_FALSE, DEFAULT_VALUE);
  }

  public BooleanFormater(final String trueValue, final String falseValue, final String defaultValue) {
    this.trueValue = trueValue;
    this.falseValue = falseValue;
    this.defaultValue = defaultValue;
  }

  @Override
  public String format(final Object object) {
    try {
      return ((Boolean) object).booleanValue() ? trueValue : falseValue;
    } catch (Exception e) {
      log.warn("Could not parse value: " + object, e);
      return defaultValue;
    }
  }

}
