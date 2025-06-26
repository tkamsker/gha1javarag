package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import java.util.List;

import org.springframework.util.Assert;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.dao.db.CustomerUnlockRequestDao;
import at.a1ta.cuco.core.shared.dto.access.ContextAwareCustomerUnlockRequest;

public class CustomerUnlockRequestDaoImpl extends AbstractDao implements CustomerUnlockRequestDao {

  @Override
  public void insert(ContextAwareCustomerUnlockRequest request) {
    validateRequestData(request);
    executeInsert("CustomerUnlockRequest.insert", request);
  }

  @Override
  public void update(ContextAwareCustomerUnlockRequest request) {
    validateRequestData(request);
    executeUpdate("CustomerUnlockRequest.update", request);
  }

  @Override
  public ContextAwareCustomerUnlockRequest findByCustomerIdAndUsernameAndJobIdAndSessionKey(long customerId, BiteUser user, String jobId, String sessionKey) {
    HashMap<String, Object> params = new HashMap<String, Object>(4);
    params.put("customerId", customerId);
    params.put("userId", user.getId());
    params.put("jobId", jobId);
    params.put("sessionKey", sessionKey);

    return (ContextAwareCustomerUnlockRequest) performObjectQuery("CustomerUnlockRequest.findCustomerUnlockRequestByCustomerIdAndUsernameAndJobIdAndSessionKey", params);
  }

  private void validateRequestData(ContextAwareCustomerUnlockRequest request) {
    Assert.notNull(request, "request must not be null");
    if (request.getCustomerId() <= 0) {
      throw new IllegalArgumentException("customerId cannot be less than equal to zero");
    }
    Assert.hasText(request.getJobId(), "jobId must not be null or empty");
    Assert.notNull(request.getUser(), "user must not be null");
    Assert.hasText(request.getSessionKey(), "sessionKey must not be null or empty");
  }

  @Override
  public List<ContextAwareCustomerUnlockRequest> findByCustomerIdAndUsernameAndContextKey(long customerNumber, BiteUser user, String sessionId) {
    HashMap<String, Object> params = new HashMap<String, Object>(4);
    params.put("customerId", customerNumber);
    params.put("userId", user.getId());
    params.put("sessionKey", sessionId);

    return performListQuery("CustomerUnlockRequest.findCustomerUnlockRequestByCustomerIdAndUsernameAndSessionKey", params);
  }
}
