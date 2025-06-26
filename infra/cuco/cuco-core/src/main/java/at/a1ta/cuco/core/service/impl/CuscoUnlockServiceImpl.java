package at.a1ta.cuco.core.service.impl;

import java.io.StringWriter;
import java.net.MalformedURLException;
import java.net.URL;
import java.rmi.RemoteException;
import java.util.HashMap;
import java.util.Map;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.apache.commons.codec.binary.Base64;
import org.apache.commons.lang.StringUtils;
import org.apache.commons.lang.time.FastDateFormat;
import org.apache.xmlbeans.XmlException;
import org.apache.xmlbeans.XmlObject;
import org.joda.time.DateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.util.Assert;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Text;

import com.telekomaustriagroup.esb.cusco.CuscoError;
import com.telekomaustriagroup.esb.cusco.CuscoStub;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.bite.data.cusco.CusCoConfigurtationBean;
import at.a1ta.bite.data.cusco.CusCoMessage;
import at.a1ta.bite.data.cusco.CusCoMessageBuilder;
import at.a1ta.cuco.core.dao.cusco.CusCoResponse;
import at.a1ta.cuco.core.service.CuscoUnlockService;
import at.a1ta.cuco.core.shared.dto.Customer;
import at.mobilkom.crm.cusco.CheckStatusForSignedRequestDocument;
import at.mobilkom.crm.cusco.CheckStatusForSignedRequestType;
import at.mobilkom.crm.cusco.CheckStatusForSignedResponseDocument;
import at.mobilkom.crm.cusco.CheckStatusForSignedResponseType;
import at.mobilkom.crm.cusco.NewJobType.VariableData;
import at.mobilkom.crm.cusco.PrepareForSignRequestDocument;
import at.mobilkom.crm.cusco.PrepareForSignRequestType;
import at.mobilkom.crm.cusco.PrepareForSignResponseDocument;

@Service
public class CuscoUnlockServiceImpl extends BaseEsbClient<CuscoStub> implements CuscoUnlockService {

  private static final Logger LOGGER = LoggerFactory.getLogger(CuscoUnlockServiceImpl.class);

  private static final String OP_PREPARE_FOR_SIGN = "PrepareForSign";
  private static final String OP_CHECK_STATUS_FOR_SIGNED = "CheckStatusForSigned";

  private static final String SOURCE_SYSTEM_CUCO = "CuCo";
  private static final String DUMMY_PSWD = "no-password";

  private static final FastDateFormat DATEFORMAT = FastDateFormat.getInstance("dd.MM.yyyy");

  @Override
  public CusCoResponse prepareForSign(Customer customer, UserInfo userInfo, String contactPerson, String templateId) {
    final CusCoMessage message = getCuscoMessageBuilder().createForOperation(OP_PREPARE_FOR_SIGN);
    message.setTemplateId(templateId);
    message.setOutputChannel("Brief");
    message.setStatusReportId("12354");

    PrepareForSignRequestDocument requestDoc = PrepareForSignRequestDocument.Factory.newInstance();
    PrepareForSignRequestType request = requestDoc.addNewPrepareForSignRequest();
    request.setJobId(message.getJobId());
    request.setPassword(message.getPassword());
    request.setSendingSystem(message.getSourceSystem());
    request.setTemplateId(templateId);
    request.setOutputChannel(message.getOutputChannel());
    request.setInteractionId("");

    appendMessageData(customer, userInfo, contactPerson, request);

    PrepareForSignResponseDocument response;
    try {
      response = stub.prepareForSign(requestDoc, null);
    } catch (RemoteException | CuscoError e) {
      LOGGER.error("Error while preparing for sign", e);
      CusCoResponse cuscoResponse = new CusCoResponse();
      cuscoResponse.setJobId(message.getJobId());
      cuscoResponse.setStatus("500");
      return cuscoResponse;
    }
    CusCoResponse cuscoResponse = new CusCoResponse();
    cuscoResponse.setJobId(message.getJobId());
    cuscoResponse.setStatus("200");

    String responseDocStr = response.getPrepareForSignResponse().getDocument();
    byte[] responseDoc = responseDocStr.getBytes();
    cuscoResponse.setRawData(Base64.decodeBase64(responseDoc));
    return cuscoResponse;
  }

  private CusCoMessageBuilder getCuscoMessageBuilder() {
    CusCoConfigurtationBean configBean = new CusCoConfigurtationBean(SOURCE_SYSTEM_CUCO, DUMMY_PSWD);
    return new CusCoMessageBuilder(configBean);
  }

