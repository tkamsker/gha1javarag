/*
 * Copyright 2009 - 2012 by A1 Telekom Austria AG
 * All Rights Reserved.
 * 
 * The Software is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * All information contained herein is, and remains the property of
 * A1 Telekom Austria AG and its suppliers, if any.
 * The intellectual and technical concepts contained herein are proprietary
 * to A1 Telekom Austria AG and its suppliers and may be covered by
 * intertional or national patents, patents in process, and are protected
 * by trade secret or copyright law. Dissemination of this information or
 * reproduction of this material is strictly forbidden unless prior written
 * permission is obtained from A1 Telekom Austria AG.
 */
package at.a1ta.cuco.core.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import at.a1ta.bite.data.clarify.shared.dto.Location;
import at.a1ta.bite.data.clarify.shared.dto.LocationCollection;
import at.a1telekom.eai.lkmslocation.AddressDetail;

public interface LocationService {

  LocationCollection getClarifyLocationsForCustomer(Long customerId, int locationPageSize, int locationPageIndex);

  Number getDistinctNrLocations4customer(Number customerId);

  Page<Location> getClarifyLocationsForCustmomer(Long customerId, Pageable pageable);

  AddressDetail getAddressDetailForLocation(String lkmsId);
}
