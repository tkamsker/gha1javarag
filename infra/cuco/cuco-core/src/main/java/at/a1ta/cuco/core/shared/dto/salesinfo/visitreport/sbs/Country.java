package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs;

import java.io.Serializable;

public class Country implements Serializable {
  private String iso3166Alpha2;
  private String iso3166Alpha3;
  private String nameGerman;

  public String getIso3166Alpha2() {
    return iso3166Alpha2;
  }

  public void setIso3166Alpha2(String iso3166Alpha2) {
    this.iso3166Alpha2 = iso3166Alpha2;
  }

  public String getIso3166Alpha3() {
    return iso3166Alpha3;
  }

  public void setIso3166Alpha3(String iso3166Alpha3) {
    this.iso3166Alpha3 = iso3166Alpha3;
  }

  public String getNameGerman() {
    return nameGerman;
  }

  public void setNameGerman(String nameGerman) {
    this.nameGerman = nameGerman;
  }

  @Override
  public String toString() {
    return "Country [iso3166Alpha2=" + iso3166Alpha2 + ", iso3166Alpha3=" + iso3166Alpha3 + ", nameGerman=" + nameGerman + "]";
  }

}
