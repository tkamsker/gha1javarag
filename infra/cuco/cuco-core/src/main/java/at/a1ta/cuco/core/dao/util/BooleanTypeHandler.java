package at.a1ta.cuco.core.dao.util;

import java.sql.SQLException;

import com.ibatis.sqlmap.client.extensions.ParameterSetter;
import com.ibatis.sqlmap.client.extensions.ResultGetter;
import com.ibatis.sqlmap.client.extensions.TypeHandlerCallback;

public class BooleanTypeHandler implements TypeHandlerCallback {

  /** Indicates 1 or true. */
  static final String TRUE_STRING = "1";

  /** Indicates 0 or false. */
  static final String FALSE_STRING = "0";

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
      return Boolean.TRUE;
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