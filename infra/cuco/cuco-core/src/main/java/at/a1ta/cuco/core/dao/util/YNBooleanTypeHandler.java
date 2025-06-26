package at.a1ta.cuco.core.dao.util;

import java.sql.SQLException;

import com.ibatis.sqlmap.client.extensions.ParameterSetter;
import com.ibatis.sqlmap.client.extensions.ResultGetter;
import com.ibatis.sqlmap.client.extensions.TypeHandlerCallback;

/**
 * An iBATIS type handler callback for java.lang.Booleans that are mapped to either 'Y' or 'N' in the database. If a
 * value is something other than 'Y' in the database, including <code>null</code>, the resulting Boolean will be false.
 * <p>
 * DB --> Java ---------------- 'Y' true null false 'N' false 'blah' false Java --> DB ---------------- null 'N' false 'N' true 'Y'
 */
public class YNBooleanTypeHandler implements TypeHandlerCallback {

  /** Indicates Yes or true. */
  static final String TRUE_STRING = "J";

  /** Indicates No or false. */
  static final String FALSE_STRING = "N";

  /**
   * From Java to DB.
   */
  @Override
  public void setParameter(ParameterSetter setter, Object parameter) throws SQLException {
    if (parameter == null) {
      setter.setString(FALSE_STRING);
      return;
    }

    final Boolean bool = (Boolean) parameter;

    if (bool.booleanValue()) {
      setter.setString(TRUE_STRING);
    } else {
      setter.setString(FALSE_STRING);
    }
  }

  /**
   * From DB to Java.
   */
  @Override
  public Object getResult(ResultGetter getter) throws SQLException {
    final String dbValue = trim(getter.getString());

    final Object result = valueOf(dbValue);

    return result;
  }

  /**
   * Converts DB value to the Java value.
   */
  @Override
  public Object valueOf(String s) {
    if (s == null) {
      return Boolean.FALSE;
    }

    final String value = trim(s);

    if (TRUE_STRING.equals(value)) {
      return Boolean.TRUE;
    }

    return Boolean.FALSE;
  }

  /**
   * Trims the String if not null.
   */
  static String trim(String string) {
    return (string == null) ? null : string.trim();
  }
}