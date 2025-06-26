package at.a1ta.cuco.core.service;

import java.util.ArrayList;

import at.a1ta.cuco.core.shared.dto.PointOfSaleInfo;

public interface KUMSCommonService {

  /**
   * Get the full list of all POS<br />
   * 
   * @return empty list if no data found
   */
  public ArrayList<PointOfSaleInfo> loadAvailablePOSList();
  
}
