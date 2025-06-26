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
package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.commons.collections.CollectionUtils;
import org.apache.commons.collections.Predicate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.db.UnknownAreaCodeDao;
import at.a1ta.cuco.core.service.UnknownAreaCodeService;
import at.a1ta.cuco.core.shared.dto.PhoneNumber;
import at.a1ta.cuco.core.shared.dto.UnknownAreaCode;

@Service
public class UnknownAreaCodeServiceImpl implements UnknownAreaCodeService {

  private UnknownAreaCodeDao unknownAreaCodeDao;

  @Override
  public void deleteUnknownAreaCode(Long id) {
    unknownAreaCodeDao.deleteUnknownAreaCode(id);
  }

  @Override
  public List<UnknownAreaCode> getAllUnknownAreaCodes() {
    return unknownAreaCodeDao.getAllUnknownAreaCodes();
  }

  @Override
  public UnknownAreaCode getUnknownAreaCodeById(Long id) {
    return unknownAreaCodeDao.getUnknownAreaCodeById(id);
  }

  @Override
  public void saveUnknownAreaCode(UnknownAreaCode ct) {
    if (ct.getId() == null) {
      unknownAreaCodeDao.insertUnknownAreaCode(ct);
    } else {
      unknownAreaCodeDao.updateUnknownAreaCode(ct);
    }
  }

  @Autowired
  public void setUnknownAreaCodeDao(UnknownAreaCodeDao unknownAreaCodeDao) {
    this.unknownAreaCodeDao = unknownAreaCodeDao;
  }

  @SuppressWarnings({"unchecked", "rawtypes"})
  @Override
  public List<PhoneNumber> filterPhoneNumbersWithUnknownAreaCode(Collection<PhoneNumber> phoneNumbers) {
    final List<UnknownAreaCode> unknownCodes = getAllUnknownAreaCodes();
    if (unknownCodes.isEmpty()) {
      return new ArrayList<PhoneNumber>(phoneNumbers);
    }
    final Pattern pattern = createUnknownNumberFilterPattern(unknownCodes);

    return new ArrayList(CollectionUtils.select(phoneNumbers, new Predicate() {
      @Override
      public boolean evaluate(Object input) {
        if (input instanceof PhoneNumber) {
          PhoneNumber number = (PhoneNumber) input;
          Matcher x = pattern.matcher(number.getCityIdentificationNumber());
          return !x.matches();
        }
        return false;
      }
    }));

  }

  private Pattern createUnknownNumberFilterPattern(Collection<UnknownAreaCode> excludes) {
    StringBuilder sb = new StringBuilder();
    for (UnknownAreaCode code : excludes) {
      String areaCode = code.getAreaCode();

      if (areaCode != null && areaCode.startsWith("0")) {
        areaCode = code.getAreaCode().replaceFirst("0", "");
      }
      sb.append("[0]?");
      sb.append(areaCode);
      sb.append("|");
    }
    if (sb.indexOf("|") > 0) {
      sb.deleteCharAt(sb.lastIndexOf("|"));
    }
    return Pattern.compile(sb.toString());
  }
}
