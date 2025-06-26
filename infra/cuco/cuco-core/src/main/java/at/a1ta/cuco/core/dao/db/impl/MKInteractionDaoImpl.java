package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.bite.data.clarify.shared.dto.CustomerInteraction;
import at.a1ta.cuco.core.dao.db.MKInteractionDao;

public class MKInteractionDaoImpl extends AbstractDao implements MKInteractionDao {

  @Override
  public List<CustomerInteraction> listMKInteractions(long customerId) {
    List<CustomerInteraction> interactions = performListQuery("MKInteraction.GetInteractionsByCustomerId", customerId);
    for (CustomerInteraction interaction : interactions) {
      interaction.setType("MK");
    }
    return interactions;
  }

}
