/*
 * Copyright 2009 - 2012 by A1 Telekom Austria AG
 * All Rights Reserved.
 * 
 * The Software is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * All information contained herein is, and remains the property of
 * A1 Telekom Austria AG and its suppliers, if any.
 * The intellectual and technical concepts contained herein are proprietary
 * to A1 Telekom Austria AG and its suppliers and may be covered by
 * intertional or national patents, patents in process, and are protected
 * by trade secret or copyright law. Dissemination of this information or
 * reproduction of this material is strictly forbidden unless prior written
 * permission is obtained from A1 Telekom Austria AG.
 */
package at.a1ta.cuco.core.shared.dto.tariff;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import at.a1ta.cuco.core.shared.dto.Message;

public class TariffSimulation implements Serializable {

  private Tariff currentTariff;
  private List<Tariff> simulation;
  private Message additionalInformation;

  public static final TariffSimulation NONE = new TariffSimulation() {

  };

  public Tariff getCurrentTariff() {
    return currentTariff;
  }

  public void setCurrentTariff(Tariff currentTariff) {
    this.currentTariff = currentTariff;
  }

  public List<Tariff> getSimulation() {
    return simulation;
  }

  public void setSimulation(List<Tariff> simulation) {
    this.simulation = simulation;
  }

  public void addTariff(Tariff tariff) {
    if (simulation == null) {
      simulation = new ArrayList<Tariff>();
    }
    int index = simulation.lastIndexOf(tariff);
    if (index > -1) {
      simulation.add(index + 1, tariff);
    } else {
      simulation.add(tariff);
    }

  }

  public void setAdditionalInformation(Message additionalInformation) {
    this.additionalInformation = additionalInformation;
  }

  public Message getAdditionalInformation() {
    return additionalInformation;
  }
}
