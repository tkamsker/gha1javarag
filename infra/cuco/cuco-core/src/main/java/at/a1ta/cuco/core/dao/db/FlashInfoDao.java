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
package at.a1ta.cuco.core.dao.db;

import java.util.Collection;
import java.util.List;
import java.util.Map;

import at.a1ta.cuco.core.shared.dto.FlashInfo;
import at.a1ta.cuco.core.shared.dto.Tupel;

public interface FlashInfoDao {

  FlashInfo getFlashInfoById(long flashId);

  List<FlashInfo> getAllFlashInfos();

  List<FlashInfo> getFlashInfoForUserAndCustomer(long userId, long customerId);

  void insertFlashInfo(FlashInfo flashInfo);

  void updateFlashInfo(FlashInfo flashInfo);

  void deleteFlashInfo(long flashId);

  /**
   * @param collection the first value has to be the ID of the flash and the second the customer number
   */
  void insertFlashCustomer(Collection<Tupel<Long, Long>> collection);

  void deleteFlashCustomerForFlash(long flashId);

  void insertFlashRole(long flashInfoId, String roleId);

  void deleteFlashRoleForFlash(long flashId);

  void insertFlashViewed(long flashInfoId, long customerId, long userId);

  List<FlashInfo> loadMyFlashInfos(Map<String, Object> params);

}