package at.a1ta.cuco.core.shared.dto.tariff;

import java.io.Serializable;

import at.a1ta.cuco.core.shared.dto.BillingAccountNumber;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;
import at.mobilkom.bit.tariffguide.SimulationType;

/**
 * @author q907291
 */
public class TariffSimulationRequest implements Serializable {

  private PhoneNumberStructure phoneNumber;
  private BillingAccountNumber billingAccountNumber;
  private SimulationType.Enum simulationType;

  public PhoneNumberStructure getPhoneNumber() {
    return phoneNumber;
  }

  public void setPhoneNumber(PhoneNumberStructure phoneNumber) {
    this.phoneNumber = phoneNumber;
  }

  public BillingAccountNumber getBillingAccountNumber() {
    return billingAccountNumber;
  }

  public void setBillingAccountNumber(BillingAccountNumber billingAccountNumber) {
    this.billingAccountNumber = billingAccountNumber;
  }

  public SimulationType.Enum getSimulationType() {
    return simulationType;
  }

  public void setSimulationType(SimulationType.Enum simulationType) {
    this.simulationType = simulationType;
  }

  @Override
  public String toString() {
    return "TariffSimulationRequest [phoneNumber=" + phoneNumber + ", billingAccountNumber=" + billingAccountNumber + ", simulationType=" + simulationType + "]";
  }

}
