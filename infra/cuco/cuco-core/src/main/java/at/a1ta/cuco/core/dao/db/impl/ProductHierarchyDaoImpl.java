package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.ProductHierarchyDao;
import at.a1ta.cuco.core.shared.dto.ProductHierarchy;

public class ProductHierarchyDaoImpl extends AbstractDao implements ProductHierarchyDao {

  @Override
  public List<ProductHierarchy> getProductHierarchy() {
    return performListQuery("ProductHierarchy.get");
  }
}
