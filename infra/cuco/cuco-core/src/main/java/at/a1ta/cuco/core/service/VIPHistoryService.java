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

import java.util.Date;
import java.util.List;

import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.VIPHistoryEntry;

public interface VIPHistoryService {

  List<VIPHistoryEntry> getVIPHistory(Long customerId);

  List<VIPHistoryEntry> getVIPHistory(Date from, Date to, String searchTerm, String vipStatus);

  void saveVIPStatusAndHistory(VIPHistoryEntry vipHistory, String lastChangeDate, Party cucoCustomer, String uUuser);

}
