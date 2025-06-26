package at.a1ta.cuco.core.service.impl;

import java.util.Calendar;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TimeZone;

import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import org.springframework.util.Assert;

import a1.gdpr.webservice.Brand;
import a1.gdpr.webservice.UserType;
import at.a1ta.bite.audit.core.Auditor;
import at.a1ta.bite.core.server.dto.PartySearchEvent;
import at.a1ta.bite.core.server.dto.Trackable;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.server.service.UserTrackingService;
import at.a1ta.bite.data.solr.core.query.Field;
import at.a1ta.bite.data.solr.core.query.result.FacetResult;
import at.a1ta.cuco.core.audit.ContextAwareAuditHelper;
import at.a1ta.cuco.core.audit.CuCoAuditActivity;
import at.a1ta.cuco.core.audit.CuCoAuditScope;
import at.a1ta.cuco.core.dao.db.PartyDao;
import at.a1ta.cuco.core.service.EsbPartyService;
import at.a1ta.cuco.core.service.PartyCustomerLoyaltyService;
import at.a1ta.cuco.core.service.PartyDeclarationOfConsentService;
import at.a1ta.cuco.core.service.PartyProfileService;
import at.a1ta.cuco.core.service.PartySearchValueFormatHelper;
import at.a1ta.cuco.core.service.PartyService;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PartyAdditionalInfo;
import at.a1ta.cuco.core.shared.dto.PartySearch;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;
import at.a1ta.cuco.core.shared.dto.PointOfSaleInfo;
import at.a1ta.cuco.core.shared.dto.ServiceClassInfo;
import at.a1ta.cuco.core.shared.dto.SimplePage;
import at.a1ta.cuco.core.shared.dto.StandardAddress;
import at.a1ta.cuco.core.shared.dto.StandardAddress.AddressDataSource;
import at.a1ta.cuco.core.shared.validator.AONNumberValidator;
import at.a1ta.cuco.core.shared.validator.BANValidator;
import at.a1ta.cuco.core.shared.validator.CityValidator;
import at.a1ta.cuco.core.shared.validator.CommonValidator;
import at.a1ta.cuco.core.shared.validator.FirstnameValidator;
import at.a1ta.cuco.core.shared.validator.HousenumberValidator;
import at.a1ta.cuco.core.shared.validator.LastnameValidator;
import at.a1ta.cuco.core.shared.validator.PartyIdValidator;
import at.a1ta.cuco.core.shared.validator.PhonenumberValidator;
import at.a1ta.cuco.core.shared.validator.StreetValidator;
import at.a1ta.cuco.core.shared.validator.ZipCodeValidator;
import at.a1telekom.eai.party.Address;

@Service
public class PartyServiceImpl implements PartyService {

  private final PartyIdValidator partyIdValidator = new PartyIdValidator();
  private final BANValidator banValidator = new BANValidator();
  private final AONNumberValidator aonNumberValidator = new AONNumberValidator();
  private final LastnameValidator lastnameValidator = new LastnameValidator();
  private final FirstnameValidator firstnameValidator = new FirstnameValidator();
  private final PhonenumberValidator phonenumberValidator = new PhonenumberValidator();
  private final ZipCodeValidator zipCodeValidator = new ZipCodeValidator();
  private final CityValidator cityValidator = new CityValidator();

  private final HousenumberValidator housenumberValidator = new HousenumberValidator();
  private final StreetValidator streetValidator = new StreetValidator();

  static final int DEFAULT_MAX_ELEM = 2000;
  static final String PARTYSEARCH_SOLR_ENABLED = "Partysearch.solrEnabled";
  static final String FACETED_PARTYSEARCH_ENABLED = "Partysearch.solrFacetedSearchEnabled";

  private static final Logger LOGGER = LoggerFactory.getLogger(PartyServiceImpl.class);

  private static final String SETTING_SUBSIDISED_TARIFS = "subsidised_tarifs";
  private static final String SETTING_SUBSIDISED_TARIFS_SEPERATOR = ";";

  private PartyDao customerDao;
  private PartyDao partySolrRepository;
  private PartyDao partySolrRepositoryWithPhoneNumbers;
  private PartySearchValueFormatHelper partySearchFormatHelper;

