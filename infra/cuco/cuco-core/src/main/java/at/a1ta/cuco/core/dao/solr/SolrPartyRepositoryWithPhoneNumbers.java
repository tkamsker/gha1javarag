package at.a1ta.cuco.core.dao.solr;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;

import at.a1ta.bite.data.solr.core.query.Query;
import at.a1ta.cuco.core.dao.db.PhoneNumberDao;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PartySearch;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;

public class SolrPartyRepositoryWithPhoneNumbers extends SolrPartyRepository {

  static final int MAX_LOOP = 3;

  private PhoneNumberDao phoneNumberDao;

  @Override
  public Page<Party> search(PartySearch customerSearch, Pageable pageable) {
    if (customerSearch.getPhoneNumber() != null) {
      final PhoneNumberStructure phoneNumberStructure = parsePhoneNumber(customerSearch);

      if (phoneNumberStructure == null) {
        return new PageImpl<Party>(Collections.<Party> emptyList());
      }

      customerSearch.setLkz(phoneNumberStructure.getCountryCode());
      customerSearch.setOkz(phoneNumberStructure.getOnkz());
      customerSearch.setCallNumber(phoneNumberStructure.getNumber());
    }

    Query query = SolrPartyQueryHelper.convertToQuery(customerSearch);
    query.setPageRequest(pageable);
    // grouping takes a lot of time => filter result in code (10 times faster)
    // query.addGroupByField(SolrPartyQuery.SearchField.CUSTOMERNUMBER);
    return rippleLoad(query, pageable);
  }

  private PhoneNumberStructure parsePhoneNumber(PartySearch partySearch) {
    return phoneNumberDao.parse(partySearch.getPhoneNumber());
  }

  private Page<Party> rippleLoad(Query query, Pageable pageable) {
    Page<Party> page = getSolrTemplate().executeListQuery(query, Party.class);
    List<Party> result = removeDuplicates(page.getContent());

    if (page.getTotalElements() > pageable.getPageSize()) {
      int loopCount = 0;
      int initialPageNumber = pageable.getPageNumber();
      while (result.size() < page.getSize() && ++loopCount < MAX_LOOP) {
        query.setPageRequest(new PageRequest(initialPageNumber + loopCount, pageable.getPageSize()));
        result.addAll(getSolrTemplate().executeListQuery(query, Party.class).getContent());
        result = removeDuplicates(result);
      }
    }
    if (!result.isEmpty() && result.size() > pageable.getPageSize()) {
      result = result.subList(0, pageable.getPageSize());
    }
    return new PageImpl<Party>(result, query.getPageRequest(), page.getTotalElements());
  }

  List<Party> removeDuplicates(List<Party> parties) {
    return new ArrayList<Party>(new HashSet<Party>(parties));
  }

  @Autowired
  public void setPhoneNumberDao(PhoneNumberDao phoneNumberDao) {
    this.phoneNumberDao = phoneNumberDao;
  }

}
