package at.a1ta.cuco.core.dao.esb;

import at.a1ta.cuco.core.shared.dto.ContractOwnerAssignment;

public interface CustomerAssignmentDao {

  public ContractOwnerAssignment getContractOwnerAssignmentByBan(String ban);

  public ContractOwnerAssignment getContractOwnerAssignmentByPartyId(String partyId);

}
