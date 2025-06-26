package at.a1ta.cuco.core.dao.db.impl;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.dao.DuplicateKeyException;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.VbmProductsDao;
import at.a1ta.cuco.core.shared.dto.nbo.VBMDeclineReason;
import at.a1ta.cuco.core.shared.dto.nbo.VBMProduct;
import at.a1ta.cuco.core.shared.dto.nbo.VBMProductDetails;

public class VbmProductsDaoImpl extends AbstractDao implements VbmProductsDao {

  private static final String PARAM_CUSTOMER_ID = "customerId";
  private static final String PARAM_PRODUCT_NAME = "productName";
  private static final String PARAM_MONTH_YEAR_PERIOD = "monthYearPeriod";
  private static final String PARAM_SCORING_THRESHOLD = "scoreThreshold";
  private static final String QUERY_GET_VBM_PRODUCTS = "vbmProducts.listAvailableOffersForKunde";
  private static final String INSERT_REGISTER_FEEDBACK = "vbmProducts.registerFeedback";
  private static final String QUERY_GET_ALL_VBM_PRODUCTS_DETAILS = "vbmProducts.getProduktInfo";

  @Override
  public List<VBMProduct> listVBMProduct(Long customerId, String productName, String monthYearPeriod, Integer scoringTotal,
      final int maxResults) {
    final Map<String, Object> params = new HashMap<String, Object>(4);
    if (customerId != null) {
      params.put(PARAM_CUSTOMER_ID, customerId);
    }
    if (productName != null) {
      params.put(PARAM_PRODUCT_NAME, productName);
    }
    if (monthYearPeriod != null) {
      params.put(PARAM_MONTH_YEAR_PERIOD, monthYearPeriod);
    }
    if (scoringTotal != null) {
      params.put(PARAM_SCORING_THRESHOLD, scoringTotal);
    }
    return performListQuery(QUERY_GET_VBM_PRODUCTS, params, 0, maxResults);
  }

  @Override
  public List<VBMProductDetails> listAllVBMProductDetails() {
    List<VBMProductDetails> resultList = new ArrayList<VBMProductDetails>();
    List<VBMProductDetails> result = performListQuery(QUERY_GET_ALL_VBM_PRODUCTS_DETAILS, new HashMap<String, Object>());
    if (result != null) {
      resultList.addAll(result);
    }
    return resultList;
  }

  @Override
  public void registerCustomerResponse(VBMDeclineReason declineReason, VBMProduct vbmProduct, String username, String userId) {
    try {
      executeInsert(INSERT_REGISTER_FEEDBACK, vbmProduct.getProductFeedback());
    } catch (DuplicateKeyException ex) {
      // Do Nothing, Feedback is stored.
    }

  }

}
