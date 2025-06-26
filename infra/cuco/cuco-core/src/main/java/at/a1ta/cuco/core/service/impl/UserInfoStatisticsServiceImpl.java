package at.a1ta.cuco.core.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.db.UserInfoStatisticsDao;
import at.a1ta.cuco.core.service.UserInfoStatisticsService;
import at.a1ta.cuco.core.shared.dto.UserInfoStatistics;

@Service
public class UserInfoStatisticsServiceImpl implements UserInfoStatisticsService {

  private UserInfoStatisticsDao userInfoStatisticsDao;

  @Override
  public UserInfoStatistics getUserInfoStatistics(String uUser) {
    return userInfoStatisticsDao.getUserInfoStatistics(uUser);
  }

  @Autowired
  public void setUserInfoStatisticsDao(UserInfoStatisticsDao userInfoStatisticsDao) {
    this.userInfoStatisticsDao = userInfoStatisticsDao;
  }

}
