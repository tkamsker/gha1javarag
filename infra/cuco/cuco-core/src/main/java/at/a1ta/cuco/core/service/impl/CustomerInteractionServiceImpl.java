package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import org.apache.commons.lang.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.data.clarify.dao.ClarifyInteractionAndWorkflowDao;
import at.a1ta.bite.data.clarify.shared.dto.ClarifyCustomerInteractionResponse;
import at.a1ta.bite.data.clarify.shared.dto.CustomerInteraction;
import at.a1ta.cuco.core.dao.db.MKInteractionDao;
import at.a1ta.cuco.core.service.CustomerInteractionService;

@Service
public class CustomerInteractionServiceImpl implements CustomerInteractionService {

  private static final String MK_SITE_INDICATOR = "MK";

  private ClarifyInteractionAndWorkflowDao clarifyInteractionAndWorkflowDao;

  private MKInteractionDao mkInteractionDao;

  @Override
  public ClarifyCustomerInteractionResponse listInteractions(long customerId, String siteId) {
    return clarifyInteractionAndWorkflowDao.getClarifyInteractionsViaSite(customerId, siteId);
  }

  @Override
  public List<CustomerInteraction> listMKInteractions(long customerId) {
    return mkInteractionDao.listMKInteractions(customerId);
  }

  @Override
  public List<CustomerInteraction> listAllInteractions(long customerId, String siteId, boolean addMKInteractions) {
    List<CustomerInteraction> interactions = new ArrayList<CustomerInteraction>();
    if (!StringUtils.startsWith(siteId, MK_SITE_INDICATOR)) {
      interactions.addAll(listInteractions(customerId, siteId).getInteractions());
    }
    if (addMKInteractions) {
      interactions.addAll(listMKInteractions(customerId));
    }
    Collections.sort(interactions, new Comparator<CustomerInteraction>() {

      @Override
      public int compare(CustomerInteraction i1, CustomerInteraction i2) {
        if (i1.getStartDate() == null && i2.getStartDate() == null) {
          return 0;
        }
        if (i1.getStartDate() == null) {
          return 1;
        }
        if (i2.getStartDate() == null) {
          return -1;
        }
        return -i1.getStartDate().compareTo(i2.getStartDate());
      }
    });
    return interactions;
  }

  @Autowired
  public void setClarifyInteractionAndWorkflowDao(ClarifyInteractionAndWorkflowDao clarifyInteractionAndWorkflowDao) {
    this.clarifyInteractionAndWorkflowDao = clarifyInteractionAndWorkflowDao;
  }

  @Autowired
  public void setMkInteractionDao(MKInteractionDao mkInteractionDao) {
    this.mkInteractionDao = mkInteractionDao;
  }

}
