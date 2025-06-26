package at.a1ta.cuco.core.shared.dto;

import java.util.Date;
import java.util.List;

import at.a1ta.bite.core.shared.dto.BiteUser;

public class FlashInfo extends FlashInfoBase {

  private Date from;
  private Date to;
  private List<CustomerBlock> customerBlocks;
  private BiteUser creator;

  public Date getFrom() {
    return from;
  }

  public void setFrom(Date from) {
    this.from = from;
  }

  public Date getTo() {
    return to;
  }

  public void setTo(Date to) {
    this.to = to;
  }

  public List<CustomerBlock> getCustomerBlocks() {
    return customerBlocks;
  }

  public void setCustomerBlocks(List<CustomerBlock> customerBlocks) {
    this.customerBlocks = customerBlocks;
  }

  public BiteUser getCreator() {
    return creator;
  }

  public void setCreator(BiteUser creator) {
    this.creator = creator;
  }

  public long getCustomerCount() {
    long count = 0;
    for (CustomerBlock block : customerBlocks) {
      count += block.getCount();
    }
    return count;
  }

}
