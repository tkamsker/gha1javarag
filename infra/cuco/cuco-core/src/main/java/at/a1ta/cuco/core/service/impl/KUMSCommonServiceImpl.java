package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.cuco.core.dao.db.ImageSizeDao;
import at.a1ta.cuco.core.dao.esb.KUMSCommonDao;
import at.a1ta.cuco.core.service.KUMSCommonService;
import at.a1ta.cuco.core.shared.dto.PointOfSaleInfo;

import com.telekomaustriagroup.esb.kumscommon.KUMSCommonStub;

@Service
public class KUMSCommonServiceImpl extends BaseEsbClient<KUMSCommonStub> implements KUMSCommonService {
  
  private static final Logger LOGGER = LoggerFactory.getLogger(KUMSCommonServiceImpl.class);
  
  @Autowired
  private KUMSCommonDao kumsCommonDao;

  @Override
  public ArrayList<PointOfSaleInfo> loadAvailablePOSList() {
    return kumsCommonDao.loadAvailablePOSList();
  }
  
}
