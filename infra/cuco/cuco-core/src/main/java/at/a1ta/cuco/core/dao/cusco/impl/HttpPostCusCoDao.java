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

import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.commons.lang.StringUtils;
import org.apache.commons.lang.time.FastDateFormat;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.ParseException;
import org.apache.http.util.EntityUtils;
import org.joda.time.DateTime;
import org.springframework.beans.factory.InitializingBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataRetrievalFailureException;
import org.springframework.jdbc.datasource.lookup.DataSourceLookupFailureException;
import org.springframework.stereotype.Repository;
import org.springframework.util.Assert;

import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.bite.data.cusco.CusCoConfigurtationBean;
import at.a1ta.bite.data.cusco.CusCoMessage;
import at.a1ta.bite.data.cusco.CusCoMessageBuilder;
import at.a1ta.bite.data.cusco.http.CusCoHttpOperations;
import at.a1ta.bite.data.cusco.http.ResponseMapper;
import at.a1ta.cuco.core.dao.cusco.CusCoDao;
import at.a1ta.cuco.core.dao.cusco.CusCoResponse;
import at.a1ta.cuco.core.shared.dto.Customer;

/**
 * provide access to cusco via http
 * <strong>error case</error>
 * 
 * <pre>
 * <Error>
 *   <Number>8017</Number>
 *   <Message>
 *     Error message Text
 *   </Message>
 * </Error>
 * </pre>
 */
@Repository
public class HttpPostCusCoDao implements CusCoDao, InitializingBean {

  private static final String OP_PREPARE_FOR_SIGN = "PrepareForSign";
  private static final String OP_CHECK_STATUS_FOR_SIGNED = "CheckStatusForSigned";
  private static final Pattern XML_STATUS_PATTERN = Pattern.compile("<Status>(.+?)</Status>");
  private static final Pattern XML_ERROR_PATTERN = Pattern.compile("<Error>(.+?)</Error>");
  private static final FastDateFormat DATEFORMAT = FastDateFormat.getInstance("dd.MM.yyyy");

  private CusCoHttpOperations operations;
  private CusCoConfigurtationBean config;
  private String endpoint;

  public HttpPostCusCoDao() {

  }

  @Override
  public CusCoResponse prepareForSign(Customer customer, UserInfo userInfo, String contactPerson, String templateId) {
    final CusCoMessage message = new CusCoMessageBuilder(config).createForOperation(OP_PREPARE_FOR_SIGN);
    message.setTemplateId(templateId);
    message.setOutputChannel("Brief");
    message.setStatusReportId("12354");

    appendMessageData(customer, userInfo, contactPerson, message);

    CusCoResponse response = operations.sendMessage(message, getEndpoint() + "/" + OP_PREPARE_FOR_SIGN, new ResponseMapper<CusCoResponse>() {

      @Override
      public CusCoResponse createResponse(HttpResponse httpResponse) {
        HttpEntity entity = httpResponse.getEntity();
        assertHttpStatusCode(httpResponse, 200);
        assertMimeType(httpResponse, "application/pdf");

        CusCoResponse response = new CusCoResponse();
        response.setJobId(message.getJobId());
        response.setStatus(Integer.toString(httpResponse.getStatusLine().getStatusCode()));
        try {
          response.setRawData(EntityUtils.toByteArray(entity));
        } catch (IOException e) {
          throw new DataRetrievalFailureException("Cannot read http response", e);
        }

        return response;
      }

    });

    return response;
  }

  void appendMessageData(Customer customer, UserInfo userInfo, String contactPerson, CusCoMessage message) {
    Assert.notNull(customer);
    Assert.notNull(userInfo);

    message.put("PartyId", Long.toString(customer.getId()));
    message.put("PartyBirthdate", customer.getBirthdate() != null ? DATEFORMAT.format(customer.getBirthdate()) : "");
    if (StringUtils.equalsIgnoreCase("Firma", customer.getSalutation())) {
      message.put("CustomerIsCompany", Boolean.toString(true));
      message.put("ContractCompNumber", customer.getCommercialRegisterNumber());
    } else {
      message.put("CustomerIsCompany", Boolean.toString(false));
    }
    message.put("ContractTitle", customer.getTitle());
    message.put("ContractSalutation", customer.getSalutation());
    message.put("ContractFirstName", customer.getFirstname());
    message.put("ContractLastName", customer.getLastname());
    message.put("ContractStreet", customer.getStreet());
    message.put("ContractHousenr", customer.getHousenumber());
    message.put("ContractCountry", customer.getCountry());
    message.put("ContractZipCode", customer.getPoBox());
    message.put("ContractCity", customer.getCity());
    message.put("DealerId", userInfo.getUsername());
    message.put("DealerSalesPerson", userInfo.getName());
    message.put("ContactPersonFullName", contactPerson);
    message.put("ContractLastChangeStr", DateTime.now().toString("dd.MM.yyyy"));
    message.put("DealerCity", userInfo.getBiteUser().getManagementLevel1OrgUnitDescription());
  }

