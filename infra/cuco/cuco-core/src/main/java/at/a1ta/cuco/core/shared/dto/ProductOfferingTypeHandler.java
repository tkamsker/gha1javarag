package at.a1ta.cuco.core.shared.dto;

import java.sql.CallableStatement;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import at.a1ta.cuco.core.shared.dto.ProductOffering;

import com.ibatis.sqlmap.engine.type.BaseTypeHandler;

public class ProductOfferingTypeHandler extends BaseTypeHandler {
  @Override
  public void setParameter(PreparedStatement ps, int i, Object parameter, String jdbcType) throws SQLException {
    ps.setString(i, parameter.toString());
  }

  @Override
  public Object getResult(ResultSet rs, String columnName) throws SQLException {
    Long id = rs.getLong(columnName);
    if (rs.wasNull()) {
      return null;
    } else {
      return ProductOffering.valueOf(id);
    }
  }

  @Override
  public Object getResult(ResultSet rs, int columnIndex) throws SQLException {
    Long id = rs.getLong(columnIndex);
    if (rs.wasNull()) {
      return null;
    } else {
      return ProductOffering.valueOf(id);
    }
  }

  @Override
  public Object getResult(CallableStatement cs, int columnIndex) throws SQLException {
    Long id = cs.getLong(columnIndex);
    if (cs.wasNull()) {
      return null;
    } else {
      return ProductOffering.valueOf(id);
    }
  }

  @Override
  public Object valueOf(String s) {
    return ProductOffering.valueOf(s);
  }
}
