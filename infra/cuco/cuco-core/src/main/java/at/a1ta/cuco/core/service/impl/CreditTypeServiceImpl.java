package at.a1ta.cuco.core.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.db.CreditTypeDao;
import at.a1ta.cuco.core.service.CreditTypeService;
import at.a1ta.cuco.core.shared.dto.CreditType;

@Service
public class CreditTypeServiceImpl implements CreditTypeService {

  private CreditTypeDao creditTypeDao;

  @Override
  public void deleteCreditType(Long id) {
    creditTypeDao.deleteCreditType(id);
  }

  @Override
  public List<CreditType> getAllCreditTypes() {
    return creditTypeDao.getAllCreditTypes();
  }

  @Override
  public CreditType getCreditTypeById(Long id) {
    return creditTypeDao.getCreditTypeById(id);
  }

  @Override
  public void saveCreditType(CreditType ct) {
    if (ct.getId() == null) {
      creditTypeDao.insertCreditType(ct);
    } else {
      creditTypeDao.updateCreditType(ct);
    }
  }

  @Autowired
  public void setCreditTypeDao(CreditTypeDao creditTypeDao) {
    this.creditTypeDao = creditTypeDao;
  }
}
