package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.SingleTurnaroundDao;
import at.a1ta.cuco.core.shared.dto.SingleTurnaround;

public class SingleTurnaroundDaoImpl extends AbstractDao implements SingleTurnaroundDao {

  @Override
  public List<SingleTurnaround> getSingleTurnaroundsForCustomerAndProdgrp(long customerId, long prodgrpId) {
    HashMap<String, Long> params = new HashMap<String, Long>();
    params.put("customerId", customerId);
    params.put("prodgrpId", prodgrpId);

    return performListQuery("SingleTurnaround.getSingleTurnaroundsforProdGrp", params);
  }

}
