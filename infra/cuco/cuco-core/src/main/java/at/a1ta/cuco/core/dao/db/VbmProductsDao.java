package at.a1ta.cuco.core.dao.db;

import java.util.List;

import at.a1ta.cuco.core.shared.dto.nbo.VBMDeclineReason;
import at.a1ta.cuco.core.shared.dto.nbo.VBMProduct;
import at.a1ta.cuco.core.shared.dto.nbo.VBMProductDetails;

public interface VbmProductsDao {
  List<VBMProduct> listVBMProduct(Long customerId, String productName, String monthYearPeriod, Integer scoringTotal, int maxResults);

  List<VBMProductDetails> listAllVBMProductDetails();

  void registerCustomerResponse(VBMDeclineReason declineReason, VBMProduct vbmProduct, String username, String userId);

}