  private SettingService settingService;
  private UserTrackingService userTrackingService;
  @Autowired
  private EsbPartyService esbPartyService;
  @Autowired
  private PartyDeclarationOfConsentService partyDeclarationOfConsentService;
  @Autowired
  private PartyProfileService partyProfileService;
  @Autowired
  private PartyCustomerLoyaltyService partyCustomerLoyaltyService;

  @Override
  public Party get(final long id) {
    Party party = customerDao.loadParty(id);
    // adjust offset
    if (party != null && party.getBirthdate() != null) {
      try {
        party.setDateOfBirth(party.getBirthdate().getTime() + getOffsetDiff());
      } catch (Exception ex) {
        LOGGER.warn("Could not adjust DST for DOB for party : " + party.getId() + " - DOB: " + party.getDateOfBirth());
      }
    }
    return party;
  }

  public static int getOffsetDiff() {
    final Calendar cal = Calendar.getInstance(TimeZone.getDefault());
    return (cal.get(Calendar.ZONE_OFFSET) + cal.get(Calendar.DST_OFFSET));
  }

  @Override
  public SimplePage<Party> search(PartySearch partySearch) {
    Assert.notNull(partySearch);
    // if user tries to search for lead, copy id to lead id
    if (!CommonValidator.isBlank(partySearch.getId()) && partySearch.getId().trim().toUpperCase().startsWith("L")) {
      partySearch.setLeadId(partySearch.getId());
      partySearch.setId(partySearch.getId().toLowerCase().replace('l', ' ').trim());
    }

    Auditor.audit(ContextAwareAuditHelper.createFor(CuCoAuditScope.CUSTOMER, CuCoAuditActivity.SEARCH).withMessage(partySearch.toString()));

    PartySearch formattedSearch = formatSearchValues(partySearch);

    boolean indexedSearchEnabled = isIndexedSearchEnabled();
    final int maxResults = settingService.getIntValue("Partysearch.maxResults", DEFAULT_MAX_ELEM);

    SimplePage<Party> searchResult = new SimplePage<Party>();
    if (indexedSearchEnabled) {
      if (partySearch.isFulltext()) {
        failsafeTrackUserSearch(new PartySearchEvent(partySearch.getSearchExecutingUserName(), PartySearchEvent.EventType.SEARCH_FT));
      } else if (StringUtils.isNotBlank(partySearch.getAonAccountNumber())) {
        failsafeTrackUserSearch(new PartySearchEvent(partySearch.getSearchExecutingUserName(), PartySearchEvent.EventType.SEARCH_PRI));
      } else {
        failsafeTrackUserSearch(new PartySearchEvent(partySearch.getSearchExecutingUserName(), PartySearchEvent.EventType.SEARCH_SOL));
      }
      searchResult = indexedSearch(formattedSearch, maxResults);
    }
    if ((!indexedSearchEnabled || searchResult == null || searchResult.getContent().isEmpty()) && !partySearch.isFulltext()) {
      if ((isUniqueFieldGiven(partySearch) && areUniqueFieldsValid(partySearch)) || areNoneUniqueSearchCriteriaValid(partySearch)) {
        failsafeTrackUserSearch(new PartySearchEvent(partySearch.getSearchExecutingUserName(), PartySearchEvent.EventType.SEARCH_FB));

        searchResult = this.customerDao.search(formattedSearch, maxResults);
      } else {
        searchResult = new SimplePage<Party>();
        searchResult.setInputValid(false);
      }
    }

    return searchResult;
  }

  @Override
  public SimplePage<Party> searchNonCustomers(PartySearch partySearch) {
    Assert.notNull(partySearch);

    Auditor.audit(ContextAwareAuditHelper.createFor(CuCoAuditScope.CUSTOMER, CuCoAuditActivity.SEARCH_LEAD).withMessage(partySearch.toString()));

    PartySearch formattedSearch = formatSearchValues(partySearch);
    final int maxResults = settingService.getIntValue("Partysearch.maxResults", DEFAULT_MAX_ELEM);
    SimplePage<Party> searchResult = this.customerDao.searchNonCustomer(formattedSearch, maxResults);
    return searchResult;
  }

