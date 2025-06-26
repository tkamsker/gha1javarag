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

import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.cuco.core.dao.cusco.CusCoResponse;
import at.a1ta.cuco.core.shared.dto.Customer;
import at.a1ta.cuco.core.shared.dto.access.UnlockRequestContext;
import at.a1ta.cuco.core.shared.dto.access.UnlockStateEnum;

public interface CustomerUnlockService {

  boolean checkIfUnlockded(Customer customer, UserInfo user, String contextKey, String jobId);

  boolean checkIfUnlockedForSession(Customer customer, UserInfo user, String sessionId);

  CusCoResponse sendUnlockRequest(Customer customer, UserInfo user, UnlockRequestContext context, String contextKey);

  boolean updateUnlockRequestStateAndCheckIfUnlocked(Customer customer, UserInfo user, String contextKey, String referenceKey);

  void lockOverride(Customer customer, UserInfo user, String contextKey, UnlockStateEnum state);

}
