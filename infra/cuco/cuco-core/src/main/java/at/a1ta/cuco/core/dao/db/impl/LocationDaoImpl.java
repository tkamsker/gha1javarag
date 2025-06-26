package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.bite.data.clarify.shared.dto.Location;
import at.a1ta.cuco.core.dao.db.LocationDao;

public class LocationDaoImpl extends AbstractDao implements LocationDao {

  @SuppressWarnings("unchecked")
  @Override
  public Map<Long, Location> listLocations(List<Long> customerIds) {
    Map<String, Object> params = new HashMap<String, Object>(2);
    params.put("customerIds", customerIds);

    return (Map<Long, Location>) performMapQuery("Location.getLocations4Customers", params, "id");
  }

  @Override
  public Number getDistinctNrLocations4customer(long customerId) {
    return performObjectQuery("Location.CountDistinctLocations4customer", customerId);
  }
}
