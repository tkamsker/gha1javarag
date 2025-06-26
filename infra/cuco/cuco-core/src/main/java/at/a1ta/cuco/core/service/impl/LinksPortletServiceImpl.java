package at.a1ta.cuco.core.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.db.LinksPortletDao;
import at.a1ta.cuco.core.service.LinksPortletService;
import at.a1ta.cuco.core.shared.dto.LinksPortlet;

@Service
public class LinksPortletServiceImpl implements LinksPortletService {

  private LinksPortletDao linksPortletDao;

  @Override
  public List<LinksPortlet> getAllLinks() {
    return linksPortletDao.getAllLinks();
  }

  @Autowired
  public void setLinksPortletDao(LinksPortletDao linksPortletDao) {
    this.linksPortletDao = linksPortletDao;
  }

}
