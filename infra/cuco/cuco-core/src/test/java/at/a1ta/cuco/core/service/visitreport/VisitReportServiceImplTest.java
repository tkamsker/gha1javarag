package at.a1ta.cuco.core.service.visitreport;

import static org.junit.Assert.assertNotNull;

import java.math.BigDecimal;

import org.junit.Before;
import org.junit.Test;

import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.DigitalSellingNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.InternetSpeedType;

public class VisitReportServiceImplTest {

  private VisitReportServiceImpl service;

  @Before
  public void beforeTest() {
    service = new VisitReportServiceImpl();
  }

  @Test
  public void testMarshalling() {
    DigitalSellingNote note = new DigitalSellingNote();
    note.getHousehold().setFloor(12);
    note.getInternetSpeed().getInternetSpeedOld().setInternetSpeedType(InternetSpeedType.MBIT_150);
    note.getInternetSpeed().getInternetSpeedNew().setA1CyberProtectionPrice(new BigDecimal(150));
    String result = service.marshalDigitalSellingNote(note);
    assertNotNull(result);
  }
}
