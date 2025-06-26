package at.a1ta.cuco.core.service.visitreport;

import java.math.BigDecimal;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.service.TextService;
import at.a1ta.bite.core.shared.dto.Text;
import at.a1ta.cuco.core.service.util.ReportUtil;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.DigitalSellingNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.InternetSpeed;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.InternetSpeedNew;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.InternetSpeedOld;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.MobilePhoneNew;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.MobilePhoneOld;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.MobileTariffNew;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.MobileTariffOld;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.Music;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.PaymentNew;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.PaymentOld;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.SecurityNew;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.SecurityOld;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.ServicesNew;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.ServicesOld;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.SmartHomeNew;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.SmartHomeOld;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.TVNew;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.TVOld;
import net.sf.jasperreports.engine.JRException;
import net.sf.jasperreports.engine.JasperPrint;

@Service
public class VisitReportPrintService {

  private static final NumberFormat numberFormat = new DecimalFormat("#0.00");

  private TextService textService;

  public JasperPrint generateDigitalSellingNoteReport(final DigitalSellingNote note, final String nameOfUser) throws JRException {
    String jrxml = "at/a1ta/cuco/core/service/visitreport/digitalSellingNote.jrxml";
    Map<String, Object> params = createParamsForReport(nameOfUser, getText("si_vi_ds_summary_table_title_sum_old"), getText("si_vi_ds_summary_table_title_sum_new"), note.getComment());

    ArrayList<DigitalSellingNotePrintModel> data = generateModel(note);
    return ReportUtil.createReport(jrxml, data, params);
  }

  private ArrayList<DigitalSellingNotePrintModel> generateModel(DigitalSellingNote note) {
    ArrayList<DigitalSellingNotePrintModel> list = new ArrayList<DigitalSellingNotePrintModel>();

    InternetSpeed internetSpeed = note.getInternetSpeed();
    InternetSpeedOld isOld = internetSpeed.getInternetSpeedOld();
    InternetSpeedNew isNew = internetSpeed.getInternetSpeedNew();
    if (shouldShow(isOld.getSum(), isOld.getComment(), isNew.getSum(), isNew.getComment())) {
      list.add(getPrintModel("si_vi_ds_internet_speed_title", isOld.getSum(), isOld.getComment(), isNew.getSum(), isNew.getComment()));
    }

    TVOld tvOld = note.getTv().getTvOld();
    TVNew tvNew = note.getTv().getTvNew();
    if (shouldShow(tvOld.getSum(), tvOld.getComment(), tvNew.getSum(), tvNew.getComment())) {
      list.add(getPrintModel("si_vi_ds_tv_title", tvOld.getSum(), tvOld.getComment(), tvNew.getSum(), tvNew.getComment()));
    }

    MobilePhoneOld mpOld = note.getMobilePhone().getMobilePhoneOld();
    MobilePhoneNew mpNew = note.getMobilePhone().getMobilePhoneNew();
    if (shouldShow(mpOld.getSum(), mpOld.getComment(), mpNew.getSum(), mpNew.getComment())) {
      list.add(getPrintModel("si_vi_ds_mobile_phone_title", mpOld.getSum(), mpOld.getComment(), mpNew.getSum(), mpNew.getComment()));
    }

    MobileTariffOld mtOld = note.getMobileTariff().getMobileTariffOld();
    MobileTariffNew mtNew = note.getMobileTariff().getMobileTariffNew();
    if (shouldShow(mtOld.getSum(), mtOld.getComment(), mtNew.getSum(), mtNew.getComment())) {
      list.add(getPrintModel("si_vi_ds_mobile_tariff_title", mtOld.getSum(), mtOld.getComment(), mtNew.getSum(), mtNew.getComment()));
    }

    Music music = note.getMusic();
    if (shouldShow(music.getSum(), music.getCommentOld(), null, music.getCommentNew())) {
      list.add(getPrintModel("si_vi_ds_music_title", music.getSum(), music.getCommentOld(), null, music.getCommentNew()));
    }

    SecurityOld secOld = note.getSecurity().getSecurityOld();
    SecurityNew secNew = note.getSecurity().getSecurityNew();
    if (shouldShow(secOld.getSum(), secOld.getComment(), secNew.getSum(), secNew.getComment())) {
      list.add(getPrintModel("si_vi_ds_security_title", secOld.getSum(), secOld.getComment(), secNew.getSum(), secNew.getComment()));
    }

    SmartHomeOld smOld = note.getSmartHome().getSmartHomeOld();
    SmartHomeNew smNew = note.getSmartHome().getSmartHomeNew();
    if (shouldShow(smOld.getSum(), smOld.getComment(), smNew.getSum(), smNew.getComment())) {
      list.add(getPrintModel("si_vi_ds_smart_home_title", smOld.getSum(), smOld.getComment(), smNew.getSum(), smNew.getComment()));
    }

    PaymentOld payOld = note.getPayment().getPaymentOld();
    PaymentNew payNew = note.getPayment().getPaymentNew();
    if (shouldShow(payOld.getSum(), payOld.getComment(), payNew.getSum(), payNew.getComment())) {
      list.add(getPrintModel("si_vi_ds_payment_title", payOld.getSum(), payOld.getComment(), payNew.getSum(), payNew.getComment()));
    }

    ServicesOld svOld = note.getServices().getServicesOld();
    ServicesNew svNew = note.getServices().getServicesNew();
    if (shouldShow(svOld.getSum(), svOld.getComment(), svNew.getSum(), svNew.getComment())) {
      list.add(getPrintModel("si_vi_ds_services_title", svOld.getSum(), svOld.getComment(), svNew.getSum(), svNew.getComment()));
    }

    list.add(getPrintModel("si_vi_ds_summary_total_sum", note.getSumOld(), null, note.getSumNew(), null));

    return list;
  }

  private boolean shouldShow(BigDecimal priceOld, String noteOld, BigDecimal priceNew, String noteNew) {
    if (hasPrice(priceOld) || hasNote(noteOld) || hasPrice(priceNew) || hasNote(noteNew)) {
      return true;
    }
    return false;
  }

  private boolean hasPrice(BigDecimal price) {
    return price != null && price.compareTo(BigDecimal.ZERO) != 0;
  }

  private boolean hasNote(String note) {
    return note != null && !note.trim().isEmpty();
  }

  private DigitalSellingNotePrintModel getPrintModel(String textKey, BigDecimal priceOld, String noteOld, BigDecimal priceNew, String noteNew) {
    String title = getText(textKey);
    return new DigitalSellingNotePrintModel(title, formatPrice(priceOld), noteOld, formatPrice(priceNew), noteNew);
  }

  private String getText(String textKey) {
    Text text = textService.getByKey(textKey);
    if (text == null) {
      return textKey;
    }
    return text.getText();
  }

  private Map<String, Object> createParamsForReport(final String nameOfUser, final String colOldHeader, final String colNewHeader, String comment) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("nameOfUser", nameOfUser);
    params.put("templateFile", "at/a1ta/cuco/core/service/visitreport/styles.jrtx");
    params.put("bgLogo", "at/a1ta/cuco/core/service/visitreport/a1_piano.png");
    params.put("colOldHeader", colOldHeader);
    params.put("colNewHeader", colNewHeader);
    params.put("comment", comment);
    return params;
  }

  @Autowired
  public void setTextService(TextService textService) {
    this.textService = textService;
  }

  public static String formatPrice(BigDecimal price) {
    if (price == null) {
      return "";
    }
    return "€ " + numberFormat.format(price);
  }
}
