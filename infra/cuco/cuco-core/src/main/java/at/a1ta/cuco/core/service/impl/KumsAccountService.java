package at.a1ta.cuco.core.service.impl;

import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.telekom.www.eai.wstokumsretrieveaccount.GetAccountDocument;
import at.telekom.www.eai.wstokumsretrieveaccount.GetAccountResponseDocument;
import at.telekom.www.eai.wstokumsretrieveaccount.WSKUMSRetrieveAccountResponseACC1ACCOUNTType;

import com.telekomaustriagroup.esb.kumsaccount.KUMSAccountStub;

@Service
public class KumsAccountService extends BaseEsbClient<KUMSAccountStub> {

  public WSKUMSRetrieveAccountResponseACC1ACCOUNTType getAccount(String clearingAccount) throws Exception {
    GetAccountDocument doc = GetAccountDocument.Factory.newInstance();
    doc.addNewGetAccount().setACCTID(clearingAccount);

    GetAccountResponseDocument value = stub.getAccount(doc, null);

    return value.getGetAccountResponse().getACC1ACCOUNT();
  }
}
