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
package at.a1ta.cuco.core.service.util;

import java.io.IOException;
import java.io.InputStream;
import java.util.Collection;
import java.util.Map;

import net.sf.jasperreports.engine.JRException;
import net.sf.jasperreports.engine.JasperCompileManager;
import net.sf.jasperreports.engine.JasperFillManager;
import net.sf.jasperreports.engine.JasperPrint;
import net.sf.jasperreports.engine.JasperReport;
import net.sf.jasperreports.engine.data.JRBeanCollectionDataSource;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public final class ReportUtil {

  private static final Logger logger = LoggerFactory.getLogger(ReportUtil.class);

  private ReportUtil() {}

  public static JasperPrint createReport(final String jrxml, @SuppressWarnings("rawtypes") final Collection beanCollection, final Map<String, Object> params) {
    InputStream inputStream = Thread.currentThread().getContextClassLoader().getResourceAsStream(jrxml);
    return createReport(inputStream, beanCollection, params);
  }

  public static JasperPrint createReport(final InputStream inputStream, @SuppressWarnings("rawtypes") final Collection beanCollection, final Map<String, Object> params) {
    try {
      JasperReport report = JasperCompileManager.compileReport(inputStream);
      return JasperFillManager.fillReport(report, params, new JRBeanCollectionDataSource(beanCollection));
    } catch (JRException e) {
      logger.error(e.getMessage(), e);
      throw new RuntimeException(e);
    } finally {
      try {
        inputStream.close();
      } catch (IOException e) {
        logger.error(e.getMessage(), e);
      }
    }
  }

  public static JasperReport createSubreport(String jrxml) {
    InputStream inputStream = Thread.currentThread().getContextClassLoader().getResourceAsStream(jrxml);
    try {
      return JasperCompileManager.compileReport(inputStream);
    } catch (JRException e) {
      logger.error(e.getMessage(), e);
      throw new RuntimeException(e);
    } finally {
      try {
        inputStream.close();
      } catch (IOException e) {
        logger.error(e.getMessage(), e);
      }
    }
  }

}
