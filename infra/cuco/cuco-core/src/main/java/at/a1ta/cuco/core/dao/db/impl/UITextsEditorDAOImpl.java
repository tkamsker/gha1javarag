package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.UITextsEditorDAO;
import at.a1ta.cuco.core.shared.dto.UIText;

public class UITextsEditorDAOImpl extends AbstractDao implements UITextsEditorDAO {

  @Override
  public List<UIText> getUITexts() {
    return performListQuery("TextsEditor.getUITexts");
  }

  @Override
  public void updateUIText(UIText text) {
    executeUpdate("TextsEditor.updateUIText", text);
  }
  
  @Override
  public List<UIText> searchText(String value) {
    return performListQuery("TextsEditor.searchText", value);
  }

}
