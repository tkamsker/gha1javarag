package at.a1ta.cuco.core.dao.esb;

import static org.mockito.Matchers.*;
import static org.mockito.Mockito.*;

import java.rmi.RemoteException;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.core.server.esb.EsbException;
import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.shared.dto.PayableTicket;
import at.a1ta.cuco.core.shared.dto.PhoneNumber;
import at.mobilkom.brian.wsdl.BrianSisAddCreditRequestDocument;
import at.mobilkom.eai.esb.EsbParam;

import com.telekomaustriagroup.esb.briana1.BrianA1Stub;
import com.telekomaustriagroup.esb.briana1.BwsErrMsg;

@RunWith(MockitoJUnitRunner.class)
public class EsbBrianDaoTest {

  @Mock
  private BrianA1Stub brainA1Stub;

  private BrianDaoImpl brianDao = new BrianDaoImpl();
  private BiteUser user;

  @Before
  public void setUp() {
    user = new BiteUser();
    user.setUsername("darkknight");
    user.setFirstName("Bat");
    user.setLastName("Man");
    brianDao.setStub(brainA1Stub);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testAddCreditThrowsIllegalArgumentExceptionWhenCalledWithNull() {
    brianDao.addCreditRecord(null);
  }

  @Test
  public void testAddCreditSendsCreditRequestCorrectly() throws RemoteException, BwsErrMsg {
    PayableTicket ticket = PayableTicket.builder().forPhoneNumber(createPhoneNumber()).disposeExpenses(100D).createdBy(user).withProductCode("#s2gx").build();

    brianDao.addCreditRecord(ticket);

    verify(brainA1Stub, timeout(1)).brianSisAddCredit(any(BrianSisAddCreditRequestDocument.class), isNull(EsbParam.class));
  }

  @SuppressWarnings("unchecked")
  @Test(expected = EsbException.class)
  public void testAddCreditThrowsEsbExceptionOnRemoteFault() throws RemoteException, BwsErrMsg {
    PayableTicket ticket = PayableTicket.builder().forPhoneNumber(createPhoneNumber()).disposeExpenses(100D).createdBy(user).withProductCode("#s2gx").build();

    when(brainA1Stub.brianSisAddCredit(any(BrianSisAddCreditRequestDocument.class), isNull(EsbParam.class))).thenThrow(RemoteException.class);
    brianDao.addCreditRecord(ticket);
  }

  @SuppressWarnings("unchecked")
  @Test(expected = EsbException.class)
  public void testAddCreditThorwsEsbEceptionBwsError() throws RemoteException, BwsErrMsg {
    PayableTicket ticket = PayableTicket.builder().forPhoneNumber(createPhoneNumber()).disposeExpenses(100D).createdBy(user).withProductCode("#s2gx").build();

    when(brainA1Stub.brianSisAddCredit(any(BrianSisAddCreditRequestDocument.class), isNull(EsbParam.class))).thenThrow(BwsErrMsg.class);
    brianDao.addCreditRecord(ticket);
  }

  private PhoneNumber createPhoneNumber() {
    PhoneNumber number = new PhoneNumber();
    number.setBanId("123456789");
    number.setCountryIdentificationNumber("+43");
    number.setCityIdentificationNumber("732");
    number.setSubscriberNumber("2222");
    return number;
  }

}
