package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.CategoryDao;
import at.a1ta.cuco.core.shared.dto.Category;

public class CategoryDaoImpl extends AbstractDao implements CategoryDao {

  @Override
  public List<Category> listCategories() {
    return performListQuery("SegCategory.list");
  }
}
