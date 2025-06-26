/*
 * Copyright 2009 - 2013 by A1 Telekom Austria AG
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
package at.a1ta.cuco.core.service.report;

import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

import org.hamcrest.collection.IsEmptyCollection;
import org.hamcrest.core.IsEqual;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import at.a1ta.bite.core.server.dto.DepartmentActionRecord;

public class DepartmentActionStatisticsTest {

  private DepartmentActionStatistics stats;

  @Before
  public void setUp() {
    stats = new DepartmentActionStatistics(generate());
  }

  @Test
  public void testCreateKeyCapturesDepartmentCorrectly() {
    stats.createKey(createActionRecord("action", 1L, "department"));

    Assert.assertThat(stats.getDepartments(), IsEqual.equalTo((Set<String>) new HashSet<String>() {
      {
        add("department");
      }
    }));
  }

  @Test
  public void testCreateKeyCapturesDepartmentOnlyOnceEvenIfAddedMultipleTimes() {
    stats.createKey(createActionRecord("action", 1L, "department"));
    stats.createKey(createActionRecord("action", 2L, "department"));
    stats.createKey(createActionRecord("action", 3L, "department"));

    Assert.assertThat(stats.getDepartments(), IsEqual.equalTo((Set<String>) new HashSet<String>() {
      {
        add("department");
      }
    }));
  }

  @Test
  public void testGetDepartmentsRetursEmptyListWhenNoDataAvailable() {
    Assert.assertThat(stats.getDepartments(), IsEmptyCollection.empty());
  }

  private DepartmentActionRecord createActionRecord(String action, Long actionCount, String department) {
    DepartmentActionRecord actionRecord = new DepartmentActionRecord();
    actionRecord.setAction(action);
    actionRecord.setActionCount(actionCount);
    actionRecord.setDepartment(department);
    return actionRecord;
  }

  private Collection<DepartmentActionRecord> generate() {
    return Collections.emptyList();
  }

}
