package at.a1ta.cuco.core.export;

public interface ExportContent {

  public void setTypeFormater(final Class<?> clazz, final Formater formater);

  public void setColumnFormater(final int column, final Formater formater);

  public void setRowFormater(final Formater formater);

  public void setContentFormater(final Formater formater);

  public void clear();

  public int addRow(final Object... columnValues);

  public int setRow(final int row, final Object... columnValues);

  public String asString();
}
