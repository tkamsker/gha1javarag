package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

import at.a1ta.bite.core.shared.dto.BiteUser;

public class StandardAddress implements Serializable {

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((additional == null) ? 0 : additional.hashCode());
    result = prime * result + (int) (addressId ^ (addressId >>> 32));
    result = prime * result + ((block == null) ? 0 : block.hashCode());
    result = prime * result + ((city == null) ? 0 : city.hashCode());
    result = prime * result + ((country == null) ? 0 : country.hashCode());
    result = prime * result + ((creationDate == null) ? 0 : creationDate.hashCode());
    result = prime * result + ((creationUser == null) ? 0 : creationUser.hashCode());
    result = prime * result + ((dataSource == null) ? 0 : dataSource.hashCode());
    result = prime * result + ((doorNumber == null) ? 0 : doorNumber.hashCode());
    result = prime * result + ((floorNumber == null) ? 0 : floorNumber.hashCode());
    result = prime * result + ((houseNumber == null) ? 0 : houseNumber.hashCode());
    result = prime * result + ((lastModificationDate == null) ? 0 : lastModificationDate.hashCode());
    result = prime * result + ((lastModificationUser == null) ? 0 : lastModificationUser.hashCode());
    result = prime * result + ((lkmsId == null) ? 0 : lkmsId.hashCode());
    result = prime * result + (int) (partyId ^ (partyId >>> 32));
    result = prime * result + ((postcode == null) ? 0 : postcode.hashCode());
    result = prime * result + ((staircase == null) ? 0 : staircase.hashCode());
    result = prime * result + ((street == null) ? 0 : street.hashCode());
    result = prime * result + ((village == null) ? 0 : village.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) {
      return true;
    }
    if (obj == null) {
      return false;
    }
    if (getClass() != obj.getClass()) {
      return false;
    }
    StandardAddress other = (StandardAddress) obj;
    if (additional == null) {
      if (other.additional != null) {
        return false;
      }
    } else if (!additional.equals(other.additional)) {
      return false;
    }
    if (addressId != other.addressId) {
      return false;
    }
    if (block == null) {
      if (other.block != null) {
        return false;
      }
    } else if (!block.equals(other.block)) {
      return false;
    }
    if (city == null) {
      if (other.city != null) {
        return false;
      }
    } else if (!city.equals(other.city)) {
      return false;
    }
    if (country == null) {
      if (other.country != null) {
        return false;
      }
    } else if (!country.equals(other.country)) {
      return false;
    }
    if (creationDate == null) {
      if (other.creationDate != null) {
        return false;
      }
    } else if (!creationDate.equals(other.creationDate)) {
      return false;
    }
    if (creationUser == null) {
      if (other.creationUser != null) {
        return false;
      }
    } else if (!creationUser.equals(other.creationUser)) {
      return false;
    }
    if (dataSource != other.dataSource) {
      return false;
    }
    if (doorNumber == null) {
      if (other.doorNumber != null) {
        return false;
      }
    } else if (!doorNumber.equals(other.doorNumber)) {
      return false;
    }
    if (floorNumber == null) {
      if (other.floorNumber != null) {
        return false;
      }
    } else if (!floorNumber.equals(other.floorNumber)) {
      return false;
    }
    if (houseNumber == null) {
      if (other.houseNumber != null) {
        return false;
      }
    } else if (!houseNumber.equals(other.houseNumber)) {
      return false;
    }
    if (lastModificationDate == null) {
      if (other.lastModificationDate != null) {
        return false;
      }
    } else if (!lastModificationDate.equals(other.lastModificationDate)) {
      return false;
    }
    if (lastModificationUser == null) {
      if (other.lastModificationUser != null) {
        return false;
      }
    } else if (!lastModificationUser.equals(other.lastModificationUser)) {
      return false;
    }
    if (lkmsId == null) {
      if (other.lkmsId != null) {
        return false;
      }
    } else if (!lkmsId.equals(other.lkmsId)) {
      return false;
    }
    if (partyId != other.partyId) {
      return false;
    }
    if (postcode == null) {
      if (other.postcode != null) {
        return false;
      }
    } else if (!postcode.equals(other.postcode)) {
      return false;
    }
    if (staircase == null) {
      if (other.staircase != null) {
        return false;
      }
    } else if (!staircase.equals(other.staircase)) {
      return false;
    }
    if (street == null) {
      if (other.street != null) {
        return false;
      }
    } else if (!street.equals(other.street)) {
      return false;
    }
    if (village == null) {
      if (other.village != null) {
        return false;
      }
    } else if (!village.equals(other.village)) {
      return false;
    }
    return true;
  }

  public enum AddressDataSource {
    PARTY_SERVICE, USER_INPUT, KUMS_COMMON_SERVICE
  };

  private long addressId;
  private String lkmsId;
  private long partyId;
  private String street;
  private String houseNumber;
  private String block;
  private String staircase;
  private String floorNumber;
  private String doorNumber;
  private String additional;
  private String postcode;
  private String city;
  private String village;
  private String country;

  private BiteUser creationUser;
  private Date creationDate;
  private BiteUser lastModificationUser;
  private Date lastModificationDate;

  private AddressDataSource dataSource;

  public String getLkmsId() {
    return lkmsId;
  }

  public void setLkmsId(String lkmsId) {
    this.lkmsId = lkmsId;
  }

  public String getStreet() {
    return street;
  }

  public void setStreet(String street) {
    this.street = street;
  }

  public String getHouseNumber() {
    return houseNumber;
  }

  public void setHouseNumber(String houseNumber) {
    this.houseNumber = houseNumber;
  }

  public String getBlock() {
    return block;
  }

  public void setBlock(String block) {
    this.block = block;
  }

  public String getStaircase() {
    return staircase;
  }

  public void setStaircase(String staircase) {
    this.staircase = staircase;
  }

  public String getFloorNumber() {
    return floorNumber;
  }

  public void setFloorNumber(String floorNumber) {
    this.floorNumber = floorNumber;
  }

  public String getDoorNumber() {
    return doorNumber;
  }

  public void setDoorNumber(String doorNumber) {
    this.doorNumber = doorNumber;
  }

  public String getAdditional() {
    return additional;
  }

  public void setAdditional(String additional) {
    this.additional = additional;
  }

  public String getPostcode() {
    return postcode;
  }

  public void setPostcode(String postcode) {
    this.postcode = postcode;
  }

  public String getCity() {
    return city;
  }

  public void setCity(String city) {
    this.city = city;
  }

  public String getVillage() {
    return village;
  }

  public void setVillage(String village) {
    this.village = village;
  }

  public String getCountry() {
    return country;
  }

  public void setCountry(String country) {
    this.country = country;
  }

  @Override
  public String toString() {
    return "StandardAddress [addressId=" + addressId + ", lkmsId=" + lkmsId + ", partyId=" + partyId + ", street=" + street + ", houseNumber=" + houseNumber + ", block=" + block + ", staircase="
        + staircase + ", floorNumber=" + floorNumber + ", doorNumber=" + doorNumber + ", additional=" + additional + ", postcode=" + postcode + ", city=" + city + ", village=" + village
        + ", country=" + country + ", creationUser=" + creationUser + ", creationDate=" + creationDate + ", lastModificationUser=" + lastModificationUser + ", lastModificationDate="
        + lastModificationDate + ", dataSource=" + dataSource + "]";
  }

  public long getAddressId() {
    return addressId;
  }

  public void setAddressId(long addressId) {
    this.addressId = addressId;
  }

  public BiteUser getCreationUser() {
    return creationUser;
  }

  public void setCreationUser(BiteUser creationUser) {
    this.creationUser = creationUser;
  }

  public Date getCreationDate() {
    return creationDate;
  }

  public void setCreationDate(Date creationDate) {
    this.creationDate = creationDate;
  }

  public BiteUser getLastModificationUser() {
    return lastModificationUser;
  }

  public void setLastModificationUser(BiteUser lastModificationUser) {
    this.lastModificationUser = lastModificationUser;
  }

  public Date getLastModificationDate() {
    return lastModificationDate;
  }

  public void setLastModificationDate(Date lastModificationDate) {
    this.lastModificationDate = lastModificationDate;
  }

  public AddressDataSource getDataSource() {
    return dataSource;
  }

  public void setDataSource(AddressDataSource dataSource) {
    this.dataSource = dataSource;
  }

  public long getPartyId() {
    return partyId;
  }

  public void setPartyId(long partyId) {
    this.partyId = partyId;
  }

}