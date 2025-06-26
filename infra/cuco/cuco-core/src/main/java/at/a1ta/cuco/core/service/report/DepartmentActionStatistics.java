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
import java.util.LinkedHashSet;
import java.util.Set;

import at.a1ta.bite.core.server.dto.DepartmentActionRecord;

public class DepartmentActionStatistics extends ActionStatisticBase<DepartmentActionRecord> {

  private Set<String> departments = new LinkedHashSet<String>();

  public DepartmentActionStatistics(Collection<DepartmentActionRecord> data) {
    super(data);
  }

  @Override
  String createKey(DepartmentActionRecord record) {
    captureDepartment(record.getDepartment());
    return record.getDepartment() + "#" + record.getAction();
  }

  private void captureDepartment(String department) {
    if (!departments.contains(department)) {
      departments.add(department);
    }
  }

  public Set<String> getDepartments() {
    return Collections.unmodifiableSet(this.departments);
  }

}