  private void assertNonErrorResponse(String rawData) {
    final Matcher matcher = XML_ERROR_PATTERN.matcher(rawData);
    if (matcher.find()) {
      throw new DataRetrievalFailureException(matcher.group(1));
    }
  }

  /**
   * @see at.a1ta.cuco.core.dao.cusco.CusCoDao#checkStatusForSigned(java.lang.String)
   *      parses the http response of the returned entity
   * 
   *      <pre>
   *  <StatusForSigned>
   *    <Status>Unknown</Status>
   *    <StatusId>0</StatusId>
   *  </StatusForSigned>
   * </pre>
   */
  @Override
  public CusCoResponse checkStatusForSigned(String jobId) {
    Assert.hasText(jobId);
    CusCoMessage message = new CusCoMessageBuilder(config).createForOperation(OP_CHECK_STATUS_FOR_SIGNED, jobId);
    String url = getEndpoint() + "/" + OP_CHECK_STATUS_FOR_SIGNED;
    CusCoResponse response = operations.sendMessage(message, url, new ResponseMapper<CusCoResponse>() {

      @Override
      public CusCoResponse createResponse(HttpResponse httpResponse) {
        HttpEntity entity = httpResponse.getEntity();
        assertHttpStatusCode(httpResponse, 200);
        assertMimeType(httpResponse, "text/xml");

        CusCoResponse response = new CusCoResponse();

        try {
          String rawData = EntityUtils.toString(entity);
          assertNonErrorResponse(rawData);
          final Matcher matcher = XML_STATUS_PATTERN.matcher(rawData);
          matcher.find();
          response.setStatus(matcher.group(1));
        } catch (ParseException e) {
          throw new DataRetrievalFailureException("Cannot parse http response", e);
        } catch (IOException e) {
          throw new DataRetrievalFailureException("Cannot read http response", e);
        }

        return response;
      }

    });

    return response;
  }

  private void assertMimeType(HttpResponse httpResponse, String mimeType) {
    HttpEntity entity = httpResponse.getEntity();
    if (entity != null) {
      if (!StringUtils.startsWithIgnoreCase(entity.getContentType().getValue(), mimeType)) {
        EntityUtils.consumeQuietly(entity);
        throw new DataRetrievalFailureException("Expected MIME Type '" + mimeType + "' but was " + httpResponse.getEntity().getContentType().getValue());
      }
    }
  }

  private void assertHttpStatusCode(HttpResponse httpResponse, int statusCode) {
    if (httpResponse.getStatusLine().getStatusCode() != statusCode) {
      HttpEntity entity = httpResponse.getEntity();
      if (entity != null) {
        String message = "";
        try {
          message = EntityUtils.toString(entity);
        } catch (ParseException e) {
          throw new DataSourceLookupFailureException(e.getMessage(), e);
        } catch (IOException e) {
          throw new DataSourceLookupFailureException(e.getMessage(), e);
        }
        throw new DataSourceLookupFailureException("Unable to connect to cusco service. Returned HTTP-" + httpResponse.getStatusLine().getStatusCode() + "\r\n" + message);
      }
    }
  }

  @Override
  public CusCoHttpOperations getOperations() {
    return this.operations;
  }

  @Autowired
  public void setOperations(CusCoHttpOperations operations) {
    this.operations = operations;
  }

  @Autowired(required = false)
  public void setConfig(CusCoConfigurtationBean config) {
    this.config = config;
  }

  @Override
  public void afterPropertiesSet() throws Exception {
    if (config == null) {
      this.config = new CusCoConfigurtationBean("Test", "test");
    }
  }

  public void setEndpoint(String endpoint) {
    this.endpoint = endpoint;
  }

  public String getEndpoint() {
    return endpoint;
  }

}
