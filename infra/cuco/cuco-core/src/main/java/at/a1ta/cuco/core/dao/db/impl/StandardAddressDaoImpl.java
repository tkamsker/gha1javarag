package at.a1ta.cuco.core.dao.db.impl;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.StandardAddressDao;
import at.a1ta.cuco.core.shared.dto.StandardAddress;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.Country;

public class StandardAddressDaoImpl extends AbstractDao implements StandardAddressDao {

  @Override
  public StandardAddress getAddress(long addressId) {
    return performObjectQuery("StandardAddress.getAddress", addressId);
  }

  @Override
  public StandardAddress getAddressByLkmsIdAndPartyId(String lkmsId, long partyId) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("lkmsId", lkmsId);
    params.put("partyId", partyId);
    return performObjectQuery("StandardAddress.getAddressByLkmsIdAndPartyId", params);
  }

  @Override
  public void insertAddress(StandardAddress address) {
    executeInsert("StandardAddress.insertAddress", address);

  }

  @Override
  public void updateAddress(StandardAddress address) {
    executeUpdate("StandardAddress.updateAddress", address);

  }

  @Override
  public Collection<Country> loadCountries() {
    return performListQuery("StandardAddress.loadCountries");
  }
}
