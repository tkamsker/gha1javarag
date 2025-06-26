package at.a1ta.cuco.core.service;

import java.util.ArrayList;

import at.a1ta.cuco.core.shared.dto.product.CallNumber;
import at.a1ta.cuco.core.shared.dto.product.Promotion;

public interface PromotionService {

  ArrayList<Promotion> getSubscriptions(CallNumber callNumber);

}
