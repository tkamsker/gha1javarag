package at.a1ta.cuco.core.shared.dto.salesinfo;

import java.util.Date;

import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.CommunicationChannel;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.CommunicationType;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.ContactSource;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.ContactType;

public class SbsNoteReportRow {

  String userName;
  String me1;
  String me2;
  String me3;
  String me4;
  CommunicationType communicationType;
  CommunicationChannel communicationChannel;
  ContactType contactType;
  ContactSource contactSource;
  Date startDate;

  public String getMeAtLevel(int level) {
    switch (level) {
      case 1:
        return me1;
      case 2:
        return me2;
      case 3:
        return me3;
      case 4:
        return me4;
      default:
        return null;
    }
  }

  public String getUserName() {
    return userName;
  }

  public void setUserName(String userName) {
    this.userName = userName;
  }

  public String getMe1() {
    return me1;
  }

  public void setMe1(String me1) {
    this.me1 = me1;
  }

  public String getMe2() {
    return me2;
  }

  public void setMe2(String me2) {
    this.me2 = me2;
  }

  public String getMe3() {
    return me3;
  }

  public void setMe3(String me3) {
    this.me3 = me3;
  }

  public String getMe4() {
    return me4;
  }

  public void setMe4(String me4) {
    this.me4 = me4;
  }

  public CommunicationType getCommunicationType() {
    return communicationType;
  }

  public void setCommunicationType(CommunicationType communicationType) {
    this.communicationType = communicationType;
  }

  public CommunicationChannel getCommunicationChannel() {
    return communicationChannel;
  }

  public void setCommunicationChannel(CommunicationChannel communicationChannel) {
    this.communicationChannel = communicationChannel;
  }

  public ContactType getContactType() {
    return contactType;
  }

  public void setContactType(ContactType contactType) {
    this.contactType = contactType;
  }

  public ContactSource getContactSource() {
    return contactSource;
  }

  public void setContactSource(ContactSource contactSource) {
    this.contactSource = contactSource;
  }

  public Date getStartDate() {
    return startDate;
  }

  public void setStartDate(Date startDate) {
    this.startDate = startDate;
  }

  @Override
  public String toString() {
    return "SbsNoteReportRow [userName=" + userName + ", me1=" + me1 + ", me2=" + me2 + ", me3=" + me3 + ", me4=" + me4 + ", communicationType=" + communicationType + ", communicationChannel=" + communicationChannel + ", contactType=" + contactType + ", contactSource=" + contactSource
        + ", startDate=" + startDate + "]";
  }
}