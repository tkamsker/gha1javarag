package at.a1ta.cuco.core.shared.dto.tariff;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

import at.a1ta.cuco.core.shared.dto.tariff.ContributionMargin.Indicator;

public class Tariff implements Serializable {

  public static final Tariff UNKNOWN = new Tariff("unknown");

  public Tariff() {}

  public Tariff(String name) {
    this.name = name;
  }

  private String id;
  private String name;
  private String code;
  private Price baseFee;
  private ContributionMargin contributionMargin;
  private boolean expanded = false;
  private List<TariffCharacteristic> characteristics = new ArrayList<TariffCharacteristic>(0);
  private List<String> recommendationReasons = new ArrayList<String>(1);

  private boolean hasExpander;
  private boolean visible;
  private boolean showParentInformation;
  private boolean showChildInformation;
  private String type;

  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getCode() {
    return code;
  }

  public void setCode(String code) {
    this.code = code;
  }

  public void setBaseFee(Price baseFee) {
    this.baseFee = baseFee;
  }

  public Price getBaseFee() {
    return baseFee;
  }

  public void setType(String type) {
    this.type = type;
  }

  public String getType() {
    return type;
  }

  public void setCharacteristics(List<TariffCharacteristic> characteristics) {
    this.characteristics = characteristics;
  }

  public List<TariffCharacteristic> getCharacteristics() {
    return characteristics;
  }

  public void addCharacteristic(TariffCharacteristic characteristic) {
    this.characteristics.add(characteristic);
  }

  public void setContributionMargin(ContributionMargin contributionMargin) {
    this.contributionMargin = contributionMargin;
  }

  public ContributionMargin getContributionMargin() {
    return contributionMargin;
  }

  public boolean hasPositiveContributionMargin() {
    return getContributionMargin() != null && getContributionMargin().getIndicator() == Indicator.GREEN;
  }

  public boolean isRecommended() {
    return !this.recommendationReasons.isEmpty();
  }

  public boolean hasExpander() {
    return hasExpander;
  }

  public void setHasExpander(boolean hasExpander) {
    this.hasExpander = hasExpander;
  }

  public boolean isVisible() {
    return visible;
  }

  public void setVisible(boolean visible) {
    this.visible = visible;
  }

  public boolean showParentInformation() {
    return showParentInformation;
  }

  public void setShowParentInformation(boolean showParentInformation) {
    this.showParentInformation = showParentInformation;
  }

  public boolean showChildInformation() {
    return showChildInformation;
  }

  public void setShowChildInformation(boolean showChildInformation) {
    this.showChildInformation = showChildInformation;
  }

  public void setExpanded(boolean expanded) {
    this.expanded = expanded;
  }

  public boolean isExpanded() {
    return expanded;
  }

  public void addRecommendationReason(String reason) {
    this.recommendationReasons.add(reason);
  }

  public void addRecommendationReasons(Collection<String> reasons) {
    this.recommendationReasons.addAll(reasons);
  }

  public List<String> getRecommendationReasons() {
    return Collections.unmodifiableList(recommendationReasons);
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((name == null) ? 0 : name.hashCode());
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
    Tariff other = (Tariff) obj;
    if (name == null) {
      if (other.name != null) {
        return false;
      }
    } else if (!name.equals(other.name)) {
      return false;
    }
    return true;
  }
}
