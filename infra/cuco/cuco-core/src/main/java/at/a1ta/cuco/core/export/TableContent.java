package at.a1ta.cuco.core.export;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class TableContent implements ExportContent {

  private static final int DEFAULT_ROW_LEN = 128; // performance influence for the StringBuilder

  private List<List<Object>> table = new ArrayList<List<Object>>();

  private Formater nullFormater = new NullFormater();

  private Map<Class<?>, Formater> typeFormaters = new HashMap<Class<?>, Formater>();

  private Map<Integer, Formater> columnFormaters = new HashMap<Integer, Formater>();

  private Formater rowFormater;

  private Formater contentFormater;

  public TableContent() {
    typeFormaters.put(Date.class, new DateFormater());
    typeFormaters.put(Boolean.class, new BooleanFormater());
    typeFormaters.put(null, new NullFormater());
  }

  @Override
  public void setTypeFormater(final Class<?> clazz, final Formater formater) {
    typeFormaters.put(clazz, formater);
  }

  @Override
  public void setRowFormater(final Formater formater) {
    rowFormater = formater;
  }

  @Override
  public void setColumnFormater(final int column, final Formater formater) {
    columnFormaters.put(column, formater);
  }

  public void setColumnFormater(final int startColumn, final int endColumn, final Formater formater) {
    for (int i = startColumn; i <= endColumn; i++) {
      columnFormaters.put(i, formater);
    }
  }

  @Override
  public void clear() {
    table.clear();
  }

  @Override
  public int addRow(final Object... columnValues) {
    final List<Object> columns = Arrays.asList(columnValues);
    table.add(columns);
    return table.size() - 1;
  }

  @Override
  public int setRow(final int row, final Object... columnValues) {
    final List<Object> columns = Arrays.asList(columnValues);
    // TODO manuels check if the index is correct
    table.set(row, columns);
    return row;
  }

  @Override
  public String asString() {
    final StringBuilder sbContent = new StringBuilder(table.size() * DEFAULT_ROW_LEN);

    for (final List<Object> row : table) {
      int curColIdx = 0;

      final StringBuilder sbRow = new StringBuilder(DEFAULT_ROW_LEN);
      for (final Object cell : row) {
        sbRow.append(format(cell, curColIdx));
        curColIdx++;
      }
      sbContent.append(rowFormater.format(sbRow));
    }

    if (contentFormater != null) {
      return contentFormater.format(sbContent);
    }
    return sbContent.toString();
  }

  private String format(final Object value, final int curCellIdx) {
    final Class<?> clazz = value == null ? null : value.getClass();
    Formater formater = clazz == null ? nullFormater : typeFormaters.get(clazz);
    if (formater == null) {
      formater = nullFormater;
    }

    final String content = formater.format(value);
    final Formater columnFormater = columnFormaters.get(curCellIdx);
    if (columnFormater != null) {
      return columnFormater.format(content);
    }
    return content;
  }

  @Override
  public void setContentFormater(final Formater formater) {
    this.contentFormater = formater;
  }
}
