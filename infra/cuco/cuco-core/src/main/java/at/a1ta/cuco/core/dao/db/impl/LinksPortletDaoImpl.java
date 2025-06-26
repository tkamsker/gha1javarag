package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.LinksPortletDao;
import at.a1ta.cuco.core.shared.dto.LinksPortlet;

public class LinksPortletDaoImpl extends AbstractDao implements LinksPortletDao {

  @Override
  public List<LinksPortlet> getAllLinks() {
    return performListQuery("LinksPortlet.getAllLinks");
  }

}
