package at.a1ta.cuco.core.dao.db.visitreport;

import java.sql.SQLException;
import java.util.HashSet;
import java.util.Set;

import org.apache.commons.lang.StringUtils;

import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SetupType;

import com.ibatis.sqlmap.client.extensions.ParameterSetter;
import com.ibatis.sqlmap.client.extensions.ResultGetter;

public class SetupTypeSetTypeHandler implements com.ibatis.sqlmap.client.extensions.TypeHandlerCallback {

  private static final String SEPARATOR = ";";

  @Override
  public Set<SetupType> getResult(ResultGetter getter) throws SQLException {
    String string = getter.getString();
    String[] array = string.split(SEPARATOR);
    Set<SetupType> set = new HashSet<SetupType>();
    for (String str : array) {
      set.add(SetupType.valueOf(str));
    }
    return set;
  }

  @SuppressWarnings("unchecked")
  @Override
  public void setParameter(ParameterSetter setter, Object parameter) throws SQLException {
    Set<SetupType> set = (Set<SetupType>) parameter;
    setter.setString(StringUtils.join(set.toArray(), SEPARATOR));
  }

  @Override
  public Object valueOf(String string) {
    String[] array = string.split(SEPARATOR);
    Set<SetupType> set = new HashSet<SetupType>();
    for (String str : array) {
      set.add(SetupType.valueOf(str));
    }
    return set;
  }
}