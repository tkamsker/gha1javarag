package at.a1ta.cuco.core.dao.db;

import java.util.Collection;

import at.a1ta.cuco.core.shared.dto.StandardAddress;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.Country;

public interface StandardAddressDao {

  StandardAddress getAddress(long addressId);

  StandardAddress getAddressByLkmsIdAndPartyId(String lkmsId, long partyId);

  void insertAddress(StandardAddress address);

  void updateAddress(StandardAddress address);

  Collection<Country> loadCountries();
}
