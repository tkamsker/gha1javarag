/*
 * Copyright 2009 - 2012 by A1 Telekom Austria AG
 * All Rights Reserved.
 * 
 * The Software is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * All information contained herein is, and remains the property of
 * A1 Telekom Austria AG and its suppliers, if any.
 * The intellectual and technical concepts contained herein are proprietary
 * to A1 Telekom Austria AG and its suppliers and may be covered by
 * intertional or national patents, patents in process, and are protected
 * by trade secret or copyright law. Dissemination of this information or
 * reproduction of this material is strictly forbidden unless prior written
 * permission is obtained from A1 Telekom Austria AG.
 */
package at.a1ta.cuco.core.service.impl;

import junit.framework.Assert;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.cuco.core.shared.dto.GamificationResponse;

@RunWith(MockitoJUnitRunner.class)
public class GamificationHttpServiceImplTest {

  private static final String[] AREA_CODES = {"732", "0732", "664", "0664", "699", "0699"};

  private GamificationHttpServiceImpl service;

  @Before
  public void setUp() {
    this.service = new GamificationHttpServiceImpl();
  }

  @Test
  public void testFilterNoUnknownAreaCodes() {
    // TODO
    // String input =
    // "{\"data\": {\"cucoMessages\": {\"agentId\": \"1\",\"messages\":    [            {         \"messageUid\": \"d3dcab1f-2591-41ab-9dfe-9e812150011b\",         \"timestamp\": \"1502705968714\",         \"title\": \"Seamless multimedia analyzer\",         \"message\": \"Accusamus ad et eligendi voluptatibus in.\",         \"type\": \"battle\",         \"url\": \"http://www.google.at\"      },            {         \"messageUid\": \"6dad222d-6d19-4eb2-ad14-5f1b1bcd91c3\",         \"timestamp\": \"1502705968715\",         \"title\": \"User-centric bi-directional ability\",         \"message\": \"Illum fugiat sunt laudantium qui quia.\",         \"type\": \"battle\",         \"url\": \"http://www.google.at\"      }   ]}}}";
    GamificationResponse result = new GamificationResponse();
    Assert.assertNotNull(result);
  }

}
