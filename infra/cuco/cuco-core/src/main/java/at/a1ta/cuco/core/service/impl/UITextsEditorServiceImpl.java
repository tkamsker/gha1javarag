package at.a1ta.cuco.core.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.db.UITextsEditorDAO;
import at.a1ta.cuco.core.service.UITextsEditorService;
import at.a1ta.cuco.core.shared.dto.UIText;

@Service
public class UITextsEditorServiceImpl implements UITextsEditorService {
  
  @Autowired
  private UITextsEditorDAO uiTextsEditorDAO;
  
  @Override
  public List<UIText> getUITexts() {
    return uiTextsEditorDAO.getUITexts();
  }

  @Override
  public void updateUIText(UIText text) {
    uiTextsEditorDAO.updateUIText(text);
  }
  
  @Override
  public List<UIText> searchText(String text) {
    return uiTextsEditorDAO.searchText(text);
  }

}
