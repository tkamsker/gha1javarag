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

import java.net.MalformedURLException;
import java.rmi.RemoteException;
import java.util.ArrayList;

import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentConsignee;
import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentTree;

public interface CustomerEquipmentService {
  EquipmentTree getEquipmentTree(final String equipmentConsigneeId, final long partyId) throws RemoteException, MalformedURLException;

  ArrayList<EquipmentConsignee> getEquipmentConsignees(final ArrayList<Long> partyIds) throws MalformedURLException, RemoteException;

  ArrayList<EquipmentConsignee> getEquipmentConsignees(long partyId) throws MalformedURLException, RemoteException;
}
