package at.a1ta.cuco.core.dao.esb;

import java.util.ArrayList;

import org.springframework.stereotype.Component;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.cuco.core.shared.dto.BillingAccountNumber;
import at.a1ta.cuco.core.shared.dto.ContractOwnerAssignment;
import at.a1telekom.eai.customerassignment.xsd.GetContractOwnerAssignmentRequest;
import at.a1telekom.eai.customerassignment.xsd.GetContractOwnerAssignmentRequest.GetBy;
import at.a1telekom.eai.customerassignment.xsd.GetContractOwnerAssignmentRequestDocument;
import at.a1telekom.eai.customerassignment.xsd.GetContractOwnerAssignmentResponse;

import com.telekomaustriagroup.esb.customerassignment.CustomerAssignmentStub;

@Component
public class CustomerAssignmentDaoImpl extends BaseEsbClient<CustomerAssignmentStub> implements CustomerAssignmentDao {

  @Override
  public ContractOwnerAssignment getContractOwnerAssignmentByBan(String ban) {
    GetContractOwnerAssignmentRequestDocument requestDocument = createGetContractOwnerAssignmentRequestDocumentByBan(ban);
    try {
      return copy(stub.getContractOwnerAssignment(requestDocument, null).getGetContractOwnerAssignmentResponse());
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }

  @Override
  public ContractOwnerAssignment getContractOwnerAssignmentByPartyId(String partyId) {
    GetContractOwnerAssignmentRequestDocument requestDocument = createGetContractOwnerAssignmentRequestDocumentByPartyId(partyId);
    try {
      return copy(stub.getContractOwnerAssignment(requestDocument, null).getGetContractOwnerAssignmentResponse());
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }

  private GetContractOwnerAssignmentRequestDocument createGetContractOwnerAssignmentRequestDocumentByBan(String ban) {
    GetContractOwnerAssignmentRequestDocument requestDocument = GetContractOwnerAssignmentRequestDocument.Factory.newInstance();
    GetContractOwnerAssignmentRequest getContractOwnerAssignmentRequest = requestDocument.addNewGetContractOwnerAssignmentRequest();
    getContractOwnerAssignmentRequest.setSourceSystem("CUCO");
    getContractOwnerAssignmentRequest.setUser("UCUCO01");
    GetBy getBy = getContractOwnerAssignmentRequest.addNewGetBy();
    getBy.setBAN(ban);
    return requestDocument;
  }

  private GetContractOwnerAssignmentRequestDocument createGetContractOwnerAssignmentRequestDocumentByPartyId(String partyId) {
    GetContractOwnerAssignmentRequestDocument requestDocument = GetContractOwnerAssignmentRequestDocument.Factory.newInstance();
    GetContractOwnerAssignmentRequest getContractOwnerAssignmentRequest = requestDocument.addNewGetContractOwnerAssignmentRequest();
    getContractOwnerAssignmentRequest.setSourceSystem("CUCO");
    getContractOwnerAssignmentRequest.setUser("UCUCO01");
    GetBy getBy = getContractOwnerAssignmentRequest.addNewGetBy();
    getBy.setPartyId(partyId);
    getContractOwnerAssignmentRequest.setListAllBANs(true);
    return requestDocument;
  }

  private ContractOwnerAssignment copy(GetContractOwnerAssignmentResponse getContractOwnerAssignmentResponse) {
    ContractOwnerAssignment contractOwnerAssignment = new ContractOwnerAssignment();
    contractOwnerAssignment.setAccounts(new ArrayList<BillingAccountNumber>());
    contractOwnerAssignment.setPartyId(getContractOwnerAssignmentResponse.getPartyId());
    if (getContractOwnerAssignmentResponse.getAccounts() != null) {
      for (at.a1telekom.eai.customerassignment.xsd.Account accountWS : getContractOwnerAssignmentResponse.getAccounts().getAccountArray()) {
        BillingAccountNumber account = new BillingAccountNumber();
        account.setBan(Long.parseLong(accountWS.getBAN()));
        contractOwnerAssignment.getAccounts().add(account);
      }
    }
    return contractOwnerAssignment;
  }

}
