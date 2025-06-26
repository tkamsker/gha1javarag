package at.a1ta.cuco.core.dao.util;

import java.sql.SQLException;

import org.apache.commons.lang.NotImplementedException;

import at.a1ta.cuco.core.shared.dto.IndexationStatus;

import com.ibatis.sqlmap.client.extensions.ParameterSetter;
import com.ibatis.sqlmap.client.extensions.ResultGetter;
import com.ibatis.sqlmap.client.extensions.TypeHandlerCallback;

public class IdxStatusDBMappingHandler implements TypeHandlerCallback {

  /**
   * From DB to Java.
   */
  @Override
  public Object getResult(ResultGetter getter) throws SQLException {
    final String dbValue = trim(getter.getString());
    return valueOf(dbValue);
  }

  /**
   * From Java to DB.
   */
  @Override
  public void setParameter(ParameterSetter arg0, Object arg1) throws SQLException {
    // read only
    throw new NotImplementedException();
  }

  /**
   * Converts DB value to the Java value.
   */
  @Override
  public Object valueOf(String s) {
    return IndexationStatus.getForDWHValue(s);
  }

  static String trim(String string) {
    return (string == null) ? null : string.trim();
  }

}