  @Override
  public List<FacetResult> facetedSearch(PartySearch partySearch, Field facetedField) {
    Assert.notNull(partySearch);
    Assert.notNull(facetedField);
    // if user tries to search for lead, copy id to lead id
    if (!CommonValidator.isBlank(partySearch.getId()) && partySearch.getId().trim().toUpperCase().startsWith("L")) {
      partySearch.setLeadId(partySearch.getId());
      partySearch.setId(partySearch.getId().toLowerCase().replace('l', ' ').trim());
    }
    boolean indexedSearchEnabled = solrFacetedSearchEnabled();

    List<FacetResult> searchResult = Collections.<FacetResult> emptyList();
    if (indexedSearchEnabled) {
      try {
        searchResult = chooseRepositoryForSearch(partySearch).facetedSearch(partySearch, facetedField);
      } catch (Exception e) {
        LOGGER.warn("Could not execute SOLR Query", e);
      }
      return searchResult;
    }
    return searchResult;
  }

  private PartySearch formatSearchValues(PartySearch partySearch) {
    PhoneNumberStructure phoneStructure = partySearchFormatHelper.parsePhoneNumber(partySearch.getPhoneNumber());
    if (phoneStructure != null) {
      partySearch.setLkz(phoneStructure.getCountryCode());
      partySearch.setOkz(phoneStructure.getOnkz());
      partySearch.setCallNumber(phoneStructure.getNumber());
    }
    partySearch.setCommercialRegisterNumber(partySearchFormatHelper.formatCommectialRegisterNumber(partySearch.getCommercialRegisterNumber()));
    return partySearch;
  }

  private SimplePage<Party> indexedSearch(PartySearch customerSearch, int maxResults) {
    SimplePage<Party> result = new SimplePage<Party>();
    // if user tries to search for lead, copy id to lead id
    if (!CommonValidator.isBlank(customerSearch.getId()) && customerSearch.getId().trim().toUpperCase().startsWith("L")) {
      customerSearch.setLeadId(customerSearch.getId());
      customerSearch.setId(customerSearch.getId().toLowerCase().replace('l', ' ').trim());
    }
    try {
      result = chooseRepositoryForSearch(customerSearch).search(customerSearch, maxResults);
    } catch (Exception e) {
      LOGGER.warn("Could not execute SOLR Query", e);
    }
    return result;
  }

  private PartyDao chooseRepositoryForSearch(PartySearch customerSearch) {

    if (customerSearch.isFulltext()) {
      return this.partySolrRepositoryWithPhoneNumbers;
    }
    if (StringUtils.isNotBlank(customerSearch.getAonAccountNumber())) {
      return this.customerDao;
    } else if (isSearchForPhoneNumberOrBAN(customerSearch)) {
      return this.partySolrRepositoryWithPhoneNumbers;
    }
    return this.partySolrRepository;
  }

  private boolean isSearchForPhoneNumberOrBAN(PartySearch customerSearch) {
    return (StringUtils.isNotBlank(customerSearch.getBillingAccountNumber()) || StringUtils.isNotBlank(customerSearch.getOkz()) || StringUtils.isNotBlank(customerSearch.getPhoneNumber()));
  }

  @Override
  public List<Party> getCustomers4Header(final Number headerId) {
    return this.getCustomers4Header(headerId.longValue(), -1, -1);
  }

  @Override
  public List<Party> getCustomers4Header(final Number headerId, final int skip, final int maxResults) {
    if (headerId == null) {
      throw new org.apache.commons.lang.NullArgumentException("headerId");
    }
    return this.customerDao.getCustomers4Header(headerId.longValue(), skip, maxResults);
  }

  @Override
  public Party getHierarchyForParty(long partyId) {
    List<Party> parties = customerDao.getHierarchyForParty(partyId);

    Map<Long, Party> id2party = new HashMap<Long, Party>(parties.size());
    for (Party party : parties) {
      id2party.put(party.getId(), party);
    }

    Party rootParty = null;
    for (Party party : parties) {
      long parentId = party.getHeaderId();

      if (party.getId() == parentId) {
        rootParty = party;
      } else {
        Party parent = id2party.get(parentId);
        parent.addChild(party);
      }
    }

    return rootParty;
  }

  @Override
  public int countCustomers4Header(Long headerId) {
    if (headerId == null) {
      throw new org.apache.commons.lang.NullArgumentException("headerId");
    }
    return customerDao.countCustomers4Header(headerId);
  }

