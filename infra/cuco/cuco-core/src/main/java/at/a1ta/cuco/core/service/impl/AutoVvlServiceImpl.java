package at.a1ta.cuco.core.service.impl;

import java.util.Calendar;
import java.util.Date;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.service.TextService;
import at.a1ta.cuco.core.service.AutoVvlService;
import at.a1ta.cuco.core.shared.dto.product.AutoVvlInfo;
import at.a1ta.cuco.core.shared.dto.product.AutoVvlInfo.AutoVvlStatus;
import at.a1ta.cuco.core.shared.dto.product.CallNumber;
import at.a1telekom.cdm.common.TimePeriod;
import at.a1telekom.cdm.common.error.ErrorDetailsDocument;
import at.a1telekom.cdm.common.error.ErrorDetailsType;
import at.a1telekom.eai.customerinventorytermination.ADXAccount;
import at.a1telekom.eai.customerinventorytermination.GetTerminationInformationForADXAccountRequest;
import at.a1telekom.eai.customerinventorytermination.GetTerminationInformationForADXAccountRequestDocument;
import at.a1telekom.eai.customerinventorytermination.GetTerminationInformationForADXAccountResponse;
import at.a1telekom.eai.customerinventorytermination.GetTerminationInformationForADXAccountResponse.AutoExtendedCommitmentContract;
import at.a1telekom.eai.customerinventorytermination.GetTerminationInformationForADXAccountResponse.AutoExtendedCommitmentContract.CommitmentDuration;
import at.a1telekom.eai.customerinventorytermination.GetTerminationInformationForADXAccountResponseDocument;
import at.a1telekom.eai.customerinventorytermination.GetTerminationInformationForSubscriptionRequest;
import at.a1telekom.eai.customerinventorytermination.GetTerminationInformationForSubscriptionRequestDocument;
import at.a1telekom.eai.customerinventorytermination.GetTerminationInformationForSubscriptionResponse;
import at.a1telekom.eai.customerinventorytermination.GetTerminationInformationForSubscriptionResponse.AutoExtendedCommitment;
import at.a1telekom.eai.customerinventorytermination.GetTerminationInformationForSubscriptionResponseDocument;

import com.telekomaustriagroup.esb.customerinventorytermination.CustomerInventoryTerminationStub;
import com.telekomaustriagroup.esb.customerinventorytermination.Error;

@Service
public class AutoVvlServiceImpl extends BaseEsbClient<CustomerInventoryTerminationStub> implements AutoVvlService {

  @Autowired
  TextService textService;

