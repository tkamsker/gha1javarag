package at.a1ta.cuco.core.dao.util;

import java.sql.SQLException;

import com.ibatis.sqlmap.client.extensions.ParameterSetter;

/**
 * @author christoph.strobl@telekom.at
 * 
 * 
 *         An iBATIS type handler callback for java.lang.Booleans that are mapped to either 'Y' or 'N' in the database.
 *         If a value is something other than 'Y' in the database, including <code>null</code>, the resulting Boolean
 *         will be false.
 * 
 *         DB --> Java ---------------- 'J' true null null 'N' false 'blah' false
 * 
 *         Java --> DB ---------------- null null false 'N' true 'J'
 */
public class YNNullableBooleanTypeHandler extends YNBooleanTypeHandler {

    @Override
    public Object valueOf(String s) {
        if (s == null) {
            return null;
        }
        return super.valueOf(s);
    }

    @Override
    public void setParameter(ParameterSetter setter, Object parameter) throws SQLException {
        if (parameter == null) {
            setter.setNull(java.sql.Types.VARCHAR);
            return;
        }
        super.setParameter(setter, parameter);
    }
}
