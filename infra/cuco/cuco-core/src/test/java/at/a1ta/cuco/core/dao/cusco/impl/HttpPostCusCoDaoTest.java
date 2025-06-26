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
package at.a1ta.cuco.core.dao.cusco.impl;

import static org.junit.Assert.*;

import org.joda.time.DateTime;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.bite.data.cusco.CusCoConfigurtationBean;
import at.a1ta.bite.data.cusco.CusCoMessage;
import at.a1ta.bite.data.cusco.CusCoMessageBuilder;
import at.a1ta.bite.data.cusco.http.CusCoHttpOperations;
import at.a1ta.cuco.core.shared.dto.Customer;

@RunWith(MockitoJUnitRunner.class)
public class HttpPostCusCoDaoTest {

  private static final byte[] PDF_RAW_DATA = "0000062268 00000 n 0000062387 00000 n trailer<</Size 27/Info 4 0 R/Root 1 0 R/ID[<291E31B2DA429A5F86CB347D3E3598F6><291E31B2DA429A5F86CB347D3E3598F6>]>>startxref63374%%EOF".getBytes();
  private static final String SOURCE_SYSTEM = "source";
  private static final String PASSWORD = "password";
  private static final String JOB_ID = "job-1";

  private static final CusCoConfigurtationBean CONFIG = new CusCoConfigurtationBean(SOURCE_SYSTEM, PASSWORD);

  @Mock
  private CusCoHttpOperations operationsMock;

  private HttpPostCusCoDao cuscoDao;

  @Before
  public void setUp() {
    cuscoDao = new HttpPostCusCoDao();
    cuscoDao.setOperations(operationsMock);
    cuscoDao.setConfig(CONFIG);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testCheckStatusForSignedWithNullValue() {
    cuscoDao.checkStatusForSigned(null);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testCheckStatusForSignedEmptyStringValue() {
    cuscoDao.checkStatusForSigned("");
  }

  @Test(expected = IllegalArgumentException.class)
  public void testPrepareForSignWihtNullCustomer() {
    cuscoDao.prepareForSign(null, new UserInfo(), null, null);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testPrepareForSignWihtNullUser() {
    cuscoDao.prepareForSign(new Customer(), null, null, null);
  }

  @Test
  public void testAppendMessageData() {
    CusCoMessage message = new CusCoMessageBuilder(new CusCoConfigurtationBean("test", "test")).createForOperation("PrepareForSign", "job-1");

    Customer customer = new Customer();
    customer.setId(12345);
    customer.setBirthdate(new DateTime(2012, 10, 11, 0, 0).toDate());
    customer.setTitle("Mag");
    customer.setSalutation("Herr");
    customer.setFirstname("Roland");
    customer.setLastname("Konrad Kobald");
    customer.setStreet("Lassallestrasse");
    customer.setHousenumber("9");
    customer.setCountry("A");
    customer.setPoBox("1020");
    customer.setCity("Wien");

    UserInfo userInfo = new UserInfo();
    userInfo.getBiteUser().setUsername("MKW8KT");
    userInfo.getBiteUser().setFirstName("Andreas");
    userInfo.getBiteUser().setLastName("Stollmayer");

    String contactPerson = "Dr. Klaus Hagenauer";

    cuscoDao.appendMessageData(customer, userInfo, contactPerson, message);

    assertEquals("12345", message.get("PartyId"));
    assertEquals("11.10.2012", message.get("PartyBirthdate"));
    assertEquals("false", message.get("CustomerIsCompany"));
    assertEquals("Mag", message.get("ContractTitle"));
    assertEquals("Herr", message.get("ContractSalutation"));
    assertEquals("Roland", message.get("ContractFirstName"));
    assertEquals("Konrad Kobald", message.get("ContractLastName"));
    assertEquals("Lassallestrasse", message.get("ContractStreet"));
    assertEquals("9", message.get("ContractHousenr"));
    assertEquals("A", message.get("ContractCountry"));
    assertEquals("1020", message.get("ContractZipCode"));
    assertEquals("Wien", message.get("ContractCity"));
    assertEquals("MKW8KT", message.get("DealerId"));
    assertEquals("Andreas Stollmayer", message.get("DealerSalesPerson"));
    assertEquals("Dr. Klaus Hagenauer", message.get("ContactPersonFullName"));
  }

  @Test
  public void testAppendMessageDataIsNotFirma() {
    CusCoMessage message = new CusCoMessageBuilder(new CusCoConfigurtationBean("test", "test")).createForOperation("PrepareForSign", "job-1");

    Customer customer = new Customer();
    UserInfo userInfo = new UserInfo();
    String contactPerson = "Test Contact Person";

    cuscoDao.appendMessageData(customer, userInfo, contactPerson, message);

    assertEquals("false", message.get("CustomerIsCompany"));
    assertEquals(null, message.get("ContractCompNumber"));
  }

  @Test
  public void testAppendMessageDataFirma() {
    CusCoMessage message = new CusCoMessageBuilder(new CusCoConfigurtationBean("test", "test")).createForOperation("PrepareForSign", "job-1");

    Customer customer = new Customer();
    customer.setSalutation("Firma");
    customer.setCommercialRegisterNumber("777");

    UserInfo userInfo = new UserInfo();
    String contactPerson = "Test Contact Person";

    cuscoDao.appendMessageData(customer, userInfo, contactPerson, message);

    assertEquals("true", message.get("CustomerIsCompany"));
    assertEquals("777", message.get("ContractCompNumber"));
  }

}
