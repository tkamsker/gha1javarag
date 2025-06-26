package at.a1ta.cuco.core.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.dao.SettingDao;
import at.a1ta.cuco.core.dao.db.VbmProductsDao;
import at.a1ta.cuco.core.service.VBMProductsService;
import at.a1ta.cuco.core.shared.dto.nbo.VBMDeclineReason;
import at.a1ta.cuco.core.shared.dto.nbo.VBMProduct;

@Service
public class VBMProductsServiceImpl implements VBMProductsService {
  @Autowired
  private VbmProductsDao vBMProductsDao;

  @Autowired
  private SettingDao settingsDao;

  @Override
  public List<VBMProduct> listVBMProduct(long customerId, String productName, String monthYearPeriod, Integer scoringTotal, int maxResults) {

    return this.vBMProductsDao.listVBMProduct(
        customerId,
        productName,
        monthYearPeriod,
        settingsDao.getSettingOrNull("vbm.scoring.threshold") != null ? Integer.valueOf(settingsDao.getSettingOrNull(
            "vbm.scoring.threshold").getValue()) : 50, maxResults);
  }

  @Override
  public void registerCustomerResponse(VBMDeclineReason declineReason, VBMProduct vbmProduct, String username, String userID) {
    vBMProductsDao.registerCustomerResponse(declineReason, vbmProduct, username, userID);

  }

}
