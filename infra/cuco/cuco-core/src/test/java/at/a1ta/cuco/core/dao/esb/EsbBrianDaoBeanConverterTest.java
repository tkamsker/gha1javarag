package at.a1ta.cuco.core.dao.esb;

import java.text.SimpleDateFormat;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.dao.esb.BrianDaoImpl.PayableTicket2AddCreditRequestConverter;
import at.a1ta.cuco.core.shared.dto.PayableTicket;
import at.a1ta.cuco.core.shared.dto.PhoneNumber;
import at.mobilkom.brian.wsdl.BrianSisAddCreditRequest;

public class EsbBrianDaoBeanConverterTest {

  private PayableTicket2AddCreditRequestConverter converter;

  @Before
  public void setUp() {
    converter = PayableTicket2AddCreditRequestConverter.INSTANCE;
  }

  @Test
  public void testConverterReturnsEmptyAddCreditRequestWhenCalledWithNull() {
    Assert.assertNotNull(converter.convert(null));
  }

  @Test
  public void testConverterConvertsPayableTicketCorrectly() {
    BiteUser user = new BiteUser();
    user.setUsername("q907291");
    PayableTicket ticket = PayableTicket.builder().forPhoneNumber(createPhoneNumber("123456789")).disposeExpenses(100D).withProductCode("#s2gx").createdBy(user).build();
    ticket.setId(987654321L);

    BrianSisAddCreditRequest request = converter.convert(ticket);
    Assert.assertEquals("BCRD", request.getAdcrdCmd().getActivityCode());
    Assert.assertEquals(100D, request.getAdcrdCmd().getAmount(), 0.0F);
    Assert.assertEquals("123456789", request.getAdcrdCmd().getBan());
    Assert.assertEquals("#s2gx", request.getAdcrdCmd().getChargeCode());
    Assert.assertEquals(new SimpleDateFormat("yyyy/MM/dd").format(ticket.getCreateDate()), request.getAdcrdCmd().getEffectDate());
    Assert.assertEquals("PAST: 987654321 (q907291)", request.getAdcrdCmd().getMemo());
    Assert.assertEquals("+437322222", request.getAdcrdCmd().getMsisdn());
    Assert.assertTrue(request.getAdcrdCmd().getNextBill());
    Assert.assertEquals("q907291", request.getAdcrdCmd().getUid());

    Assert.assertNull(request.getAdcrdCmd().getBen());
    Assert.assertNull(request.getAdcrdCmd().getBillAddComments());
    Assert.assertNull(request.getAdcrdCmd().getBillComment());
    Assert.assertNull(request.getAdcrdCmd().getSoc());
  }

  @Test
  public void testNumberConversionPositiveNoScale() {
    Assert.assertEquals(100D, converter.formatDouble(100D), 0.0F);
    Assert.assertEquals(-100D, converter.formatDouble(-100D), 0.0F);
  }

  @Test
  public void testNumberConversionNegativeNoScale() {
    Assert.assertEquals(-100D, converter.formatDouble(-100D), 0.0F);
  }

  @Test
  public void testNumberConversionWithScale2MustRemainUntouched() {
    Assert.assertEquals(100.56D, converter.formatDouble(100.56D), 0.0F);
  }

  @Test
  public void testNumberConversionWithScale3MustBeRoundedUpAndScaledTo2Digits() {
    Assert.assertEquals(100.57D, converter.formatDouble(100.56912544D), 0.0F);
  }

  @Test
  public void testNumberConversionWithScale3MustBeRoundedDownAndScaledTo2Digits() {
    Assert.assertEquals(100.56D, converter.formatDouble(100.56412544D), 0.0F);
  }

  private PhoneNumber createPhoneNumber(String ban) {
    PhoneNumber number = new PhoneNumber();
    number.setBanId(ban);
    number.setCountryIdentificationNumber("+43");
    number.setCityIdentificationNumber("732");
    number.setSubscriberNumber("2222");
    return number;
  }
}
