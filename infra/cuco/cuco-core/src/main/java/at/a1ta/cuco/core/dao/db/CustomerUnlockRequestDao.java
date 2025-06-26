package at.a1ta.cuco.core.dao.db;

import java.util.List;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.shared.dto.access.ContextAwareCustomerUnlockRequest;

public interface CustomerUnlockRequestDao {

  public void insert(ContextAwareCustomerUnlockRequest request);

  public void update(ContextAwareCustomerUnlockRequest request);

  public ContextAwareCustomerUnlockRequest findByCustomerIdAndUsernameAndJobIdAndSessionKey(long customerId, BiteUser user, String jobId, String sessionKey);

  public List<ContextAwareCustomerUnlockRequest> findByCustomerIdAndUsernameAndContextKey(long customerNumber, BiteUser user, String sessionId);

}
