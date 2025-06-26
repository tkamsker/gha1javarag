package at.a1ta.cuco.core.service.customerequipment;

import java.net.MalformedURLException;
import java.rmi.RemoteException;
import java.util.ArrayList;
import java.util.List;

import net.sf.ehcache.Cache;
import net.sf.ehcache.CacheManager;
import net.sf.ehcache.Element;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.cuco.core.service.CustomerEquipmentService;
import at.a1ta.cuco.core.service.PartyService;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentConsignee;
import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentTree;
import at.telekom.eai.businesscustomerequipment.xsd.EquipmentRequest;
import at.telekom.eai.businesscustomerequipment.xsd.EquipmentResponse;
import at.telekom.eai.businesscustomerequipment.xsd.GetEquipmentRequestDocument;
import at.telekom.eai.businesscustomerequipment.xsd.GetEquipmentResponseDocument;
import at.telekom.eai.businesscustomerequipment.xsd.GetPartnersRequestDocument;
import at.telekom.eai.businesscustomerequipment.xsd.GetPartnersResponseDocument;
import at.telekom.eai.businesscustomerequipment.xsd.PartnerItem;
import at.telekom.eai.businesscustomerequipment.xsd.PartnerRequest;
import at.telekom.eai.businesscustomerequipment.xsd.PartnerResponse;

import com.telekomaustriagroup.esb.businesscustomerequipment.BusinessCustomerEquipmentStub;

@Service
public class CustomerEquipmentServiceImpl extends BaseEsbClient<BusinessCustomerEquipmentStub> implements CustomerEquipmentService {
  private static Logger logger = LoggerFactory.getLogger(CustomerEquipmentServiceImpl.class);

  private static String EHCACHE_KEY = "customerEquipmentCache";

  @Autowired
  private PartyService partyService;
  @Autowired
  private CustomerEquipmentHelper helper;
  @Autowired
  private CustomerEquipmentTranslator translator;

  @Override
  public EquipmentTree getEquipmentTree(String equipmentConsigneeId, long partyId) throws RemoteException, MalformedURLException {
    Cache cache = CacheManager.getInstance().getCache(EHCACHE_KEY);
    Element cacheElement = cache.get(equipmentConsigneeId);

    if (cacheElement == null) {
      EquipmentTree data = getEquipmentTreeFromSAP(equipmentConsigneeId, partyId);

      logger.debug("Caching Business Customer Equipment data for consigneeId '" + equipmentConsigneeId + "' and partyId '" + partyId + "'.");
      cacheElement = new Element(equipmentConsigneeId, data);
      cache.put(cacheElement);

      return data;
    }

    logger.debug("Returning cached Business Customer Equipment data for consigneeId '" + equipmentConsigneeId + "' and partyId '" + partyId + "'.");
    return (EquipmentTree) cacheElement.getObjectValue();
  }

  private EquipmentTree getEquipmentTreeFromSAP(String equipmentConsigneeId, long partyId) throws RemoteException, MalformedURLException {
    Party party = partyService.get(partyId);
    EquipmentConsignee equipmentConsignee = getEquipmentConsignee(partyId, equipmentConsigneeId);
    EquipmentResponse response = requestEquipments(equipmentConsigneeId);

    return helper.buildEquipmentTree(response, party, equipmentConsignee);
  }

  @Override
  public ArrayList<EquipmentConsignee> getEquipmentConsignees(ArrayList<Long> partyIds) throws MalformedURLException, RemoteException {
    ArrayList<EquipmentConsignee> allConsignees = new ArrayList<EquipmentConsignee>();
    for (long partyId : partyIds) {
      allConsignees.addAll(getEquipmentConsignees(partyId));
    }
    return allConsignees;
  }

  @SuppressWarnings("unchecked")
  @Override
  public ArrayList<EquipmentConsignee> getEquipmentConsignees(long partyId) throws MalformedURLException, RemoteException {

    Cache cache = CacheManager.getInstance().getCache(EHCACHE_KEY);
    Element cacheElement = cache.get(partyId);

    if (cacheElement == null) {
      ArrayList<EquipmentConsignee> data = getEquipmentConsigneesFromSAP(partyId);

      logger.debug("Caching Business Customer Equipment Consignees for partyId '" + partyId + "'.");
      cacheElement = new Element(partyId, data);
      cache.put(cacheElement);

      return data;
    }

    logger.debug("Returning cached Business Customer Equipment Consignees for partyId '" + partyId + "'.");
    return (ArrayList<EquipmentConsignee>) cacheElement.getObjectValue();
  }

  private ArrayList<EquipmentConsignee> getEquipmentConsigneesFromSAP(long partyId) throws MalformedURLException, RemoteException {
    PartnerRequest request = PartnerRequest.Factory.newInstance();
    request.setAuftraggeber(partyId + "");

    GetPartnersRequestDocument requestDocument = GetPartnersRequestDocument.Factory.newInstance();
    requestDocument.setGetPartnersRequest(request);

    GetPartnersResponseDocument responseDocument = stub.getPartners(requestDocument, null);

    PartnerResponse response = responseDocument.getGetPartnersResponse();

    PartnerItem[] partnerItems = response.getPartnerItemArray();
    return translator.convertToEquipmentConsigneeBeans(partyId, partnerItems);
  }

  private EquipmentConsignee getEquipmentConsignee(long partyId, String equipmentConsigneeId) throws RemoteException, MalformedURLException {
    List<EquipmentConsignee> consignees = getEquipmentConsignees(partyId);

    for (EquipmentConsignee consignee : consignees) {
      if (equipmentConsigneeId.equals(consignee.getId())) {
        return consignee;
      }
    }

    throw new RuntimeException("Could not find Business Customer Equipment consignee with ID '" + equipmentConsigneeId + "'");
  }

  private EquipmentResponse requestEquipments(String equipmentConsigneeId) throws RemoteException, MalformedURLException {
    EquipmentRequest request = EquipmentRequest.Factory.newInstance();
    request.setWarenempfanger(equipmentConsigneeId);

    GetEquipmentRequestDocument requestDocument = GetEquipmentRequestDocument.Factory.newInstance();
    requestDocument.setGetEquipmentRequest(request);

    GetEquipmentResponseDocument responseDocument = stub.getEquipment(requestDocument, null);

    return responseDocument.getGetEquipmentResponse();
  }
}
