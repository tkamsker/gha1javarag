package at.a1ta.cuco.core.service;

import java.util.ArrayList;
import java.util.HashMap;

import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.cuco.core.shared.dto.BillingAccountNumber;
import at.a1ta.cuco.core.shared.dto.CrmAuthenticationInfo;
import at.a1ta.cuco.core.shared.dto.Party;

public interface CrmAuthenticationService {
  HashMap<String, CrmAuthenticationInfo> getCustomerPasswords(final ArrayList<BillingAccountNumber> ban, Party party, UserInfo userInfo);
}
