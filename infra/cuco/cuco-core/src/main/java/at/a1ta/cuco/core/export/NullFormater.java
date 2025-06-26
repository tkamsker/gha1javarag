package at.a1ta.cuco.core.export;

public class NullFormater implements Formater {

  private static final String DEFAULT_VALUE = "";

  private final String defaultValue;

  public NullFormater() {
    this(DEFAULT_VALUE);
  }

  public NullFormater(final String defaultValue) {
    this.defaultValue = defaultValue;
  }

  @Override
  public String format(final Object object) {
    return object == null ? defaultValue : object.toString();
  }

}
