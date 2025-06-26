package at.a1ta.cuco.admin.ui.common.client.event;

import at.a1ta.cuco.core.shared.dto.UnknownAreaCode;
import at.a1ta.framework.ui.client.event.PortletEvent;

public class AddUnknownAreaCodeEvent extends PortletEvent {
  private UnknownAreaCode code;

  public UnknownAreaCode getCode() {
    return code;
  }

  public void setCode(UnknownAreaCode code) {
    this.code = code;
  }

  public AddUnknownAreaCodeEvent(UnknownAreaCode code) {
    super(null, CuCoEventType.UPDATEUNKNOWN_AREACODES);
    setCode(code);
  }

}
