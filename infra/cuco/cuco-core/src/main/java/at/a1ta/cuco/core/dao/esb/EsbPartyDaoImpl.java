package at.a1ta.cuco.core.dao.esb;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.esb.EsbException;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.shared.dto.EsbParty;
import at.a1ta.cuco.core.shared.dto.ServiceClassInfo;
import at.a1ta.cuco.core.shared.dto.StandardAddress;
import at.a1ta.cuco.core.shared.dto.StandardAddress.AddressDataSource;
import at.a1telekom.eai.party.GetPartyRequest;
import at.a1telekom.eai.party.GetPartyRequest.GetBy;
import at.a1telekom.eai.party.GetPartyRequestDocument;
import at.a1telekom.eai.party.GetPartyResponse;
import at.a1telekom.eai.party.GetPartyResponseDocument;
import at.a1telekom.eai.party.Party;

import com.telekomaustriagroup.esb.party.PartyStub;

@Repository
public class EsbPartyDaoImpl extends BaseEsbClient<PartyStub> implements EsbPartyDao {

  private final static String DEFAULT_SOURCE_SYSTEM = "CUCO";
  private final static String DEFAULT_USER = "UCUCO01";

  private SettingService settings;

  @Override
  public EsbParty getESBParty(long partyId) {
    return createEsbParty(getParty(partyId));
  }

  @Override
  public Party getParty(long partyId) {
    GetPartyRequestDocument requestDoc = GetPartyRequestDocument.Factory.newInstance();
    GetPartyRequest request = requestDoc.addNewGetPartyRequest();
    GetBy getBy = request.addNewGetBy();
    getBy.setPartyId(partyId + "");

    request.setSourceSystem(getSourceSystem());
    request.setUser(getUser());
    Party party;
    try {
      GetPartyResponseDocument responseDoc = stub.getParty(requestDoc, null);
      GetPartyResponse response = responseDoc.getGetPartyResponse();
      party = response.getParty();
      if (!party.isSetServiceClass()) {
        party.setServiceClass(ServiceClassInfo.SERVICE_CLASS_NOT_RECEIVED);
        party.setServiceClassText("");
      }

    } catch (Exception e) {
      throw new EsbException(e);
    }
    return party;
  }

  private EsbParty createEsbParty(Party party) {
    if (party == null) {
      return null;
    }
    EsbParty esbParty = new EsbParty();
    esbParty.setPartyId(Long.valueOf(party.getPartyId()));
    esbParty.setShortName(party.getShortName());
    esbParty.setAddress(extractAddress(party));

    return esbParty;
  }

  private StandardAddress extractAddress(Party party) {
    StandardAddress address = new StandardAddress();
    address.setLkmsId(party.getStandardAddress().getLkmsId());
    address.setStreet(party.getStandardAddress().getStreet());
    address.setHouseNumber(party.getStandardAddress().getHouseNumber());
    address.setBlock(party.getStandardAddress().getBlock());
    address.setStaircase(party.getStandardAddress().getStaircase());
    address.setFloorNumber(party.getStandardAddress().getFloorNumber());
    address.setDoorNumber(party.getStandardAddress().getDoorNumber());
    address.setAdditional(party.getStandardAddress().getAdditional());
    address.setPostcode(party.getStandardAddress().getPostcode());
    address.setCity(party.getStandardAddress().getCity());
    address.setVillage(party.getStandardAddress().getVillage());
    address.setCountry(party.getStandardAddress().getCountry());
    address.setDataSource(AddressDataSource.PARTY_SERVICE);
    return address;
  }

  private String getSourceSystem() {
    return settings.getValueOrDefault("esbPartyDao.sourceSystem", DEFAULT_SOURCE_SYSTEM);
  }

  private String getUser() {
    return settings.getValueOrDefault("esbPartyDao.user", DEFAULT_USER);
  }

  @Autowired
  public void setSettings(SettingService settings) {
    this.settings = settings;
  }
}
