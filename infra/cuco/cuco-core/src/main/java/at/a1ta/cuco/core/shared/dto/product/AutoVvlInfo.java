package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;
import java.util.Date;

public class AutoVvlInfo implements Serializable {

  public enum AutoVvlStatus {
    JA, NEIN, KEINE_VEREINBARUNG;
  }

  private AutoVvlStatus autoVvlStatus;
  private Date latestCommitmentEndDate;
  private String commitmentDuration;
  private Date commitmentDurationStartTime;

  private Date autoExtendedCommitmentActPeriodStartTime;
  private Date autoExtendedCommitmentActPeriodEndTime;

  private Date autoExtendedCommitmentNextPeriodStartTime;
  private Date autoExtendedCommitmentNextPeriodEndTime;

  private Date cancellationDateBeforeNextAutoVVL;

  public Date getLatestCommitmentEndDate() {
    return latestCommitmentEndDate;
  }

  public void setLatestCommitmentEndDate(Date latestCommitmentEndDate) {
    this.latestCommitmentEndDate = latestCommitmentEndDate;
  }

  public String getCommitmentDuration() {
    return commitmentDuration;
  }

  public void setCommitmentDuration(String commitmentDuration) {
    this.commitmentDuration = commitmentDuration;
  }

  public Date getCommitmentDurationStartTime() {
    return commitmentDurationStartTime;
  }

  public void setCommitmentDurationStartTime(Date commitmentDurationStartTime) {
    this.commitmentDurationStartTime = commitmentDurationStartTime;
  }

  public Date getAutoExtendedCommitmentNextPeriodStartTime() {
    return autoExtendedCommitmentNextPeriodStartTime;
  }

  public void setAutoExtendedCommitmentNextPeriodStartTime(Date autoExtendedCommitmentNextPeriodStartTime) {
    this.autoExtendedCommitmentNextPeriodStartTime = autoExtendedCommitmentNextPeriodStartTime;
  }

  public Date getAutoExtendedCommitmentActPeriodStartTime() {
    return autoExtendedCommitmentActPeriodStartTime;
  }

  public void setAutoExtendedCommitmentActPeriodStartTime(Date autoExtendedCommitmentActPeriodStartTime) {
    this.autoExtendedCommitmentActPeriodStartTime = autoExtendedCommitmentActPeriodStartTime;
  }

  public AutoVvlStatus getAutoVvlStatus() {
    return autoVvlStatus;
  }

  public void setAutoVvlStatus(AutoVvlStatus autoVvlStatus) {
    this.autoVvlStatus = autoVvlStatus;
  }

  public Date getAutoExtendedCommitmentActPeriodEndTime() {
    return autoExtendedCommitmentActPeriodEndTime;
  }

  public void setAutoExtendedCommitmentActPeriodEndTime(Date autoExtendedCommitmentActPeriodEndTime) {
    this.autoExtendedCommitmentActPeriodEndTime = autoExtendedCommitmentActPeriodEndTime;
  }

  public Date getAutoExtendedCommitmentNextPeriodEndTime() {
    return autoExtendedCommitmentNextPeriodEndTime;
  }

  public void setAutoExtendedCommitmentNextPeriodEndTime(Date autoExtendedCommitmentNextPeriodEndTime) {
    this.autoExtendedCommitmentNextPeriodEndTime = autoExtendedCommitmentNextPeriodEndTime;
  }

  public void setCancellationDateBeforeNextAutoVVL(Date cancellationDateBeforeNextAutoVVL) {
    this.cancellationDateBeforeNextAutoVVL = cancellationDateBeforeNextAutoVVL;
  }

  public Date getCancellationDateBeforeNextAutoVVL() {
    return cancellationDateBeforeNextAutoVVL;
  }

}
