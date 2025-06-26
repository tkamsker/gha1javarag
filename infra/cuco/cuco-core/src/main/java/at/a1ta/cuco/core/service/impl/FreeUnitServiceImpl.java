package at.a1ta.cuco.core.service.impl;

import java.math.BigInteger;
import java.rmi.RemoteException;
import java.util.GregorianCalendar;

import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.cuco.core.service.FreeUnitService;
import at.telekom.eai.freeunits.xsd.FreeMinutesRequestDocument;
import at.telekom.eai.freeunits.xsd.FreeMinutesResponseDocument;
import at.telekom.www.voip.api20.RequestType;
import at.telekom.www.voip.api20.ResponseType;

import com.telekomaustriagroup.esb.freeunits.FreeUnitsStub;

@Service
public class FreeUnitServiceImpl extends BaseEsbClient<FreeUnitsStub> implements FreeUnitService {
  private static BigInteger REQUEST_ID = new BigInteger("11111111");
  private static String REQUESTING_SYSTEM = "CUCO";
  private static String TNVERHAELTNISID = "";

  @Override
  public ResponseType getFreeMinutes(String countryNr, String onkz, String telNr) throws RemoteException {
    FreeMinutesRequestDocument reqDoc = FreeMinutesRequestDocument.Factory.newInstance();
    RequestType request = reqDoc.addNewFreeMinutesRequest();

    request.setRequestID(REQUEST_ID);
    request.setRequestTS(new GregorianCalendar());
    request.setRequestingSystem(REQUESTING_SYSTEM);
    request.setTNVERHAELTNISID(TNVERHAELTNISID);
    request.setCOUNTRYNR(countryNr);
    request.setKZNR(onkz);
    request.setTNNR(telNr);

    FreeMinutesResponseDocument resp = stub.getFreeMinutes(reqDoc, null);
    return resp.getFreeMinutesResponse();
  }
}
