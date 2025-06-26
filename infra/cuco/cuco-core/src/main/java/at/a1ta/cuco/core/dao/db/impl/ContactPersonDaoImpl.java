package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.ContactPersonDao;
import at.a1ta.cuco.core.shared.dto.ContactPerson;

public class ContactPersonDaoImpl extends AbstractDao implements ContactPersonDao {

  @Override
  public List<ContactPerson> listContactPersons(List<Long> partyIds) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("partyIds", partyIds);
    return performListQuery("ContactPerson.GetContactPersons4Customer", params);
  }

  @Override
  public List<ContactPerson> listContactPersonsInclLocalContacts(List<Long> partyIds) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("partyIds", partyIds);
    return performListQuery("ContactPerson.GetAllContactPersons4Customers", params);
  }

  @Override
  public Boolean checkIfReferenceExists(Long partyId, Long id) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("partyId", partyId);
    params.put("id", id);
    int checkRef = ((Integer) performObjectQuery("ContactPerson.CheckReferenceInSBSNoteAndProductNote", params));
    return (checkRef == 1 ? true : false);
  
  }

  @Override
  public void insertLocalContact(ContactPerson contact) {
    executeInsert("ContactPerson.InsertLocalContact", contact);
  }

  @Override
  public void updateLocalContact(ContactPerson contact) {
    executeUpdate("ContactPerson.updateLocalContact", contact);

  }

  @Override
  public void updateLocalContactStatus(ContactPerson contact) {
    executeUpdate("ContactPerson.updateLocalContactPersonStatus", contact);
  }

  @Override
  public void updateDWHContactStatus(ContactPerson contact) {
    Integer count = performObjectQuery("ContactPerson.getDWHContactPersonStatusEntryCount", contact);
    if (count != null && count > 0) {
      executeUpdate("ContactPerson.updateDWHContactPersonStatus", contact);
    } else {
      executeUpdate("ContactPerson.insertDWHContactPersonStatus", contact);
    }
  }

  @Override
  public void deleteLocalContact(ContactPerson contact) {
    executeDelete("ContactPerson.deleteLocalContact", contact);
  }

  @Override
  public void markLocalContactDeleted(ContactPerson contact) {
    contact.setDeleted(1);
    executeUpdate("ContactPerson.markLocalContactPersonDeleted", contact);
  }

  @Override
  public List<ContactPerson> listContactPersonsIncludingDeleted(List<Long> partyIds) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("partyIds", partyIds);
    return performListQuery("ContactPerson.GetContactPersons4CustomerIncludingDeleted", params);
  }

  @Override
  public List<ContactPerson> listContactPersonsInclLocalContactsAndDeletedContacts(List<Long> partyIds) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("partyIds", partyIds);
    return performListQuery("ContactPerson.GetAllContactPersons4CustomersIncludingDeleted", params);
  }
}
