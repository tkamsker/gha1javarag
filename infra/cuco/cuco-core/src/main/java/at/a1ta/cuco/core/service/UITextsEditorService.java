package at.a1ta.cuco.core.service;

import java.util.List;

import at.a1ta.cuco.core.shared.dto.UIText;

public interface UITextsEditorService {

  // select
  public List<UIText> getUITexts();
  
  // update
  public void updateUIText(UIText text);
  
  // search
  public List<UIText> searchText(String text);
  
}
