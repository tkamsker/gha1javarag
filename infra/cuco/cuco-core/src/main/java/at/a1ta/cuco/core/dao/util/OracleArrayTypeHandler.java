package at.a1ta.cuco.core.dao.util;

import java.sql.SQLException;
import java.util.List;

import com.ibatis.sqlmap.client.extensions.ParameterSetter;
import com.ibatis.sqlmap.client.extensions.ResultGetter;

public class OracleArrayTypeHandler implements com.ibatis.sqlmap.client.extensions.TypeHandlerCallback {

  @Override
  public Object getResult(ResultGetter getter) throws SQLException {
    List<Object> list;
    java.sql.Array array = getter.getArray();
    int baseType = array.getBaseType();
    if (baseType == java.sql.Types.VARCHAR || baseType == java.sql.Types.NUMERIC) {
      Object[] elements = (Object[]) array.getArray();
      list = java.util.Arrays.asList(elements);
    } else {
      throw new java.lang.IllegalArgumentException("Unknown type (" + array.getBaseTypeName() + ") for conversion.");
    }
    return list;
  }

  @Override
  public void setParameter(ParameterSetter arg0, Object arg1) throws SQLException {}

  @Override
  public Object valueOf(String arg0) {
    return null;
  }

}
