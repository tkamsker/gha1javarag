package at.a1ta.cuco.core.dao.esb;

import java.io.UnsupportedEncodingException;

import javax.xml.bind.DatatypeConverter;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Repository;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.esb.EsbException;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.dao.util.BrianCeeQueryOrderStub;
import at.mobilkom.brian.wsdl.BrianCeeQueryOrderRequest;
import at.mobilkom.brian.wsdl.BrianCeeQueryOrderRequestDocument;
import at.mobilkom.brian.wsdl.BrianCeeQueryOrderResponseDocument;
import at.mobilkom.brian.wsdl.CeeQOrderByUidRec;
import at.mobilkom.brian.wsdl.IspUidRec;
import at.mobilkom.eai.esb.EsbParam;

@Component
@Repository
class BrianCeeQueryOrderDaoImpl extends BaseEsbClient<BrianCeeQueryOrderStub> implements BrianCeeQueryOrderDao {

  private static final Logger logger = LoggerFactory.getLogger(BrianCeeQueryOrderDaoImpl.class);
  private static final String REALM_NAME = "ts.a1.net";
  private static final String DEAL_NAME = "ONETV";

  private SettingService settingService;

  @Override
  public BrianCeeQueryOrderResponseDocument getCeeQueryOrderResponse(String ispUid) {
    BrianCeeQueryOrderRequestDocument requestDocument = BrianCeeQueryOrderRequestDocument.Factory.newInstance();
    BrianCeeQueryOrderRequest request = BrianCeeQueryOrderRequest.Factory.newInstance();

    CeeQOrderByUidRec ceeQOrderByUidRec = CeeQOrderByUidRec.Factory.newInstance();
    IspUidRec ispUidRec = IspUidRec.Factory.newInstance();

    ceeQOrderByUidRec.setDealName(DEAL_NAME);
    ispUidRec.setId(ispUid);
    ispUidRec.setRealm(REALM_NAME);
    ceeQOrderByUidRec.setIspUid(ispUidRec);
    EsbParam param = new EsbParam();
    param.setSecurityCredentials(getESBSecurityCredentials());

    request.setCeeQueryOrder(ceeQOrderByUidRec);
    requestDocument.setBrianCeeQueryOrderRequest(request);
    try {
      return stub.brianCeeQueryOrder(requestDocument, param);
    } catch (Exception e) {
      String message = "BrianCeeQueryOrderRequest could not be processed.";
      throw new EsbException(message, e);
    }
  }

  private String getESBSecurityCredentials() {
    String esbSecurityUsername = settingService.getValue("asmp.username");
    String esbSecurityPassword = settingService.getValue("asmp.password");
    String esbSecurityCredentialString = esbSecurityUsername + ":" + esbSecurityPassword;
    try {
      byte[] message = esbSecurityCredentialString.getBytes("UTF-8");
      return DatatypeConverter.printBase64Binary(message);
    } catch (UnsupportedEncodingException e) {
      logger.error("Error while encoding esb security credentials", e);
    }
    return null;
  }

  @Autowired
  public void setSettingService(SettingService settingService) {
    this.settingService = settingService;
  }

}
