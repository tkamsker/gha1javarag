package at.a1ta.cuco.core.dao.esb;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.rmi.RemoteException;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Repository;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.esb.EsbException;
import at.a1ta.cuco.core.shared.dto.mobilpoints.BusinessHardwareReplacement;
import at.mobilkom.eai.brk2.LoadBRKListRequestDocument;
import at.mobilkom.eai.brk2.LoadBRKListRequestType;
import at.mobilkom.eai.brk2.LoadBRKListResponseDocument;
import at.mobilkom.eai.brk2.LoadBRKListResponseType;
import at.mobilkom.eai.brk2.LoadBRKRequestDocument;
import at.mobilkom.eai.brk2.LoadBRKRequestType;
import at.mobilkom.eai.brk2.LoadBRKRequestType.LoadOptions;
import at.mobilkom.eai.brk2.LoadBRKResponseDocument;
import at.mobilkom.eai.brk2.LoadBRKResponseType;
import at.mobilkom.eai.common.brk.BRKType;

import com.telekomaustriagroup.esb.brksvc.BrkError;
import com.telekomaustriagroup.esb.brksvc.BrkSvcStub;

@Repository
@Scope("prototype")
public class BusinessHardwareReplacementDaoImpl extends BaseEsbClient<BrkSvcStub> implements BusinessHardwareReplacementDao {
  private static boolean LOAD_OPTIONS_GET_BASIC_INFORMATION = true;
  private static boolean LOAD_OPTIONS_GET_DATA_GROUPS = false;
  private static boolean LOAD_OPTIONS_GET_ACTIVE_SONDER_CONDITIONS = false;
  private static boolean LOAD_OPTIONS_GET_PARAMETERS = false;

  @Override
  public BusinessHardwareReplacement getBusinessHardwareReplacement(long billingAccountNumber) {
    try {
      BRKType[] businessRewardingAccounts = getBusinessRewardingAccounts(billingAccountNumber);

      if (businessRewardingAccounts == null || businessRewardingAccounts.length == 0) {
        return createEmptyBusinessHardwareReplacement(billingAccountNumber);
      }

      BigInteger possibleHWRedemptionVoice = BigInteger.ZERO;
      BigInteger nbActiveSims = BigInteger.ZERO;
      BigInteger nbOGE = BigInteger.ZERO;
      BigDecimal rmCommitmentPerSim = BigDecimal.ZERO;

      for (BRKType businessRewardingAccount : businessRewardingAccounts) {
        BRKType brk = getBusinessRewardingAccountData(businessRewardingAccount);

        possibleHWRedemptionVoice = possibleHWRedemptionVoice.add(brk.getRK().getPossibleHWRedemptionVoice());
        nbActiveSims = nbActiveSims.add(brk.getOGE().getNbActiveSims());
        nbOGE = nbOGE.add(brk.getOGE().getNbOGE());
        rmCommitmentPerSim = rmCommitmentPerSim.add(brk.getOGE().getRmCommitmentPerSim());
      }

      return createBusinessHardwareReplacementFromResponse(possibleHWRedemptionVoice, nbActiveSims, nbOGE, rmCommitmentPerSim, billingAccountNumber);
    } catch (RemoteException e) {
      throw new EsbException(e);
    } catch (BrkError e) {
      throw new EsbException(e);
    }
  }

  private BusinessHardwareReplacement createEmptyBusinessHardwareReplacement(long billingAccountNumber) {
    BusinessHardwareReplacement data = new BusinessHardwareReplacement();
    data.setBillingAccountNumber(billingAccountNumber);
    data.setBusinessRewardingAccountsAvailable(false);
    return data;
  }

  private BusinessHardwareReplacement createBusinessHardwareReplacementFromResponse(BigInteger possibleHWRedemptionVoice, BigInteger nbActiveSims, BigInteger nbOGE, BigDecimal rmCommitmentPerSim, long billingAccountNumber) {
    BusinessHardwareReplacement data = new BusinessHardwareReplacement();
    data.setBillingAccountNumber(billingAccountNumber);
    data.setPossibleHardwareReplacement(possibleHWRedemptionVoice);
    data.setSimCount(nbActiveSims);
    data.setOpenBasicFeePerBan(nbOGE);
    data.setBindingMonthsPerSim(rmCommitmentPerSim);
    return data;
  }

  private BRKType getBusinessRewardingAccountData(BRKType businessRewardingAccount) throws RemoteException, BrkError {
    LoadBRKRequestDocument requestDocument = createLoadBRKRequestDocument(businessRewardingAccount);

    LoadBRKResponseDocument responseDocument = stub.loadBRK(requestDocument, null);
    LoadBRKResponseType response = responseDocument.getLoadBRKResponse();

    return response.getBRK();
  }

  private LoadBRKRequestDocument createLoadBRKRequestDocument(BRKType businessRewardingAccount) {
    LoadBRKRequestType request = LoadBRKRequestType.Factory.newInstance();
    request.setBrkAccountNumber(businessRewardingAccount.getAccountNumber());
    request.setLoadOptions(createLoadOptions());

    LoadBRKRequestDocument requestDocument = LoadBRKRequestDocument.Factory.newInstance();
    requestDocument.setLoadBRKRequest(request);

    return requestDocument;
  }

  private LoadOptions createLoadOptions() {
    LoadOptions loadOptions = LoadOptions.Factory.newInstance();
    loadOptions.setGetBasicInformation(LOAD_OPTIONS_GET_BASIC_INFORMATION);
    loadOptions.setGetDataGroups(LOAD_OPTIONS_GET_DATA_GROUPS);
    loadOptions.setGetActiveSonderConditions(LOAD_OPTIONS_GET_ACTIVE_SONDER_CONDITIONS);
    loadOptions.setGetParameters(LOAD_OPTIONS_GET_PARAMETERS);
    return loadOptions;
  }

  private BRKType[] getBusinessRewardingAccounts(long billingAccountNumber) throws RemoteException, com.telekomaustriagroup.esb.brksvc.BrkError {
    LoadBRKListRequestDocument requestDocument = createLoadBRKListRequestDocument(billingAccountNumber);

    LoadBRKListResponseDocument responseDocument = stub.loadBRKList(requestDocument, null);
    LoadBRKListResponseType response = responseDocument.getLoadBRKListResponse();

    return response.getBRKArray();
  }

  private LoadBRKListRequestDocument createLoadBRKListRequestDocument(long billingAccountNumber) {
    LoadBRKListRequestType request = LoadBRKListRequestType.Factory.newInstance();
    request.setBAN(billingAccountNumber + "");

    LoadBRKListRequestDocument requestDocument = LoadBRKListRequestDocument.Factory.newInstance();
    requestDocument.setLoadBRKListRequest(request);
    return requestDocument;
  }
}
