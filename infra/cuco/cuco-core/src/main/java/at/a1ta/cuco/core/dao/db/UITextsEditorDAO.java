package at.a1ta.cuco.core.dao.db;

import java.util.List;

import at.a1ta.cuco.core.shared.dto.UIText;

public interface UITextsEditorDAO {
  
  List<UIText> getUITexts();
  void updateUIText(UIText text);
  List<UIText> searchText(String value);
  
}