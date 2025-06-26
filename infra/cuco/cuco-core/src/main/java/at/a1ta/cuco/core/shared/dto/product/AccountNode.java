/*
 * Copyright 2009 - 2013 by A1 Telekom Austria AG
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
package at.a1ta.cuco.core.shared.dto.product;

import at.a1ta.bite.core.shared.util.CommonUtils;

/**
 * 
 */
public class AccountNode extends BaseNode implements AccountAware {

  private String accountNumber;

  private String customerName;

  public AccountNode() {}

  @Override
  public String getAccountNumber() {
    return this.accountNumber;
  }

  @Override
  public String getText() {
    return CommonUtils.defaultString(this.accountNumber, "n/a");
  }

  public static Builder builder() {
    return new Builder();
  }

  public String getCustomerName() {
    return customerName;
  }

  public void setCustomerName(String customerName) {
    this.customerName = customerName;
  }

  public static class Builder {

    private AccountNode node;

    public Builder() {
      node = new AccountNode();
    }

    public Builder accountNumber(String accountNumber) {
      node.accountNumber = accountNumber;
      node.setId(accountNumber);
      return this;
    }

    public Builder parent(BaseNode parent) {
      node.setParent(parent);
      return this;
    }

    public AccountNode build() {
      return node;
    }
  }

}
