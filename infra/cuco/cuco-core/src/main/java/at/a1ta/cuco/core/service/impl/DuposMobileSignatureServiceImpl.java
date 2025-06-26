package at.a1ta.cuco.core.service.impl;

import java.rmi.RemoteException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.telekomaustriagroup.esb.duposmobilesignature.DuposMobileSignatureStub;
import com.telekomaustriagroup.esb.duposmobilesignature.Fault;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.cuco.core.service.DuposMobileSignatureService;
import at.telekom.eai.schemas.eai.duposmobilesignature.FilesType;
import at.telekom.eai.schemas.eai.duposmobilesignature.SendContractToSign;
import at.telekom.eai.schemas.eai.duposmobilesignature.SendContractToSignDocument;
import at.telekom.eai.schemas.eai.duposmobilesignature.SendContractToSignResponseDocument;
import at.telekom.eai.schemas.eai.duposmobilesignature.SignMethodType;

@Service
public class DuposMobileSignatureServiceImpl extends BaseEsbClient<DuposMobileSignatureStub> implements DuposMobileSignatureService {

  private static final Logger LOGGER = LoggerFactory.getLogger(DuposMobileSignatureServiceImpl.class);

  @Override
  public String sendContractToSign(String jobId, byte[] data) {
    SendContractToSignDocument request = getRequestForContractSign(jobId, data);

    SendContractToSignResponseDocument response = null;
    try {
      response = stub.sendContractToSign(request, null);
    } catch (RemoteException | Fault e) {
      LOGGER.error("Error while sending contract to sign", e);
    }
    if (response == null || response.getSendContractToSignResponse() == null) {
      LOGGER.error("Error while sending contract to sign, response is null");
      return null;
    }
    if (response.getSendContractToSignResponse().getDataItemsArray() == null || response.getSendContractToSignResponse().getDataItemsArray().length == 0) {
      LOGGER.error("Error while sending contract to sign, data items are null or empty");
      return null;
    }
    return response.getSendContractToSignResponse().getDataItemsArray(0).getSigningUrlQRCode();
  }

  private SendContractToSignDocument getRequestForContractSign(String jobId, byte[] data) {
    SendContractToSignDocument request = SendContractToSignDocument.Factory.newInstance();
    SendContractToSign doc = request.addNewSendContractToSign();
    doc.setSignMethod(SignMethodType.MOBILE);
    FilesType fileType = doc.addNewFiles();
    fileType.setFileName(jobId);
    fileType.setFileData(data);
    fileType.setFileSize(data.length);
    return request;
  }

}
