package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class PhoneNumber implements Serializable {
  private Boolean broadbandPossible;
  private String cityIdentificationNumber;
  private String connectorSpecification;
  private Long contractNumber;
  private String countryIdentificationNumber;
  private Long customerId;
  private String unlistedNumberIdentification;
  private Long locationId;
  private Float maxDownloadRate;
  private Float maxUploadRate;
  private Short nrSTBPossible;
  private String subscriberNumber;
  private String tarifDescription;
  private Boolean tvPossible;
  private String phoneNumberSystemCd;
  private String banId;
  private String indexation;

  public Boolean getBroadbandPossible() {
    return broadbandPossible;
  }

  public void setBroadbandPossible(Boolean broadbandPossible) {
    this.broadbandPossible = broadbandPossible;
  }

  public String getCityIdentificationNumber() {
    return cityIdentificationNumber;
  }

  public void setCityIdentificationNumber(String cityIdentificationNumber) {
    this.cityIdentificationNumber = cityIdentificationNumber;
  }

  public String getConnectorSpecification() {
    return connectorSpecification;
  }

  public void setConnectorSpecification(String connectorSpecification) {
    this.connectorSpecification = connectorSpecification;
  }

  public Long getContractNumber() {
    return contractNumber;
  }

  public void setContractNumber(Long contractNumber) {
    this.contractNumber = contractNumber;
  }

  public String getCountryIdentificationNumber() {
    return countryIdentificationNumber;
  }

  public void setCountryIdentificationNumber(String countryIdentificationNumber) {
    this.countryIdentificationNumber = countryIdentificationNumber;
  }

  public Long getCustomerId() {
    return customerId;
  }

  public void setCustomerId(Long customerId) {
    this.customerId = customerId;
  }

  public Boolean getIsUnlistedNumber() {
    if (this.unlistedNumberIdentification == null || this.unlistedNumberIdentification.equalsIgnoreCase("n")) {
      return Boolean.FALSE;
    }
    return Boolean.TRUE;
  }

  public Long getLocationId() {
    return locationId;
  }

  public void setLocationId(Long locationId) {
    this.locationId = locationId;
  }

  public Float getMaxDownloadRate() {
    return maxDownloadRate;
  }

  public void setMaxDownloadRate(Float maxDownloadRate) {
    this.maxDownloadRate = maxDownloadRate;
  }

  public Short getNrSTBPossible() {
    return nrSTBPossible;
  }

  public void setNrSTBPossible(Short nrSTBPossible) {
    this.nrSTBPossible = nrSTBPossible;
  }

  public String getSubscriberNumber() {
    return subscriberNumber;
  }

  public void setSubscriberNumber(String subscriberNumber) {
    this.subscriberNumber = subscriberNumber;
  }

  public String getTarifDescription() {
    return tarifDescription;
  }

  public void setTarifDescription(String tarifDescription) {
    this.tarifDescription = tarifDescription;
  }

  public Boolean getTvPossible() {
    return tvPossible;
  }

  public void setTvPossible(Boolean tvPossible) {
    this.tvPossible = tvPossible;
  }

  public Float getMaxUploadRate() {
    return maxUploadRate;
  }

  public void setMaxUploadRate(Float maxUploadRate) {
    this.maxUploadRate = maxUploadRate;
  }

  public String getUnlistedNumberIdentification() {
    return unlistedNumberIdentification;
  }

  public void setUnlistedNumberIdentification(String unlistedNumberIdentification) {
    this.unlistedNumberIdentification = unlistedNumberIdentification;
  }

  public String getPhoneNumberSystemCd() {
    return phoneNumberSystemCd;
  }

  public void setPhoneNumberSystemCd(final String phoneNumberSystemCd) {
    this.phoneNumberSystemCd = phoneNumberSystemCd;
  }

  public void setBanId(String banId) {
    this.banId = banId;
  }

  public String getBanId() {
    return banId;
  }

  public String getIndexation() {
    return indexation;
  }

  public void setIndexation(final String indexation) {
    this.indexation = indexation;
  }

}
