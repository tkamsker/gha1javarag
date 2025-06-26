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
package at.a1ta.cuco.core.audit;

import at.a1ta.bite.audit.AuditAttribute;
import at.a1ta.bite.audit.core.SimpleAuditEvent;
import at.a1ta.bite.core.bean.AuthenticatedSessionContext;

public class CuCoAuditEvent extends SimpleAuditEvent {

  public CuCoAuditEvent(String username, CuCoAuditScope scope, CuCoAuditActivity activity) {
    super(username, scope, activity);
  }

  public CuCoAuditEvent(String username, CuCoAuditScope scope, CuCoAuditActivity activity, AuditAttribute... attributes) {
    super(username, scope, activity);
    this.addAttributes(attributes);
  }

  public CuCoAuditEvent(AuthenticatedSessionContext context, CuCoAuditScope scope, CuCoAuditActivity activity) {
    super(context != null ? context.getUsername() : "-", scope, activity);
    this.withContext(context);
  }

  public CuCoAuditEvent withIP(String ipaddress) {
    return withAttribute(CuCoAuditAttribute.IP_ADDRESS.withValue(ipaddress));
  }

  public CuCoAuditEvent withSession(String sessionid) {
    return withAttribute(CuCoAuditAttribute.SESSION_ID.withValue(sessionid));
  }

  public CuCoAuditEvent withError(String errormessage) {
    return withAttribute(CuCoAuditAttribute.ERROR_MESSAGE.withValue(errormessage));
  }

  public CuCoAuditEvent withReferenceNumber(String referenceNumber) {
    return withAttribute(CuCoAuditAttribute.REFERENCE_NUMBER.withValue(referenceNumber));
  }

  public CuCoAuditEvent withUsername(String username) {
    return withAttribute(CuCoAuditAttribute.USERNAME.withValue(username));
  }

  public CuCoAuditEvent withCustomerNumber(long customerNumber) {
    return withAttribute(CuCoAuditAttribute.CUSTOMERNUMBER.withValue(Long.toString(customerNumber)));
  }

  public CuCoAuditEvent withAttribute(AuditAttribute attribute) {
    this.addAttribute(attribute);
    return this;
  }

  public CuCoAuditEvent withContext(AuthenticatedSessionContext context) {
    if (context != null) {
      return withSession(context.getSessionId()).withIP(context.getIpAddress()).withUsername(context.getUsername());
    }
    return this;
  }

  public CuCoAuditEvent withMessage(String message, Object... args) {
    this.setMessage(message);
    this.setArgumentArray(args);
    return this;
  }
}