  @Override
  public boolean isSubsidised(final long customerId) {
    final String value = settingService.getValue(SETTING_SUBSIDISED_TARIFS);
    return this.customerDao.isSubsidised(customerId, value.split(SETTING_SUBSIDISED_TARIFS_SEPERATOR));
  }

  @Override
  public List<String> getAllSegments() {
    return customerDao.getAllSegments();
  }

  @Override
  public boolean isIndexedSearchEnabled() {
    boolean searchUsingSolr = true;
    try {
      searchUsingSolr = settingService.getBooleanValue(PARTYSEARCH_SOLR_ENABLED, true);
    } catch (Exception e) {
      LOGGER.debug(PARTYSEARCH_SOLR_ENABLED + " not found using default value (" + searchUsingSolr + ")");
    }
    return searchUsingSolr;
  }

  private boolean solrFacetedSearchEnabled() {
    boolean searchUsingSolr = false;
    try {
      searchUsingSolr = settingService.getBooleanValue(FACETED_PARTYSEARCH_ENABLED, true);
    } catch (Exception e) {
      LOGGER.debug(FACETED_PARTYSEARCH_ENABLED + " not found using default value (" + searchUsingSolr + ")");
    }
    return searchUsingSolr;
  }

  private boolean isLastNameCompanyNameValid(PartySearch partySearch) {
    return StringUtils.isEmpty(partySearch.getLastName()) || lastnameValidator.isValid(partySearch.getLastName());
  }

  private boolean isFirstNameValid() {
    return firstnameValidator.isValid();
  }

  private boolean isAONNumberValid(PartySearch partySearch) {
    return StringUtils.isEmpty(partySearch.getAonAccountNumber()) || aonNumberValidator.isValid(partySearch.getAonAccountNumber());
  }

  private boolean isStreetValid(PartySearch partySearch) {
    return StringUtils.isEmpty(partySearch.getStreet()) || streetValidator.isValid(partySearch.getStreet());
  }

  private boolean isZIPCodeValid(PartySearch partySearch) {
    return StringUtils.isEmpty(partySearch.getPostcode()) || zipCodeValidator.isValid(partySearch.getPostcode());
  }

  private boolean isHouseNumberValid() {
    return housenumberValidator.isValid();
  }

  private boolean isCityValid(PartySearch partySearch) {
    return StringUtils.isEmpty(partySearch.getCity()) || cityValidator.isValid(partySearch.getCity());
  }

  private boolean isPartyIdValid(PartySearch partySearch) {
    return StringUtils.isEmpty(partySearch.getId()) || partyIdValidator.isValid(partySearch.getId());
  }

  private boolean isPhoneNumberValid() {
    return phonenumberValidator.isValid();
  }

  private boolean isBANValid(PartySearch partySearch) {
    return StringUtils.isEmpty(partySearch.getBillingAccountNumber()) || banValidator.isValid(partySearch.getBillingAccountNumber());
  }

  private boolean areFirstNameDependenciesValid(PartySearch partySearch) {
    return !(StringUtils.isNotEmpty(partySearch.getFirstName()) && StringUtils.isEmpty(partySearch.getLastName()));
  }

  private boolean areStreetDependenciesValid(PartySearch partySearch) {
    return StringUtils.isEmpty(partySearch.getStreet()) || (StringUtils.isNotEmpty(partySearch.getPostcode()) && StringUtils.isNotEmpty(partySearch.getCity()));
  }

  private boolean areHouseNumberDependenciesValid(PartySearch partySearch) {
    return StringUtils.isEmpty(partySearch.getHouseNumber()) || StringUtils.isNotEmpty(partySearch.getStreet());
  }

  private boolean areNoneUniqueSearchCriteriaValid(PartySearch partySearch) {
    if (!validateNoneUniqueSearchCriteria(partySearch)) {
      return false;
    }
    return validateDependencies(partySearch);
  }

  private boolean validateNoneUniqueSearchCriteria(PartySearch partySearch) {
    if (!isLastNameCompanyNameValid(partySearch)) {
      return false;
    }
    if (!isFirstNameValid()) {
      return false;
    }
    if (!isStreetValid(partySearch)) {
      return false;
    }
    if (!isZIPCodeValid(partySearch)) {
      return false;
    }
    if (!isHouseNumberValid()) {
      return false;
    }
    if (!isCityValid(partySearch)) {
      return false;
    }
    return true;
  }

