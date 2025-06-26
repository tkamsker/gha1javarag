package at.a1ta.cuco.core.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.cuco.core.dao.db.ServiceDao;
import at.a1ta.cuco.core.service.ServiceService;
import at.a1ta.cuco.core.shared.dto.Service;

@org.springframework.stereotype.Service
public class ServiceServiceImpl implements ServiceService {

  private ServiceDao serviceDao;

  @Override
  public void deleteService(Long id) {
    serviceDao.deleteService(id);
  }

  @Override
  public List<Service> getAllServices() {
    return serviceDao.getAllServices();
  }

  @Override
  public void saveService(Service service) {
    if (service.getId() == null) {
      serviceDao.insertService(service);
    } else {
      serviceDao.updateService(service);
    }
  }

  @Override
  public List<Service> getValidForUser(Long userId) {
    return serviceDao.getValidForUser(userId);
  }

  @Autowired
  public void setServiceDao(ServiceDao serviceDao) {
    this.serviceDao = serviceDao;
  }

  @Override
  public List<Service> searchService(String service) {
    return serviceDao.searchService(service);
  }
}
