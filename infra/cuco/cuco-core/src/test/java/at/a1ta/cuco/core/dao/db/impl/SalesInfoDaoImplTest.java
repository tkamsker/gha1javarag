package at.a1ta.cuco.core.dao.db.impl;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

import org.junit.Assert;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import at.a1ta.cuco.core.shared.dto.salesinfo.SbsNoteReportRow;

@Ignore
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:testApplicationContext-cuco-core.xml"})
public class SalesInfoDaoImplTest {

  SimpleDateFormat sdf = new SimpleDateFormat("dd.MM.yyyy");

  @Autowired
  SalesInfoDaoImpl salesInfoDaoImpl;

  @Test
  public void testAll() throws Exception {

    Date begin = sdf.parse("01.01.2013");
    Date end = sdf.parse("01.01.2015");

    List<SbsNoteReportRow> reportData = salesInfoDaoImpl.getSbsNoteReportData(begin, end);
    Assert.assertNotNull(reportData);
    System.out.println(reportData.toString());
  }

}
