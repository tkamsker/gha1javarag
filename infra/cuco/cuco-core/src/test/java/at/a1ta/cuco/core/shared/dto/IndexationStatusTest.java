package at.a1ta.cuco.core.shared.dto;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class IndexationStatusTest {

  @Before
  public void setUp() throws Exception {}

  @Test
  public void testGetForDWHValue_Indexed() {
    Assert.assertEquals(IndexationStatus.INDEXED, IndexationStatus.getForDWHValue("INDEXED_PRODUCTS"));
  }

  @Test
  public void testGetForDWHValue_NotIndexed() {
    Assert.assertEquals(IndexationStatus.NOT_INDEXED, IndexationStatus.getForDWHValue("EXCLUDED"));
  }

  @Test
  public void testGetForDWHValue_IndexedNotUsed() {
    Assert.assertEquals(IndexationStatus.INDEXED_NOT_STARTED, IndexationStatus.getForDWHValue("INDEXED_PRODUCTS_NOT_USED"));
  }

  @Test
  public void testGetForDWHValue_Null() {
    Assert.assertEquals(IndexationStatus.NOT_AVAILABLE, IndexationStatus.getForDWHValue(null));
  }

  @Test
  public void testGetForDWHValue_EmptyString() {
    Assert.assertEquals(IndexationStatus.NOT_AVAILABLE, IndexationStatus.getForDWHValue(""));
  }

  @Test
  public void testGetForDWHValue_InvalidString() {
    Assert.assertEquals(IndexationStatus.NOT_AVAILABLE, IndexationStatus.getForDWHValue("test"));
  }

  @Test
  public void testGetForCIValue_Indexed() {
    Assert.assertEquals(IndexationStatus.INDEXED, IndexationStatus.getForCIValue(2));
  }

  @Test
  public void testGetForCIValue_NotIndexed() {
    Assert.assertEquals(IndexationStatus.NOT_INDEXED, IndexationStatus.getForCIValue(3));
  }

  @Test
  public void testGetForCIValue_IndexedNotUsed() {
    Assert.assertEquals(IndexationStatus.INDEXED_NOT_STARTED, IndexationStatus.getForCIValue(1));
  }

  @Test
  public void testGetForCIValue_Zero() {
    Assert.assertEquals(IndexationStatus.NOT_AVAILABLE, IndexationStatus.getForCIValue(0));
  }

  @Test
  public void testGetForCIValue_Negative() {
    Assert.assertEquals(IndexationStatus.NOT_AVAILABLE, IndexationStatus.getForCIValue(-1));
  }

  @Test
  public void testGetForCIValue_InvalidNumber() {
    Assert.assertEquals(IndexationStatus.NOT_AVAILABLE, IndexationStatus.getForCIValue(99999));
  }

}
