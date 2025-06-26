package at.a1ta.cuco.core.service.impl;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.util.Assert;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.data.clarify.dao.ClarifyInteractionAndWorkflowDao;
import at.a1ta.bite.data.clarify.shared.dto.Location;
import at.a1ta.bite.data.clarify.shared.dto.LocationCollection;
import at.a1ta.cuco.core.dao.db.LocationDao;
import at.a1ta.cuco.core.service.LocationService;
import at.a1ta.cuco.core.service.customerequipment.ProductBrowserServiceImpl;
import at.a1telekom.eai.lkmslocation.AddressDetail;
import at.a1telekom.eai.lkmslocation.GetAddressRequest;
import at.a1telekom.eai.lkmslocation.GetAddressRequestDocument;
import at.a1telekom.eai.lkmslocation.GetAddressResponse;
import at.a1telekom.eai.lkmslocation.GetAddressResponseDocument;

import com.telekomaustriagroup.esb.lkmslocation.LKMSLocationStub;

@Service
public class LocationServiceImpl extends BaseEsbClient<LKMSLocationStub> implements LocationService {

  private static final Logger logger = LoggerFactory.getLogger(ProductBrowserServiceImpl.class);

  private LocationDao locationDao;

  private ClarifyInteractionAndWorkflowDao clarifyInteractionAndWorkflowDao;

  public LocationServiceImpl() {

  }

  @Autowired
  public LocationServiceImpl(LocationDao locationDao) {
    if (locationDao == null) {
      throw new org.apache.commons.lang.NullArgumentException("locationDao");
    }
    this.locationDao = locationDao;
  }

  @Override
  public Number getDistinctNrLocations4customer(Number customerId) {
    if (customerId == null) {
      throw new org.apache.commons.lang.NullArgumentException("customerId");
    }
    return this.locationDao.getDistinctNrLocations4customer(customerId.longValue());
  }

  @Override
  public LocationCollection getClarifyLocationsForCustomer(Long customerId, int locationPageSize, int locationPageIndex) {
    return clarifyInteractionAndWorkflowDao.getLocationList(customerId, locationPageSize, locationPageIndex);
  }

  @Override
  public Page<Location> getClarifyLocationsForCustmomer(Long customerId, Pageable pageable) {
    Assert.notNull(customerId);
    Pageable pageRequest = pageable != null ? pageable : new PageRequest(0, 10);
    return clarifyInteractionAndWorkflowDao.findLocationsByCustomerId(customerId, pageRequest);
  }

  @Autowired
  public void setClarifyInteractionAndWorkflowDao(ClarifyInteractionAndWorkflowDao clarifyInteractionAndWorkflowDao) {
    this.clarifyInteractionAndWorkflowDao = clarifyInteractionAndWorkflowDao;
  }

  @Override
  public AddressDetail getAddressDetailForLocation(String lkmsId) {
    if (lkmsId != null) {
      try {
        GetAddressRequestDocument reqDoc = GetAddressRequestDocument.Factory.newInstance();
        GetAddressRequest req = GetAddressRequest.Factory.newInstance();
        req.setSourceSystem("CUCO"); // TODO externalize to db setting
        req.setUser("UCUCO1");// TODO externalize to db setting
        req.setLkmsId(lkmsId);

        reqDoc.setGetAddressRequest(req);

        GetAddressResponseDocument respDoc = stub.getAddress(reqDoc, null);
        GetAddressResponse resp = respDoc.getGetAddressResponse();

        return resp.getAddressDetail();

      } catch (Exception e) {
        logger.error(e.getMessage(), e);
        throw new RuntimeException("An error occurred during the getAddress call: " + e.getMessage(), e);
      }
    }
    return null;
  }
}