  @Override
  public AutoVvlInfo getAutoVvlInfoByCallNumber(CallNumber callNumber) {
    try {
      GetTerminationInformationForSubscriptionRequestDocument reqDoc = GetTerminationInformationForSubscriptionRequestDocument.Factory.newInstance();
      GetTerminationInformationForSubscriptionRequest request = reqDoc.addNewGetTerminationInformationForSubscriptionRequest();

      request.setCallNumber(createCallnumber(callNumber, request));

      GetTerminationInformationForSubscriptionResponseDocument respDoc = stub.getTerminationInformationForSubscription(reqDoc, null);
      GetTerminationInformationForSubscriptionResponse response = respDoc.getGetTerminationInformationForSubscriptionResponse();

      if (response != null) {
        AutoVvlInfo autoVvlInfo = new AutoVvlInfo();
        AutoExtendedCommitment autoExtendedCommitment = response.getAutoExtendedCommitment();
        autoVvlInfo.setAutoVvlStatus(mapAutoVvlStatus(autoExtendedCommitment));
        if (autoExtendedCommitment != null) {
          TimePeriod actPeriod = autoExtendedCommitment.getActPeriod();
          if (actPeriod != null) {
            if (actPeriod.getStartDateTime() != null) {
              autoVvlInfo.setAutoExtendedCommitmentActPeriodStartTime(actPeriod.getStartDateTime().getTime());

            }
            if (actPeriod.getEndDateTime() != null) {
              autoVvlInfo.setAutoExtendedCommitmentActPeriodEndTime(actPeriod.getEndDateTime().getTime());
            }
          }

          TimePeriod nextPeriod = autoExtendedCommitment.getNextPeriod();
          if (nextPeriod != null) {
            if (nextPeriod.getStartDateTime() != null) {
              autoVvlInfo.setAutoExtendedCommitmentNextPeriodStartTime(nextPeriod.getStartDateTime().getTime());
              autoVvlInfo.setCancellationDateBeforeNextAutoVVL(subtractOneDay(nextPeriod.getStartDateTime().getTime()));

            }
            if (nextPeriod.getEndDateTime() != null) {
              autoVvlInfo.setAutoExtendedCommitmentNextPeriodEndTime(nextPeriod.getEndDateTime().getTime());
            }
          }
        }

        Calendar latestCommitmentEndDate = response.getLatestCommitmentEndDate();
        if (latestCommitmentEndDate != null) {
          autoVvlInfo.setLatestCommitmentEndDate(latestCommitmentEndDate.getTime());
        }

        return autoVvlInfo;
      }
    } catch (Error err) {
      ErrorDetailsDocument faultMessage = err.getFaultMessage();
      ErrorDetailsType errorDetails = faultMessage.getErrorDetails();

      if (!errorDetails.getIsTechnical() && "CUSTINV-1001".equals(errorDetails.getErrorCode())) {
        AutoVvlInfo autoVvlInfo = new AutoVvlInfo();
        autoVvlInfo.setAutoVvlStatus(AutoVvlStatus.KEINE_VEREINBARUNG);
        return autoVvlInfo;
      }
      throw new RuntimeException(err);
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
    return null;

  }

  private at.a1telekom.cdm.common.CallNumber createCallnumber(CallNumber callNumber, GetTerminationInformationForSubscriptionRequest request) {
    at.a1telekom.cdm.common.CallNumber cn = request.addNewCallNumber();
    if (callNumber != null) {
      cn.setCC(callNumber.getCountryCode());
      cn.setNDC(callNumber.getOnkz());
      cn.setSN(callNumber.getTnum());
    }
    return cn;
  }

  @Override
  public AutoVvlInfo getAutoVvlInfoByBan(String ban) {
    try {
      GetTerminationInformationForADXAccountRequestDocument reqDoc = GetTerminationInformationForADXAccountRequestDocument.Factory.newInstance();
      GetTerminationInformationForADXAccountRequest request = reqDoc.addNewGetTerminationInformationForADXAccountRequest();

      ADXAccount account = request.addNewADXAccount();
      account.setAccountNumber(ban);

      GetTerminationInformationForADXAccountResponseDocument respDoc = stub.getTerminationInformationForADXAccount(reqDoc, null);
      GetTerminationInformationForADXAccountResponse response = respDoc.getGetTerminationInformationForADXAccountResponse();

      if (response != null) {
        AutoVvlInfo autoVvlInfo = new AutoVvlInfo();
        AutoExtendedCommitmentContract autoExtendedCommitmentContract = response.getAutoExtendedCommitmentContract();

        autoVvlInfo.setAutoVvlStatus(mapAutoVvlStatus(autoExtendedCommitmentContract));

        if (autoExtendedCommitmentContract != null) {
          CommitmentDuration commitmentDuration = autoExtendedCommitmentContract.getCommitmentDuration();
          if (commitmentDuration != null) {
            autoVvlInfo.setCommitmentDuration(createCommitmentDuration(autoExtendedCommitmentContract));
            if (commitmentDuration.getStartDateTime() != null) {
              autoVvlInfo.setCommitmentDurationStartTime(commitmentDuration.getStartDateTime().getTime());
            }
          }

          at.a1telekom.eai.customerinventorytermination.GetTerminationInformationForADXAccountResponse.AutoExtendedCommitmentContract.AutoExtendedCommitment autoExtendedCommitment = autoExtendedCommitmentContract.getAutoExtendedCommitment();

          if (autoExtendedCommitment != null) {
            TimePeriod actPeriod = autoExtendedCommitment.getActPeriod();
            if (actPeriod != null) {
              if (actPeriod.getStartDateTime() != null) {
                autoVvlInfo.setAutoExtendedCommitmentActPeriodStartTime(actPeriod.getStartDateTime().getTime());
              }
              if (actPeriod.getEndDateTime() != null) {
                autoVvlInfo.setAutoExtendedCommitmentActPeriodEndTime(actPeriod.getEndDateTime().getTime());
              }
            }

            TimePeriod nextPeriod = autoExtendedCommitment.getNextPeriod();
            if (nextPeriod != null) {
              if (nextPeriod.getStartDateTime() != null) {
                autoVvlInfo.setAutoExtendedCommitmentNextPeriodStartTime(nextPeriod.getStartDateTime().getTime());
                autoVvlInfo.setCancellationDateBeforeNextAutoVVL(subtractThreeMonth(nextPeriod.getStartDateTime().getTime()));
              }
              if (nextPeriod.getEndDateTime() != null) {
                autoVvlInfo.setAutoExtendedCommitmentNextPeriodEndTime(nextPeriod.getEndDateTime().getTime());
              }
            }
          }

        }

        Calendar latestCommitmentEndDate = response.getLatestCommitmentEndDate();
        if (latestCommitmentEndDate != null) {
          autoVvlInfo.setLatestCommitmentEndDate(latestCommitmentEndDate.getTime());
        }

        return autoVvlInfo;
      }
    } catch (Error err) {
      ErrorDetailsDocument faultMessage = err.getFaultMessage();
      ErrorDetailsType errorDetails = faultMessage.getErrorDetails();

      if (!errorDetails.getIsTechnical() && "CUSTINV-1002".equals(errorDetails.getErrorCode())) {
        AutoVvlInfo autoVvlInfo = new AutoVvlInfo();
        autoVvlInfo.setAutoVvlStatus(AutoVvlStatus.KEINE_VEREINBARUNG);
        return autoVvlInfo;
      }
      throw new RuntimeException(err);
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
    return null;
  }

  private String createCommitmentDuration(AutoExtendedCommitmentContract autoExtendedCommitmentContract) {

    int commitmentDuration = autoExtendedCommitmentContract.getCommitmentDuration().getDuration();

    String commitmentDurationUnit = autoExtendedCommitmentContract.getCommitmentDuration().getDurationUnit().toString();
    textService.getByKeyWithDefaultText("productBrowserDetails_AutoVvl_DurationUnit_Enum_" + commitmentDurationUnit, commitmentDurationUnit);

    return commitmentDuration + " " + commitmentDurationUnit;
  }

  private AutoVvlStatus mapAutoVvlStatus(AutoExtendedCommitment commitment) {
    if (commitment == null) {
      return AutoVvlStatus.KEINE_VEREINBARUNG;
    }

    return commitment.getAcceptance() ? AutoVvlStatus.JA : AutoVvlStatus.NEIN;
  }

  private AutoVvlStatus mapAutoVvlStatus(AutoExtendedCommitmentContract commitment) {
    if (commitment == null) {
      return AutoVvlStatus.KEINE_VEREINBARUNG;
    }
    return commitment.getAcceptance() ? AutoVvlStatus.JA : AutoVvlStatus.NEIN;
  }

  private Date subtractThreeMonth(Date date) {
    return calcDate(date, Calendar.MONTH, -3);
  }

  private Date subtractOneDay(Date date) {
    return calcDate(date, Calendar.DAY_OF_YEAR, -1);
  }

  private Date calcDate(Date date, int unit, int amount) {
    if (date != null) {
      Calendar calendar = Calendar.getInstance();
      calendar.setTime(date);
      calendar.add(unit, amount);
      return calendar.getTime();
    }
    return null;
  }

}
