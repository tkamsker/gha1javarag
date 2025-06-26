package at.a1ta.cuco.core.dao.esb;

import java.util.ArrayList;

import at.a1ta.cuco.core.shared.dto.PointOfSaleInfo;

public interface KUMSCommonDao {

  public ArrayList<PointOfSaleInfo> loadAvailablePOSList();

}
