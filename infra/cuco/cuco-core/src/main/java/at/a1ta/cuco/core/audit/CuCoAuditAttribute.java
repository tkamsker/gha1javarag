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

public enum CuCoAuditAttribute {
  IP_ADDRESS, SESSION_ID, ERROR_MESSAGE, REFERENCE_NUMBER, USERNAME, CUSTOMERNUMBER;

  public AuditAttribute withValue(final String value) {
    return new AuditAttribute() {

      @Override
      public String getName() {
        return CuCoAuditAttribute.this.toString();
      }

      @Override
      public Object getValue() {
        return value;
      }

    };
  }

}
