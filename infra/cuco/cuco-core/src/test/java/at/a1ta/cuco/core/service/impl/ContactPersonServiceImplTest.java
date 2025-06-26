package at.a1ta.cuco.core.service.impl;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Matchers;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.core.server.dao.SettingDao;
import at.a1ta.bite.core.shared.dto.Setting;
import at.a1ta.cuco.core.dao.db.ContactPersonDao;
import at.a1ta.cuco.core.dao.db.PartyDao;
import at.a1ta.cuco.core.shared.dto.ContactPerson;
import at.a1ta.cuco.core.shared.dto.Party;

@RunWith(MockitoJUnitRunner.class)
public class ContactPersonServiceImplTest {

  private ContactPersonServiceImpl service;

  @Mock
  private ContactPersonDao contactPersonDaoMock;
  @Mock
  private PartyDao partyDaoMock;

  @Mock
  private SettingDao settingDaoMock;

  @Before
  public void setUp() {
    service = new ContactPersonServiceImpl(contactPersonDaoMock);
    service.setPartyDao(partyDaoMock);
    Setting nullSetting = new Setting();

    Setting setting = new Setting();
    String settingValue = "Test";
    setting.setValue(settingValue);
    when(settingDaoMock.getSetting(Matchers.anyString())).thenReturn(setting);
    when(settingDaoMock.getSetting("sbs.productTabChanges.active")).thenReturn(nullSetting);
  }

  @Test
  public void testListContactPersonsEmpty() {
    List<ContactPerson> persons = service.listContactPersons(makeIdsList());
    Mockito.verify(contactPersonDaoMock).listContactPersonsInclLocalContacts(Matchers.anyListOf(Long.class));
    Mockito.verify(partyDaoMock).loadParties(Matchers.anyListOf(Long.class));
    assertNotNull(persons);
    assertEquals(0, persons.size());
  }

  @Test
  public void testListContactPersonsFromContacts() {
    Long contactId = Long.valueOf("123");

    List<ContactPerson> contacts = makeContactList(contactId);
    Mockito.when(contactPersonDaoMock.listContactPersonsInclLocalContacts(Matchers.anyListOf(Long.class))).thenReturn(contacts);
    List<ContactPerson> persons = service.listContactPersons(makeIdsList());

    assertEquals(1, persons.size());
    assertEquals(contactId, persons.get(0).getCustomerId());
  }

  @Test
  public void testListContactPersonsFromPartiesNothingFound() {
    // won't be converted to ContactPerson as it doesnt't have name, email or phone number
    List<Party> partyList = makePartyList(345, null, null, null, null);
    Mockito.when(partyDaoMock.loadParties(Matchers.anyListOf(Long.class))).thenReturn(partyList);

    List<ContactPerson> persons = service.listContactPersons(makeIdsList());
    assertEquals(0, persons.size());
  }

  @Test
  public void testListContactPersonsFromPartiesSomethingFound() {
    // will be converted to ContactPerson
    List<Party> partyList = makePartyList(345, "Nick", "Bonkers", "aaa@bbb.at", null);
    Mockito.when(partyDaoMock.loadParties(Matchers.anyListOf(Long.class))).thenReturn(partyList);

    List<ContactPerson> persons = service.listContactPersons(makeIdsList());
    assertEquals(1, persons.size());
  }

  @Test
  public void testListContactPersonsFromPartiesWithoutEmailAndPhone() {
    // won't be converted to ContactPerson as it doesnt't have neither email nor phone number
    List<Party> partyList = makePartyList(345, "Nick", "Bonkers", null, null);
    Mockito.when(partyDaoMock.loadParties(Matchers.anyListOf(Long.class))).thenReturn(partyList);

    List<ContactPerson> persons = service.listContactPersons(makeIdsList());
    assertEquals(0, persons.size());
  }

  @Test
  public void testListContactPersonsFromPartiesWithoutName() {
    // won't be converted to ContactPerson as it doesnt't have first name
    List<Party> partyList = makePartyList(345, null, "Bonkers", "aaa@bbb.at", "+43566789");
    Mockito.when(partyDaoMock.loadParties(Matchers.anyListOf(Long.class))).thenReturn(partyList);

    List<ContactPerson> persons = service.listContactPersons(makeIdsList());
    assertEquals(0, persons.size());
  }

  /**
   * @return an arraylist with one Party object (id=123)
   */
  private List<Party> makePartyList(long id, String firstName, String lastName, String email, String phoneNumber) {
    List<Party> parties = new ArrayList<Party>();
    Party party = new Party(id);
    parties.add(party);
    party.setContactPersonFirstName(firstName);
    party.setContactPersonLastName(lastName);
    party.setEMailAddress(email);
    party.setContactPhoneNumber1(phoneNumber);
    return parties;
  }

  private List<ContactPerson> makeContactList(Long id) {
    List<ContactPerson> contacts = new ArrayList<ContactPerson>();
    ContactPerson contact = new ContactPerson();
    contact.setCustomerId(id);
    contacts.add(contact);
    return contacts;
  }

  private List<Long> makeIdsList() {
    return Arrays.asList(Long.valueOf(123), Long.valueOf(456));
  }

}
