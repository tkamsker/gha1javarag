package at.a1ta.cuco.core.service;

import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.cuco.core.dao.cusco.CusCoResponse;
import at.a1ta.cuco.core.shared.dto.Customer;

public interface CuscoUnlockService {

  CusCoResponse prepareForSign(Customer customer, UserInfo userInfo, String contactPerson, String templateId);

  CusCoResponse checkStatusForSigned(String jobId);
}
