package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;
import java.util.ArrayList;

public interface Node extends Serializable {

  public String getText();

  public String getId();

  public void setId(String id);

  public BaseNode getParent();

  public void setParent(BaseNode parent);

  public ArrayList<BaseNode> getChildren();

  public void setChildren(ArrayList<BaseNode> children);

  public void addChild(BaseNode child);

  public boolean hasParent();

  public boolean hasChildren();

  public MetaData getMetaData();

  public void setMetaData(MetaData metaData);

}