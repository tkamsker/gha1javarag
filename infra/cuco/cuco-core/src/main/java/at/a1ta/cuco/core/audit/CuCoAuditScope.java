package at.a1ta.cuco.core.audit;

import at.a1ta.bite.audit.AuditScope;

public enum CuCoAuditScope implements AuditScope {
  APPLICATION, SEARCH, CUSTOMER;

  @Override
  public String getName() {
    return this.toString();
  }

}
