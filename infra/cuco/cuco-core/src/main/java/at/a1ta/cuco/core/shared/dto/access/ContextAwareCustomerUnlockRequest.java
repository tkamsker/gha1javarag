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
package at.a1ta.cuco.core.shared.dto.access;

import java.io.Serializable;
import java.util.Date;

import at.a1ta.bite.core.shared.dto.BiteUser;

public class ContextAwareCustomerUnlockRequest implements Serializable {

  public static final UnlockStateEnum DEFAULT_STATE = UnlockStateEnum.PENDING;
  public static final UnlockRequestContext DEFAULT_CONTEXT = UnlockRequestContext.SESSION;

  private Date created = new Date();
  private Date finished;

  private long customerId;
  private BiteUser user;
  private String jobId;
  private String sessionKey;
  private UnlockStateEnum state = DEFAULT_STATE;
  private UnlockRequestContext context = DEFAULT_CONTEXT;

  public Date getCreated() {
    return created;
  }

  public void setCreated(Date created) {
    this.created = created;
  }

  public Date getFinished() {
    return finished;
  }

  public void setFinished(Date finished) {
    this.finished = finished;
  }

  public long getCustomerId() {
    return customerId;
  }

  public void setCustomerId(long customerId) {
    this.customerId = customerId;
  }

  public String getJobId() {
    return jobId;
  }

  public void setJobId(String jobId) {
    this.jobId = jobId;
  }

  public String getSessionKey() {
    return sessionKey;
  }

  public void setSessionKey(String sessionKey) {
    this.sessionKey = sessionKey;
  }

  public UnlockStateEnum getState() {
    return state;
  }

  public void setState(UnlockStateEnum state) {
    this.state = state;
  }

  public UnlockRequestContext getContext() {
    return context;
  }

  public void setContext(UnlockRequestContext context) {
    this.context = context;
  }

  public BiteUser getUser() {
    return user;
  }

  public void setUser(BiteUser user) {
    this.user = user;
  }

}
