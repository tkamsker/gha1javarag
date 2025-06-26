package at.a1ta.cuco.core.shared.dto.tariff;

import java.io.Serializable;
import java.util.Collections;
import java.util.List;

public class TariffLists implements Serializable {
  private List<Tariff> allTariffsList;
  private List<Tariff> recommendedTariffsList;

  public TariffLists() {}

  public TariffLists(List<Tariff> allTariffsList, List<Tariff> recommendedTariffsList) {
    this.allTariffsList = allTariffsList != null ? allTariffsList : Collections.<Tariff> emptyList();
    this.recommendedTariffsList = recommendedTariffsList != null ? recommendedTariffsList : Collections.<Tariff> emptyList();
  }

  public List<Tariff> getAllTariffsList() {
    return allTariffsList;
  }

  public void setAllTariffsList(List<Tariff> allTariffsList) {
    this.allTariffsList = allTariffsList;
  }

  public List<Tariff> getRecommendedTariffsList() {
    return recommendedTariffsList;
  }

  public void setRecommendedTariffsList(List<Tariff> recommendedTariffsList) {
    this.recommendedTariffsList = recommendedTariffsList;
  }

}
