package at.a1ta.cuco.core.dao.esb;

import java.math.BigDecimal;
import java.rmi.RemoteException;
import java.util.Date;

import org.joda.time.format.DateTimeFormat;
import org.joda.time.format.DateTimeFormatter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.convert.converter.Converter;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Repository;
import org.springframework.util.Assert;
import org.springframework.util.StringUtils;

import com.telekomaustriagroup.esb.briana1.BrianA1Stub;
import com.telekomaustriagroup.esb.briana1.BwsErrMsg;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.esb.EsbException;
import at.a1ta.cuco.core.shared.dto.PayableTicket;
import at.mobilkom.brian.wsdl.BrianSisAddCreditRequest;
import at.mobilkom.brian.wsdl.BrianSisAddCreditRequestDocument;
import at.mobilkom.brian.wsdl.BrianSisAddCreditResponseDocument;
import at.mobilkom.brian.wsdl.SisCreditRec;
import at.mobilkom.eai.esb.ValidationException;

/**
 * EsbBrainDao uses the {@link BrianA1Stub} to handle mobile billing affairs.
 * Domain types will be converted into according interface ones using {@link Converter}.
 */
@Component
@Repository
class BrianDaoImpl extends BaseEsbClient<BrianA1Stub> implements BrianDao {

  private static final Logger logger = LoggerFactory.getLogger(BrianDaoImpl.class);

  @Override
  public void addCreditRecord(PayableTicket ticket) {
    Assert.notNull(ticket, "Cannot process null as value for payable ticket");

    BrianSisAddCreditRequestDocument requestDocument = prepareAddCreditRequestDocument(ticket);

    sendAddCreditRequest(requestDocument);
  }

  private BrianSisAddCreditResponseDocument sendAddCreditRequest(BrianSisAddCreditRequestDocument requestDocument) {
    try {
      logger.debug("Sending BrianSisAddCreditRequest:\r\n" + requestDocument);
      return stub.brianSisAddCredit(requestDocument, null);
    } catch (RemoteException e) {
      throw new EsbException("BrianSisAddCreditRequest could not be sent", e);
    } catch (BwsErrMsg e) {
      String message = "BrianSisAddCreditRequest could not be processed.";
      if (e.getFaultMessage() != null && e.getFaultMessage().getReturnRec() != null) {
        message += ("\r\n" + e.getFaultMessage().getReturnRec().toString());
      }
      throw new EsbException(message, e);
    } catch (ValidationException e) {
      throw new EsbException("BrianSisAddCreditRequest could not be sent due to incompartible types.", e);
    }
  }

  private BrianSisAddCreditRequestDocument prepareAddCreditRequestDocument(PayableTicket ticket) {
    BrianSisAddCreditRequestDocument document = BrianSisAddCreditRequestDocument.Factory.newInstance();
    document.setBrianSisAddCreditRequest(PayableTicket2AddCreditRequestConverter.INSTANCE.convert(ticket));
    return document;
  }

  public enum PayableTicket2AddCreditRequestConverter implements Converter<PayableTicket, BrianSisAddCreditRequest> {

    INSTANCE;

    private static final int NUMBER_FORMAT_SCALE = 2;
    private static final String ACTIVITY_CODE = "BCRD";
    private static final String MEMO_PREFIX = "PAST: ";

    private static final DateTimeFormatter DATE_TIME_FORMATTER = DateTimeFormat.forPattern("yyyy/MM/dd");

    @Override
    public BrianSisAddCreditRequest convert(PayableTicket source) {
      if (source == null) {
        return BrianSisAddCreditRequest.Factory.newInstance();
      }

      BrianSisAddCreditRequest request = BrianSisAddCreditRequest.Factory.newInstance();

      SisCreditRec command = request.addNewAdcrdCmd();
      command.setActivityCode(ACTIVITY_CODE);
      command.setAmount(formatDouble(source.getCosts()));

      if (StringUtils.hasText(source.getBan())) {
        command.setBan(source.getBan());
      }

      command.setChargeCode(source.getService().getProductCode());
      command.setEffectDate(DATE_TIME_FORMATTER.print(source.getCreateDate() != null ? source.getCreateDate().getTime() : new Date().getTime()));
      command.setMemo(MEMO_PREFIX + source.getId() + " (" + source.getAgent().getUsername() + ")");
      command.setMsisdn((source.getLknz() == null ? "43" : source.getLknz()) + source.getOnkz() + source.getNumber());
      command.setNextBill(true);
      command.setUid(source.getAgent().getUsername());

      return request;
    }

    protected Double formatDouble(Double value) {
      BigDecimal bd = new BigDecimal(value);
      return bd.setScale(NUMBER_FORMAT_SCALE, BigDecimal.ROUND_HALF_UP).doubleValue();

    }
  }

}
