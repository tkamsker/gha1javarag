package at.a1ta.cuco.core.shared.dto.tariff;

import java.io.Serializable;

import at.a1ta.cuco.core.shared.dto.Message;

/**
 * @author Wahl Tatiana <Tatiana.Wahl@a1telekom.at>
 */
public class TariffSimulationContainer implements Serializable {
  private Tariff currentTariff;
  private TariffLists tariffLists;
  private Message esbResponseMessage;

  public TariffSimulationContainer() {}

  public TariffSimulationContainer(Tariff currentTariff, TariffLists tariffLists, Message message) {
    this.currentTariff = currentTariff;
    this.tariffLists = tariffLists;
    this.esbResponseMessage = message;
  }

  public Tariff getCurrentTariff() {
    return currentTariff;
  }

  public void setCurrentTariff(Tariff currentTariff) {
    this.currentTariff = currentTariff;
  }

  public void setEsbResponseMessage(Message message) {
    this.esbResponseMessage = message;
  }

  public Message getEsbResponseMessage() {
    return esbResponseMessage;
  }

  public boolean hasNegativeEsbResponse() {
    return (esbResponseMessage != null && (Message.Type.WARN.equals(esbResponseMessage.getType()) || Message.Type.ERROR.equals(esbResponseMessage.getType())));
  }

  public TariffLists getTariffLists() {
    return tariffLists;
  }

  public void setTariffLists(TariffLists tariffLists) {
    this.tariffLists = tariffLists;
  }

}
