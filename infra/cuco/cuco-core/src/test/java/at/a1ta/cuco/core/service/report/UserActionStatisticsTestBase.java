package at.a1ta.cuco.core.service.report;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.URISyntaxException;
import java.text.DateFormat;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import org.apache.commons.io.FileUtils;
import org.springframework.util.ResourceUtils;
import org.springframework.util.StringUtils;

import at.a1ta.bite.core.server.dto.UserActionRecord;

public abstract class UserActionStatisticsTestBase {

  protected final String ACTION = "LOAD_CUSTO";

  protected List<UserActionRecord> generate(List<String> lines) {
    List<UserActionRecord> records = new ArrayList<UserActionRecord>(lines.size());
    for (String line : lines) {
      UserActionRecord record = createActionRecordFromDataLine(line);
      records.add(record);
    }
    return records;
  }

  protected UserActionRecord createActionRecordFromDataLine(String line) {
    String[] data = StringUtils.commaDelimitedListToStringArray(line);
    UserActionRecord record = new UserActionRecord();
    record.setLogin(data[0]);
    record.setAction(data[1]);
    try {
      DateFormat df = DateFormat.getDateInstance(DateFormat.SHORT, Locale.GERMAN);
      record.setDate(df.parse(data[2]));
    } catch (ParseException e) {
      throw new IllegalArgumentException(e);
    }
    record.setActionCount(Long.valueOf(data[3]));
    return record;
  }

  protected List<UserActionRecord> readRecordsFromFile(String name) {
    try {
      List<String> lines = FileUtils.readLines(new File(ResourceUtils.toURI(this.getClass().getResource(name))));
      return generate(lines);
    } catch (FileNotFoundException e) {
      throw new RuntimeException(e);
    } catch (IOException e) {
      throw new RuntimeException(e);
    } catch (URISyntaxException e) {
      throw new RuntimeException(e);
    }
  }
}
