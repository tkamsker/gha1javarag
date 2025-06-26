package at.a1ta.cuco.core.dao.esb;

import java.rmi.RemoteException;

import org.springframework.stereotype.Repository;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.esb.EsbException;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;
import at.a1ta.cuco.core.shared.dto.mobilpoints.MobilPoints;
import at.mobilkom.eai.mobilpointsservice.GetMPTRequestDocument;
import at.mobilkom.eai.mobilpointsservice.GetMPTRequestType;
import at.mobilkom.eai.mobilpointsservice.GetMPTResponseDocument;
import at.mobilkom.eai.mobilpointsservice.GetMPTResponseType;
import at.mobilkom.eai.mobilpointsservice.MsisdnRec;

import com.telekomaustriagroup.esb.mptsvc.ErrorMessage;
import com.telekomaustriagroup.esb.mptsvc.MptSvcStub;

@Repository
public class MobilPointsDaoImpl extends BaseEsbClient<MptSvcStub> implements MobilPointsDao {

  private static String MOBIL_POINTS_SOURCE_SYSTEM = "CUCO";
  private static boolean MOBIL_POINTS_LOAD_DETAILS = false;

  @Override
  public MobilPoints getMobilPoints(PhoneNumberStructure phoneNumber) {

    GetMPTRequestDocument requestDocument = createMobilPointsRequestDocument(phoneNumber);

    GetMPTResponseDocument responseDocument;
    try {
      responseDocument = stub.GetMPT(requestDocument, null);
    } catch (RemoteException e) {
      throw new EsbException(e);
    } catch (ErrorMessage e) {
      throw new EsbException(e);
    }
    GetMPTResponseType response = responseDocument.getGetMPTResponse();

    return createMobilPointsFromResponse(response);
  }

  private MobilPoints createMobilPointsFromResponse(GetMPTResponseType response) {
    MobilPoints mobilPoins = new MobilPoints();
    mobilPoins.setAmdocsPoints(response.getMPAmdocs());
    mobilPoins.setClarifyPoints(response.getMPCLFY());
    mobilPoins.setPartnerWebPoints(response.getMPPWSLA());
    return mobilPoins;
  }

  private GetMPTRequestDocument createMobilPointsRequestDocument(PhoneNumberStructure phoneNumber) {
    GetMPTRequestType request = GetMPTRequestType.Factory.newInstance();

    MsisdnRec msisdn = request.addNewMSISDN();
    msisdn.setCc(phoneNumber.getCountryCode());
    msisdn.setNdc(phoneNumber.getOnkz());
    msisdn.setSn(phoneNumber.getNumber());

    request.setSourceSystem(MOBIL_POINTS_SOURCE_SYSTEM);
    request.setLoadDetails(MOBIL_POINTS_LOAD_DETAILS);

    GetMPTRequestDocument requestDocument = GetMPTRequestDocument.Factory.newInstance();
    requestDocument.setGetMPTRequest(request);

    return requestDocument;
  }
}
