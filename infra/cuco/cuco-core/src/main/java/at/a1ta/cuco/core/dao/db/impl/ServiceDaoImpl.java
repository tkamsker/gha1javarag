package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.ServiceDao;
import at.a1ta.cuco.core.shared.dto.Service;

public class ServiceDaoImpl extends AbstractDao implements ServiceDao {

  @Override
  public void insertService(Service service) {
    executeInsert("Service.insert", service);
  }

  @Override
  public void deleteService(Long serviceId) {
    executeDelete("Service.delete", serviceId);
  }

  @Override
  public List<Service> getAllServices() {
    return performListQuery("Service.get");
  }

  @Override
  public void updateService(Service service) {
    executeUpdate("Service.update", service);
  }

  @Override
  public List<Service> getValidForUser(Long userId) {
    return performListQuery("Service.getValidForUser", userId);
  }

  @Override
  public List<Service> searchService(String service) {
    return performListQuery("Service.search", service);
  }
}
