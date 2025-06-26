package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.db.ContactPersonDao;
import at.a1ta.cuco.core.dao.db.PartyDao;
import at.a1ta.cuco.core.service.ContactPersonService;
import at.a1ta.cuco.core.shared.dto.ContactPerson;
import at.a1ta.cuco.core.shared.dto.Party;

@Service
public class ContactPersonServiceImpl implements ContactPersonService {

  private ContactPersonDao contactPersonDao;
  private PartyDao partyDao;

  @Override
  public List<ContactPerson> listContactPersons(List<Long> partyIds) {
    List<ContactPerson> result = new ArrayList<ContactPerson>();
    result.addAll(contactPersonDao.listContactPersonsInclLocalContacts(partyIds));
    result.addAll(extractContactPersons(partyDao.loadParties(partyIds)));
    return result;
  }

  @Override
  public List<ContactPerson> listContactPersonsIncludingDeleted(List<Long> partyIds) {
    List<ContactPerson> result = new ArrayList<ContactPerson>();
    result.addAll(contactPersonDao.listContactPersonsInclLocalContactsAndDeletedContacts(partyIds));
    result.addAll(extractContactPersons(partyDao.loadParties(partyIds)));
    return result;
  }

  private List<ContactPerson> extractContactPersons(List<Party> parties) {
    List<ContactPerson> result = new ArrayList<ContactPerson>();

    for (Party party : parties) {
      boolean containsName = party.getContactPersonLastName() != null && party.getContactPersonFirstName() != null;
      boolean containsMail = party.getEMailAddress() != null;
      boolean hasPhoneOrFaxNumber = party.getContactPhoneNumber1() != null || party.getContactPhoneNumber2() != null || party.getFaxNumber() != null;

      boolean displayContact = containsName && (containsMail || hasPhoneOrFaxNumber);

      if (!displayContact) {
        continue;
      }
      ContactPerson person = extractContactPerson(party);

      result.add(person);
    }

    return result;
  }

  private ContactPerson extractContactPerson(Party party) {
    ContactPerson result = new ContactPerson();

    result.setCustomerId(party.getId());
    result.setSalutation(party.getContactPersonSalutation());
    result.setTitle(party.getContactPersonTitle());
    result.setFirstname(party.getContactPersonFirstName());
    result.setLastname(party.getContactPersonLastName());
    result.setBirthdate(party.getContactPersonBirthdate());
    result.setAddressLine1(party.getAddressLine1());
    result.setAddressLine2(party.getAddressLine2());
    result.setMail(party.getEMailAddress());
    result.setMobilephoneNumber(party.getMobilePhoneNumber());
    result.setFaxNumber(party.getFaxNumber());
    result.setDayPhoneNumber(party.getContactPhoneNumber1());
    result.setNightPhoneNumber(party.getContactPhoneNumber2());
    result.setActive(true);
    result.setDeleted(0);
    result.setSource("KUMS");

    return result;
  }

  @Autowired
  public void setPartyDao(@Qualifier("cucoCustomerDao") PartyDao partyDao) {
    this.partyDao = partyDao;
  }

  @Autowired
  public ContactPersonServiceImpl(ContactPersonDao contactPersonDao) {
    this.contactPersonDao = contactPersonDao;
  }

  @Override
  public void insertLocalContact(ContactPerson contact) {
    this.contactPersonDao.insertLocalContact(contact);

  }

  @Override
  public void updateLocalContact(ContactPerson contact) {
    this.contactPersonDao.updateLocalContact(contact);

  }

  @Override
  public void updateLocalContactStatus(ContactPerson contact) {
    this.contactPersonDao.updateLocalContactStatus(contact);
  }

  @Override
  public void updateDWHContactStatus(ContactPerson contact) {
    this.contactPersonDao.updateDWHContactStatus(contact);
  }

  @Override
  public void deleteLocalContact(ContactPerson contact) {
    this.contactPersonDao.deleteLocalContact(contact);
  }

  @Override
  public void markLocalContactDeleted(ContactPerson contact) {
    this.contactPersonDao.markLocalContactDeleted(contact);
  }

  @Override
  public Boolean checkIfReferenceExists(Long partyId, Long id) {
    return this.contactPersonDao.checkIfReferenceExists(partyId, id);
  }

}