  private boolean validateDependencies(PartySearch partySearch) {
    if (!areFirstNameDependenciesValid(partySearch)) {
      return false;
    }
    if (!areStreetDependenciesValid(partySearch)) {
      return false;
    }
    if (!areHouseNumberDependenciesValid(partySearch)) {
      return false;
    }
    return true;
  }

  private boolean isUniqueFieldGiven(PartySearch partySearch) {
    return !StringUtils.isEmpty(partySearch.getId()) || !StringUtils.isEmpty(partySearch.getPhoneNumber()) || !StringUtils.isEmpty(partySearch.getBillingAccountNumber())
        || !StringUtils.isEmpty(partySearch.getAonAccountNumber()) || !StringUtils.isEmpty(partySearch.getCommercialRegisterNumber());
  }

  private boolean areUniqueFieldsValid(PartySearch partySearch) {
    return isPartyIdValid(partySearch) && isPhoneNumberValid() && isBANValid(partySearch) && isAONNumberValid(partySearch);
  }

  private void failsafeTrackUserSearch(Trackable trackable) {
    try {
      userTrackingService.trackUserEvent(trackable);
    } catch (Exception e) {
      LOGGER.warn("Could not track user event.", e);
    }
  }

  @Autowired
  public void setCustomerDao(@Qualifier("cucoCustomerDao") PartyDao customerDao) {
    this.customerDao = customerDao;
  }

  @Autowired(required = false)
  public void setPartySolrRepository(@Qualifier("partySolrRepository") PartyDao partySolrRepository) {
    this.partySolrRepository = partySolrRepository;
  }

  @Autowired(required = false)
  public void setPartySolrRepositoryWithPhoneNumbers(@Qualifier("partySolrRepositoryWithPhoneNumbers") PartyDao partySolrRepositoryWithPhoneNumbers) {
    this.partySolrRepositoryWithPhoneNumbers = partySolrRepositoryWithPhoneNumbers;
  }

  @Autowired
  public void setPartySearchFormatterHelper(PartySearchValueFormatHelper partySearchFormatterHelper) {
    this.partySearchFormatHelper = partySearchFormatterHelper;
  }

  @Autowired
  public void setSettingService(SettingService settingService) {
    this.settingService = settingService;
  }

  @Autowired
  public void setUserTrackingService(UserTrackingService userTrackingService) {
    this.userTrackingService = userTrackingService;
  }

  @Override
  public void saveNonCustomer(Party party) {
    this.customerDao.insertNonCustomerContact(party);
  }

  @Override
  public void mergeNonCustomerAndTransferOffers(Party party) {
    this.customerDao.mergeNonCustomerAndTransferOffers(party);
    this.customerDao.markNonCustomerMerged(party);
  }

