package at.a1ta.cuco.core.dao.util;

import java.sql.SQLException;
import java.util.Arrays;
import java.util.List;

import org.apache.commons.lang.StringUtils;

import com.ibatis.sqlmap.client.extensions.ParameterSetter;
import com.ibatis.sqlmap.client.extensions.ResultGetter;

public class ListStringTypeHandler implements com.ibatis.sqlmap.client.extensions.TypeHandlerCallback {

  @Override
  @SuppressWarnings("unchecked")
  public List<String> getResult(ResultGetter getter) throws SQLException {
    String string = getter.getString();
    return Arrays.asList(string.split(";"));
  }

  @Override
  @SuppressWarnings("unchecked")
  public void setParameter(ParameterSetter setter, Object parameter) throws SQLException {
    List<String> list = (List<String>) parameter;
    setter.setString(StringUtils.join(list, ";"));

  }

  @Override
  @SuppressWarnings("unchecked")
  public Object valueOf(String string) {
    return Arrays.asList(string.split(";"));
  }

}