  void appendMessageData(Customer customer, UserInfo userInfo, String contactPerson, PrepareForSignRequestType request) {
    Assert.notNull(customer);
    Assert.notNull(userInfo);

    Map<String, String> parameterMap = getRequestParameters(customer, userInfo, contactPerson);

    DocumentBuilderFactory dbfac = DocumentBuilderFactory.newInstance();
    DocumentBuilder docBuilder = null;
    Document doc = null;
    try {
      docBuilder = dbfac.newDocumentBuilder();
      doc = docBuilder.newDocument();

      URL namespaceURL = new URL("http://crm.mobilkom.at/cusco");
      Element documentNode = doc.createElementNS(namespaceURL.toString(), "Document");
      doc.appendChild(documentNode);
      for (Map.Entry<String, String> entry : parameterMap.entrySet()) {
        if (entry.getKey() != null && entry.getValue() != null) {
          addChildTextNodeToParent(entry.getKey(), entry.getValue(), documentNode, doc);
        }
      }

      String xmlData = domToString(doc);
      XmlObject document = XmlObject.Factory.parse(xmlData);

      VariableData data = request.addNewVariableData();
      data.set(document);
    } catch (XmlException | ParserConfigurationException | TransformerException | MalformedURLException e) {
      LOGGER.error("Error while converting string to xml", e);
    }
  }

  private Map<String, String> getRequestParameters(Customer customer, UserInfo userInfo, String contactPerson) {
    Map<String, String> parameterMap = new HashMap<String, String>();
    parameterMap.put("PartyId", Long.toString(customer.getId()));
    parameterMap.put("PartyBirthdate", customer.getBirthdate() != null ? DATEFORMAT.format(customer.getBirthdate()) : "");
    if (StringUtils.equalsIgnoreCase("Firma", customer.getSalutation())) {
      parameterMap.put("CustomerIsCompany", Boolean.toString(true));
      parameterMap.put("ContractCompNumber", customer.getCommercialRegisterNumber());
    } else {
      parameterMap.put("CustomerIsCompany", Boolean.toString(false));
    }
    parameterMap.put("ContractTitle", customer.getTitle());
    parameterMap.put("ContractSalutation", customer.getSalutation());
    parameterMap.put("ContractFirstName", customer.getFirstname());
    parameterMap.put("ContractLastName", customer.getLastname());
    parameterMap.put("ContractStreet", customer.getStreet());
    parameterMap.put("ContractHousenr", customer.getHousenumber());
    parameterMap.put("ContractCountry", customer.getCountry());
    parameterMap.put("ContractZipCode", customer.getPoBox());
    parameterMap.put("ContractCity", customer.getCity());
    parameterMap.put("DealerId", userInfo.getUsername());
    parameterMap.put("DealerSalesPerson", userInfo.getName());
    parameterMap.put("ContactPersonFullName", contactPerson);
    parameterMap.put("ContractLastChangeStr", DateTime.now().toString("dd.MM.yyyy"));
    parameterMap.put("DealerCity", userInfo.getBiteUser().getManagementLevel1OrgUnitDescription());
    return parameterMap;
  }

  private void addChildTextNodeToParent(String childTag, String childText, Element parent, Document doc) {
    Element node = doc.createElement(childTag);
    Text text = doc.createTextNode(childText);
    node.appendChild(text);
    parent.appendChild(node);
  }

  private String domToString(Document doc) throws TransformerException {
    String ret = null;

    TransformerFactory transfac = TransformerFactory.newInstance();
    Transformer trans = transfac.newTransformer();
    trans.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
    trans.setOutputProperty(OutputKeys.INDENT, "yes");

    StringWriter sw = new StringWriter();
    StreamResult result = new StreamResult(sw);
    DOMSource source = new DOMSource(doc);
    trans.transform(source, result);
    ret = sw.toString();

    return ret;
  }

  @Override
  public CusCoResponse checkStatusForSigned(String jobId) {
    Assert.hasText(jobId);
    CusCoMessage message = getCuscoMessageBuilder().createForOperation(OP_CHECK_STATUS_FOR_SIGNED, jobId);

    CheckStatusForSignedRequestDocument requestDoc = CheckStatusForSignedRequestDocument.Factory.newInstance();
    CheckStatusForSignedRequestType request = requestDoc.addNewCheckStatusForSignedRequest();
    request.setJobId(message.getJobId());
    request.setPassword(message.getPassword());
    request.setSendingSystem(message.getSourceSystem());

    CheckStatusForSignedResponseDocument response;
    try {
      response = stub.checkStatusForSigned(requestDoc, null);
    } catch (RemoteException | CuscoError e) {
      LOGGER.error("Error while checking status for signed", e);
      CusCoResponse cuscoResponse = new CusCoResponse();
      cuscoResponse.setJobId(message.getJobId());
      cuscoResponse.setStatus("500");
      return cuscoResponse;
    }
    CusCoResponse cuscoResponse = new CusCoResponse();
    cuscoResponse.setJobId(message.getJobId());

    CheckStatusForSignedResponseType responseType = response.getCheckStatusForSignedResponse();
    cuscoResponse.setStatus(responseType.getStatus());
    return cuscoResponse;
  }

}
