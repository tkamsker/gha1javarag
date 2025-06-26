package at.a1ta.cuco.core.dao.esb;

import java.rmi.RemoteException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Repository;
import org.springframework.util.Assert;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.esb.EsbException;
import at.a1ta.cuco.core.bean.PWUTokenResponse;
import at.a1ta.cuco.core.shared.dto.AccessToken;
import at.a1ta.cuco.core.shared.dto.PartnerCenterAccessTokenRequest;
import at.infonova.a1ta.dach.orderdata.CreateTokenForOrderDataRequest;
import at.infonova.a1ta.dach.orderdata.CreateTokenForOrderDataRequestDocument;
import at.infonova.a1ta.dach.orderdata.CreateTokenForOrderDataResponseDocument;
import at.infonova.a1ta.dach.orderdata.DestinationSystemType.Enum;
import at.infonova.a1ta.dach.orderdata.GetOrderDataRequest;
import at.infonova.a1ta.dach.orderdata.GetOrderDataRequestDocument;
import at.infonova.a1ta.dach.orderdata.GetOrderDataResponse;
import at.infonova.a1ta.dach.orderdata.GetOrderDataResponseDocument;
import at.infonova.a1ta.dach.orderdata.Individual;
import at.infonova.a1ta.dach.orderdata.Organisation;
import at.infonova.a1ta.dach.orderdata.Party;
import at.infonova.a1ta.dach.orderdata.PartyType;
import at.infonova.a1ta.dach.orderdata.PhoneNumberType;
import at.infonova.a1ta.dach.orderdata.impl.PartyImpl;

import com.telekomaustriagroup.esb.landingpagedealer.LandingPageDealerStub;
import com.telekomaustriagroup.esb.landingpagedealer.OrderServiceFault;

@Repository
public class PartnerCenterLandingPageDaoImpl extends BaseEsbClient<LandingPageDealerStub> implements PartnerCenterLandingPageDao {

  private static final Logger logger = LoggerFactory.getLogger(PartnerCenterLandingPageDaoImpl.class);

  @Override
  public AccessToken getAccessToken(PartnerCenterAccessTokenRequest tokenRequest) {
    Assert.notNull(tokenRequest, "Request params must not be null");
    AccessToken token = AccessToken.NONE;

    try {
      token = createAccessTokenFromOrderDataResponseDocument(stub.createTokenForOrderData(createOrderDataRequestDocumentFrom(tokenRequest),
          null));
      if (token.isValid()) {
        token.setTargetSystem(tokenRequest.getTargetSystem());
      }
      logger.info("Received {} when sending {}.", new Object[] {token, tokenRequest});
    } catch (Exception e) {
      throw new EsbException("Error calling LandingPageDealer.createTokenForOrderData", e);
    }

    return token;
  }

  private CreateTokenForOrderDataRequestDocument createOrderDataRequestDocumentFrom(PartnerCenterAccessTokenRequest tokenRequest) {
    CreateTokenForOrderDataRequestDocument requestDocument = CreateTokenForOrderDataRequestDocument.Factory.newInstance();
    CreateTokenForOrderDataRequest request = requestDocument.addNewCreateTokenForOrderDataRequest();

    if (tokenRequest.containsParameter("ban")) {
      request.setBAN(tokenRequest.getParameter("ban"));
    }
    if (tokenRequest.containsParameter("cc") || tokenRequest.containsParameter("ndc") || tokenRequest.containsParameter("sn")) {
      PhoneNumberType msisdn = request.addNewMSISDN();
      msisdn.setCc(tokenRequest.getCountryCodeAsInt());
      msisdn.setNdc(tokenRequest.getNationalDestinationCodeAsInt());
      msisdn.setSn(tokenRequest.getSubscriberNumberAsInt());
    }
    if (tokenRequest.containsParameter("partyId")) {
      Party addNewParty = request.addNewParty();
      if ("Per".equalsIgnoreCase(tokenRequest.getParameter("partyType"))) {
        addNewParty.setPartyType(PartyType.INDIVIDUAL);
        addNewParty.addNewIndividual().setPartyId(tokenRequest.getParameter("partyId"));
      } else {
        addNewParty.setPartyType(PartyType.ORGANISATION);
        Organisation addNewOrganisation = addNewParty.addNewOrganisation();
        addNewOrganisation.setPartyId(tokenRequest.getParameter("partyId"));
        addNewOrganisation.setName(tokenRequest.getParameter("partyName"));
      }
    }
    if (tokenRequest.containsParameter("a1Login")) {
      request.setA1Login(tokenRequest.getParameter("a1Login"));
    }
    request.setProcessId(tokenRequest.getProcessId());
    request.setFrontEndSystem(tokenRequest.getSourceSystem());
    request.setDestinationSystem(Enum.forString(tokenRequest.getTargetSystem()));

    return requestDocument;
  }

  private AccessToken createAccessTokenFromOrderDataResponseDocument(CreateTokenForOrderDataResponseDocument document) {
    if (document == null || document.getCreateTokenForOrderDataResponse() == null) {
      return AccessToken.NONE;
    }
    AccessToken token = new AccessToken();
    token.setToken(document.getCreateTokenForOrderDataResponse().getToken());
    return token;
  }

  @Override
  public PWUTokenResponse validatePWUToken(String token) throws RemoteException, OrderServiceFault {
    long startMsec = System.currentTimeMillis();

    GetOrderDataRequest req = GetOrderDataRequest.Factory.newInstance();
    req.setFrontEndSystem("cuco"); // Zitat Mitter Andreas: Feld ist optional, wir haben keine Validierung drauf. Würde aber trotzdem
                                   // vorschlagen, ihr schickt entsprechenden Identifier, damit Betrieb die Requests zuordnen kann.
    req.setToken(token);

    GetOrderDataRequestDocument reqDoc = GetOrderDataRequestDocument.Factory.newInstance();
    reqDoc.setGetOrderDataRequest(req);

    startMsec = System.currentTimeMillis();

    GetOrderDataResponseDocument respDoc = stub.getOrderData(reqDoc, null);

    long durationMSec = System.currentTimeMillis() - startMsec;

    GetOrderDataResponse resp = respDoc.getGetOrderDataResponse();

    PWUTokenResponse pwuTokenResponse = new PWUTokenResponse();
    pwuTokenResponse.setA1Login(resp.getA1Login());
    pwuTokenResponse.setOrderId(resp.getOrderId());
    pwuTokenResponse.setRetailerId(resp.getRetailerId());
    pwuTokenResponse.setToken(resp.getToken());
    pwuTokenResponse.setFirstName(resp.getLoginFirstName());
    pwuTokenResponse.setLastName(resp.getLoginLastName());
    pwuTokenResponse.setPartyId(fetchPartyId(resp));
    // valid token
    pwuTokenResponse.setInvokationDuration(durationMSec);
    return pwuTokenResponse;
  }

  private String fetchPartyId(GetOrderDataResponse resp) {
    if (resp.getParty() instanceof PartyImpl) {
      Individual individual = ((PartyImpl) resp.getParty()).getIndividual();
      Organisation organisation = ((PartyImpl) resp.getParty()).getOrganisation();

      if (individual != null) {
        return individual.getPartyId();
      } else if (organisation != null) {
        return organisation.getPartyId();
      }
    }
    return null;
  }
}
