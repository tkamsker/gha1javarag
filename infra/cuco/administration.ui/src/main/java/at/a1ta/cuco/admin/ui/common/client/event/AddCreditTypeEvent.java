package at.a1ta.cuco.admin.ui.common.client.event;

import at.a1ta.cuco.core.shared.dto.CreditType;
import at.a1ta.framework.ui.client.event.PortletEvent;

public class AddCreditTypeEvent extends PortletEvent {
  private CreditType credit;

  public CreditType getCredit() {
    return credit;
  }

  public void setCredit(CreditType credit) {
    this.credit = credit;
  }

  public AddCreditTypeEvent(CreditType ct) {
    super(null, CuCoEventType.UPDATECREDIT_TYPES);
    setCredit(ct);
  }

}
