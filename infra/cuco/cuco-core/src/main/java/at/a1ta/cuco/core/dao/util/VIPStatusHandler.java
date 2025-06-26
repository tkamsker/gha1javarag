package at.a1ta.cuco.core.dao.util;

import java.sql.SQLException;

import org.apache.commons.lang.NotImplementedException;

import at.a1ta.cuco.core.shared.dto.VipStatus;
import at.a1ta.cuco.core.shared.dto.VipStatus.State;

import com.ibatis.sqlmap.client.extensions.ParameterSetter;
import com.ibatis.sqlmap.client.extensions.ResultGetter;
import com.ibatis.sqlmap.client.extensions.TypeHandlerCallback;

public class VIPStatusHandler implements TypeHandlerCallback {

  static final String TRUE_STRING = "J";

  static final String FALSE_STRING = "N";

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
    if (s == null) {
      return new VipStatus(State.UNKNOWN);
    }
    final String value = trim(s);
    if (TRUE_STRING.equals(value)) {
      return new VipStatus(State.VIP);
    }
    return new VipStatus(State.NO_VIP);
  }

  static String trim(String string) {
    return (string == null) ? null : string.trim();
  }

}
