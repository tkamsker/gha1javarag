package at.a1ta.cuco.core.service.impl;

import org.junit.Assert;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import at.a1ta.cuco.core.service.AutoVvlService;
import at.a1ta.cuco.core.shared.dto.product.AutoVvlInfo;
import at.a1ta.cuco.core.shared.dto.product.CallNumber;

@Ignore
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:testApplicationContext-cuco-core.xml"})
public class IAutoVvlServiceImplTest {

  @Autowired
  AutoVvlService autoVvlService;

  @Test
  public void testBan() {
    AutoVvlInfo autoVvlInfo = autoVvlService.getAutoVvlInfoByBan("1");
    Assert.assertNotNull(autoVvlInfo);
    // TODO extend asserts
  }

  @Test
  public void testCallnumber() {
    CallNumber callNumber = new CallNumber();
    callNumber.setCountryCode("0");
    callNumber.setOnkz("0");
    callNumber.setTnum("2");

    AutoVvlInfo autoVvlInfo = autoVvlService.getAutoVvlInfoByCallNumber(callNumber);
    Assert.assertNotNull(autoVvlInfo);
    Assert.assertNotNull(autoVvlInfo.getAutoVvlStatus());
    Assert.assertNotNull(autoVvlInfo.getAutoExtendedCommitmentActPeriodStartTime());
    Assert.assertNotNull(autoVvlInfo.getAutoExtendedCommitmentActPeriodEndTime());
    Assert.assertNotNull(autoVvlInfo.getAutoExtendedCommitmentNextPeriodStartTime());
    Assert.assertNotNull(autoVvlInfo.getLatestCommitmentEndDate());
  }

}
