package at.a1ta.cuco.core.shared.dto.salesinfo;

public class SimpleNote extends SalesInfoNote {

  /**
   * Copy Constructor
   * 
   * @param simpleNote a <code>SimpleNote</code> object
   */
  public SimpleNote(SimpleNote simpleNote) {
    super(simpleNote);
  }
  
  public SimpleNote() {
    super();
  }

  @Override
  public String toString() {
    return "SimpleNote [super.toString()=" + super.toString() + "]";
  }

}
