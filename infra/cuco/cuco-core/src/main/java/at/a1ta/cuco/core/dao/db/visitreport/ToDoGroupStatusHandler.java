package at.a1ta.cuco.core.dao.db.visitreport;

import java.sql.SQLException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import at.a1ta.cuco.core.shared.dto.salesinfo.ToDoGroupNote.ToDoStatus;

import com.ibatis.sqlmap.client.extensions.ParameterSetter;
import com.ibatis.sqlmap.client.extensions.ResultGetter;

public class ToDoGroupStatusHandler implements com.ibatis.sqlmap.client.extensions.TypeHandlerCallback {

  private static final Logger logger = LoggerFactory.getLogger(ToDoGroupStatusHandler.class);

  /**
   * From DB to Java.
   */
  @Override
  public ToDoStatus getResult(ResultGetter getter) throws SQLException {
    final String dbValue = trim(getter.getString());
    return valueOf(dbValue);
  }

  /**
   * From Java to DB.
   */
  @Override
  public void setParameter(ParameterSetter setter, Object set) throws SQLException {
    setter.setString(set.toString());
  }

  /**
   * Converts DB value to the Java value.
   */
  @Override
  public ToDoStatus valueOf(String s) {
    try {
      return ToDoStatus.valueOf(s);
    } catch (Exception ex) {
      logger.error("Error while defining filter for the key " + s, ex);
      return ToDoStatus.CREATED;
    }
  }

  static String trim(String string) {
    return (string == null) ? null : string.trim();
  }

}