  @Override
  public PartyAdditionalInfo getPartyAdditionalInfo(long partyId, String userName) {
    PartyAdditionalInfo info = new PartyAdditionalInfo();
    // defaulting to Error.
    PointOfSaleInfo pointOfSaleInfo = new PointOfSaleInfo(PointOfSaleInfo.LOADING, null, null);
    ServiceClassInfo serviceClassInfo = new ServiceClassInfo(ServiceClassInfo.SERVICE_CLASS_LOADING, null);
    try {
      at.a1telekom.eai.party.Party partyExternObj = esbPartyService.getParty(partyId);
      if (partyExternObj != null) {
        pointOfSaleInfo.setStaus(PointOfSaleInfo.NOT_RECEIVED);
        serviceClassInfo.setServiceClass(partyExternObj.getServiceClass());
        serviceClassInfo.setServiceClassText(partyExternObj.getServiceClassText());
        if (partyExternObj.isSetPointOfSale() && settingService.getBooleanValue("pos.showPOSInfo", true)) {
          pointOfSaleInfo.setDealerId(partyExternObj.getPointOfSale().getDealerNumber());
          pointOfSaleInfo.setDealerName(partyExternObj.getPointOfSale().getName());
          pointOfSaleInfo.setDelearEmailId(partyExternObj.getPointOfSale().getEmailAddress());
          pointOfSaleInfo.setAddress(extractAddress(partyExternObj.getPointOfSale().getAddress()));
          pointOfSaleInfo.setStaus(PointOfSaleInfo.LOADED);
        } else if (settingService.getBooleanValue("testModeActive", false)) {
          if ((partyId == 100134728 || partyId == 106892050 || partyId == 105474529) && settingService.getBooleanValue("pos.showPOSInfo", true)) {
            pointOfSaleInfo.setStaus(PointOfSaleInfo.LOADED);
            pointOfSaleInfo.setDealerId("Mocked:");
            pointOfSaleInfo.setDealerName("Mocked:" + partyExternObj.getShortName());
            pointOfSaleInfo.setAddress(mockStandardAddress());
          }
          if ((partyId == 107067684) && settingService.getBooleanValue("pos.showPOSInfo", true)) {
            Thread.sleep(30000);
          }
          if ((partyId == 106318953) && settingService.getBooleanValue("pos.showPOSInfo", true)) {
            throw new RuntimeException();
          }

        }
      } else {
        pointOfSaleInfo.setStaus(PointOfSaleInfo.NOT_RECEIVED);
        serviceClassInfo.setServiceClass(ServiceClassInfo.SERVICE_CLASS_NOT_RECEIVED);
      }
    } catch (Exception ex) {
      pointOfSaleInfo.setStaus(PointOfSaleInfo.ERROR);
      serviceClassInfo.setServiceClass(ServiceClassInfo.SERVICE_CLASS_ERROR);
      LOGGER.error("Error while loading additional info from ESB Party Service", ex);
    }
    info.setServiceClassInfo(serviceClassInfo);
    // switched to PartyProfile
    // info.setPointOfSaleInfo(pointOfSaleInfo);
    if (settingService.getBooleanValue("gdprJune2017.showDeclarationOfConsent")) {
      info.setPartyDeclarationOfConsentInfo(partyDeclarationOfConsentService.getCurrentDeclarationOfConsentForParty(String.valueOf(partyId), userName, Brand.A_1_RBM, UserType.AGENT));
    }
    return info;
  }

  private StandardAddress extractAddress(Address esbAddress) {
    StandardAddress address = new StandardAddress();
    if (esbAddress != null) {
      address.setLkmsId(esbAddress.getLkmsId());
      address.setStreet(esbAddress.getStreet());
      address.setHouseNumber(esbAddress.getHouseNumber());
      address.setBlock(esbAddress.getBlock());
      address.setStaircase(esbAddress.getStaircase());
      address.setFloorNumber(esbAddress.getFloorNumber());
      address.setDoorNumber(esbAddress.getDoorNumber());
      address.setAdditional(esbAddress.getAdditional());
      address.setPostcode(esbAddress.getPostcode());
      address.setCity(esbAddress.getCity());
      address.setVillage(esbAddress.getVillage());
      address.setCountry(esbAddress.getCountry());
    }
    address.setDataSource(AddressDataSource.PARTY_SERVICE);
    return address;
  }

  private StandardAddress mockStandardAddress() {
    StandardAddress address = new StandardAddress();
    address.setLkmsId("1212");
    address.setStreet("Schuttelstrasse");
    address.setHouseNumber("23-25A");
    address.setBlock("25");
    address.setStaircase("0");
    address.setFloorNumber("100");
    address.setDoorNumber("1011");
    address.setAdditional("");
    address.setPostcode("1020");
    address.setCity("Wien");
    address.setVillage("Wien");
    address.setCountry("Austria");
    address.setDataSource(AddressDataSource.PARTY_SERVICE);
    return address;
  }

  @Override
  public PartyAdditionalInfo getPartyAdditionalInfo(long partyId) {
    PartyAdditionalInfo info = new PartyAdditionalInfo();
    info.setPartyProfileInfo(partyProfileService.getParty(partyId));
    info.setPartyCustomerLoyaltyInfo(partyCustomerLoyaltyService.getParty(partyId));
    return info;
  }

  @Override
  public String getPartyIdForQuoteNumber(String offerNumber) {
    return customerDao.getPartyIdForQuoteNumber(offerNumber);
  }
}
