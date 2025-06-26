package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

import at.a1ta.bite.core.shared.dto.systemmessage.PeriodOfValidity;

public class Service implements Serializable {
  private Long id;
  private PeriodOfValidity validity = new PeriodOfValidity();
  private String name;
  private String productCode;
  private Double costs;
  private String comment;
  private String product;
  private String reason1;
  private String reason2;
  private String reason3;
  private String result;
  private Long multi;
  private CreditType creditType;
  private ChargingType chargingType;
  private Long ticketcount;
  private String employeeinfo;

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public PeriodOfValidity getValidity() {
    return validity;
  }

  public void setValidity(PeriodOfValidity validity) {
    this.validity = validity;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getProductCode() {
    return productCode;
  }

  public void setProductCode(String productCode) {
    this.productCode = productCode;
  }

  public Double getCosts() {
    return costs;
  }

  public void setCosts(Double costs) {
    this.costs = costs;
  }

  public String getComment() {
    return comment;
  }

  public void setComment(String comment) {
    this.comment = comment;
  }

  public String getProduct() {
    return product;
  }

  public void setProduct(String product) {
    this.product = product;
  }

  public String getReason1() {
    return reason1;
  }

  public void setReason1(String reason1) {
    this.reason1 = reason1;
  }

  public String getReason2() {
    return reason2;
  }

  public void setReason2(String reason2) {
    this.reason2 = reason2;
  }

  public String getReason3() {
    return reason3;
  }

  public void setReason3(String reason3) {
    this.reason3 = reason3;
  }

  public String getResult() {
    return result;
  }

  public void setResult(String result) {
    this.result = result;
  }

  public Long getMulti() {
    return multi;
  }

  public void setMulti(Long multi) {
    this.multi = multi;
  }

  public CreditType getCreditType() {
    return creditType;
  }

  public void setCreditType(CreditType creditType) {
    this.creditType = creditType;
  }

  public ChargingType getChargingType() {
    return chargingType;
  }

  public void setChargingType(ChargingType chargingType) {
    this.chargingType = chargingType;
  }

  public Long getTicketcount() {
    return ticketcount;
  }

  public void setTicketcount(Long ticketcount) {
    this.ticketcount = ticketcount;
  }

  public void setEmployeeinfo(String employeeinfo) {
    this.employeeinfo = employeeinfo;
  }

  public String getEmployeeinfo() {
    return employeeinfo;
  }

  @Override
  public boolean equals(Object obj) {
    Service service = (Service) obj;
    return service != null && getId().equals(service.getId());
  }

  @Override
  public int hashCode() {
    return getId().hashCode();
  }
}
