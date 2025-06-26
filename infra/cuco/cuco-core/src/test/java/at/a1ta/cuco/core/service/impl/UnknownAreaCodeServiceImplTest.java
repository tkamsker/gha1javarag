/*
 * Copyright 2009 - 2012 by A1 Telekom Austria AG
 * All Rights Reserved.
 * 
 * The Software is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * All information contained herein is, and remains the property of
 * A1 Telekom Austria AG and its suppliers, if any.
 * The intellectual and technical concepts contained herein are proprietary
 * to A1 Telekom Austria AG and its suppliers and may be covered by
 * intertional or national patents, patents in process, and are protected
 * by trade secret or copyright law. Dissemination of this information or
 * reproduction of this material is strictly forbidden unless prior written
 * permission is obtained from A1 Telekom Austria AG.
 */
package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import junit.framework.Assert;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.cuco.core.dao.db.UnknownAreaCodeDao;
import at.a1ta.cuco.core.shared.dto.PhoneNumber;
import at.a1ta.cuco.core.shared.dto.UnknownAreaCode;

@RunWith(MockitoJUnitRunner.class)
public class UnknownAreaCodeServiceImplTest {

  private static final String[] AREA_CODES = {"732", "0732", "664", "0664", "699", "0699"};

  @Mock
  private UnknownAreaCodeDao unknownAreaCodeDaoMock;

  private UnknownAreaCodeServiceImpl service;

  @Before
  public void setUp() {
    this.service = new UnknownAreaCodeServiceImpl();
    service.setUnknownAreaCodeDao(unknownAreaCodeDaoMock);
  }

  @Test
  public void testFilterNoUnknownAreaCodes() {
    Mockito.when(unknownAreaCodeDaoMock.getAllUnknownAreaCodes()).thenReturn(Collections.<UnknownAreaCode> emptyList());
    List<PhoneNumber> result = service.filterPhoneNumbersWithUnknownAreaCode(initDefaultPhoneNumbers());
    Assert.assertEquals(6, result.size(), 0);
  }

  @Test
  public void testFilterAreaCodesWithoutLeadingZero() {
    initUnknownAreaCodes("699", "650");
    List<PhoneNumber> result = service.filterPhoneNumbersWithUnknownAreaCode(initDefaultPhoneNumbers());
    Assert.assertEquals(4, result.size(), 0);
    for (PhoneNumber number : result) {
      Assert.assertFalse(number.getCityIdentificationNumber().contains("699"));
      Assert.assertFalse(number.getCityIdentificationNumber().contains("650"));
    }
  }

  @Test
  public void testFilterAreaCodesWithLeadingZero() {
    initUnknownAreaCodes("0699", "0650");
    List<PhoneNumber> result = service.filterPhoneNumbersWithUnknownAreaCode(initDefaultPhoneNumbers());
    Assert.assertEquals(4, result.size(), 0);
    for (PhoneNumber number : result) {
      Assert.assertFalse(number.getCityIdentificationNumber().contains("699"));
      Assert.assertFalse(number.getCityIdentificationNumber().contains("650"));
    }
  }

  private List<PhoneNumber> initDefaultPhoneNumbers() {
    return initPhoneNumbers(AREA_CODES);
  }

  private List<PhoneNumber> initPhoneNumbers(String... strings) {
    List<PhoneNumber> numbers = new ArrayList<PhoneNumber>(strings.length);
    for (String s : strings) {
      PhoneNumber phoneNumber = new PhoneNumber();
      phoneNumber.setCityIdentificationNumber(s);
      numbers.add(phoneNumber);
    }
    return numbers;
  }

  private void initUnknownAreaCodes(String... strings) {
    List<UnknownAreaCode> codes = new ArrayList<UnknownAreaCode>(strings.length);
    for (String s : strings) {
      codes.add(new UnknownAreaCode(s, ""));
    }
    Mockito.when(unknownAreaCodeDaoMock.getAllUnknownAreaCodes()).thenReturn(codes);
  }

}
