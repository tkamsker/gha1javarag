package at.a1ta.cuco.core.shared.model.seg;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.ProductGroup;
import at.a1ta.cuco.core.shared.dto.RTCode;

public class MultiPartyProductGroup implements Serializable {

  private Long id;
  private String code;
  private String name;
  private String description;
  private String anbLookup;
  private Date updateTs;

  private Map<Long, Integer> nrNotes = new HashMap<Long, Integer>();
  private Map<Long, Integer> nrNotesImported = new HashMap<Long, Integer>();
  private Map<Long, Integer> nrSingleTurnarounds = new HashMap<Long, Integer>();
  private Map<Long, Integer> nrReminders = new HashMap<Long, Integer>();
  private Map<Long, Boolean> ta = new HashMap<Long, Boolean>();
  private Map<Long, Boolean> anb = new HashMap<Long, Boolean>();
  private Map<Long, Boolean> notInterested = new HashMap<Long, Boolean>();

  private List<RTCode> rtCodes = new ArrayList<RTCode>();
  private List<Party> parties = new ArrayList<Party>();

  private static final Comparator<Party> MARKER_COMPARATOR = new Comparator<Party>() {
    @Override
    public int compare(Party o1, Party o2) {
      Integer m1 = o1.getMarker();
      Integer m2 = o2.getMarker();

      return m1.compareTo(m2);
    }
  };

  public MultiPartyProductGroup(ProductGroup source) {
    this.id = source.getId();
    this.code = source.getCode();
    this.name = source.getName();
    this.description = source.getDescription();
    this.anbLookup = source.getAnbLookup();
    this.updateTs = source.getUpdateTs();
  }

  public void addProductGroup(ProductGroup source, Party party) {
    nrNotes.put(party.getId(), source.getNrNotes());
    nrNotesImported.put(party.getId(), source.getNrNotesImported());
    nrSingleTurnarounds.put(party.getId(), source.getNrSingleTurnarounds());
    nrReminders.put(party.getId(), source.getNrReminders());
    ta.put(party.getId(), source.hasTa());
    anb.put(party.getId(), source.hasAnb());
    notInterested.put(party.getId(), source.isNotInterested());

    parties.add(party);
    Collections.sort(parties, MARKER_COMPARATOR);
  }

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public String getCode() {
    return code;
  }

  public void setCode(String code) {
    this.code = code;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public String getAnbLookup() {
    return anbLookup;
  }

  public void setAnbLookup(String anbLookup) {
    this.anbLookup = anbLookup;
  }

  public Date getUpdateTs() {
    return updateTs;
  }

  public void setUpdateTs(Date updateTs) {
    this.updateTs = updateTs;
  }

  public void setNrNotes(Long partyId, int nrNotes) {
    this.nrNotes.put(partyId, nrNotes);
  }

  public int getNrNotes(Long partyId) {
    return nrNotes.get(partyId);
  }

  public int getNrNotesImported(Long partyId) {
    return nrNotesImported.get(partyId);
  }

  public void setNrNotesImported(Long partyId, Integer nrNotesImported) {
    this.nrNotesImported.put(partyId, nrNotesImported);
  }

  public void setNrSingleTurnarounds(Long partyId, Integer nrSingleTurnarounds) {
    this.nrSingleTurnarounds.put(partyId, nrSingleTurnarounds);
  }

  public int getNrSingleTurnarounds(Long partyId) {
    return this.nrSingleTurnarounds.get(partyId);
  }

  public boolean hasOneTa(ArrayList<Long> partyIds) {
    for (Long partyId : partyIds) {
      boolean hasTa = ta.get(partyId);
      if (hasTa) {
        return true;
      }
    }
    return false;
  }

  public boolean hasTa(Long partyId) {
    return ta.get(partyId);
  }

  public void setTa(Long partyId, boolean ta) {
    this.ta.put(partyId, ta);
  }

  public boolean hasOneAnb(ArrayList<Long> partyIds) {
    for (Long partyId : partyIds) {
      boolean hasAnb = anb.get(partyId);
      if (hasAnb) {
        return true;
      }
    }
    return false;
  }

  public boolean hasAnb(Long partyId) {
    return anb.get(partyId);
  }

  public void setAnb(Long partyId, boolean anb) {
    this.anb.put(partyId, anb);
  }

  public List<RTCode> getRTCodes() {
    return rtCodes;
  }

  public void setRTCodes(java.util.List<RTCode> codes) {
    this.rtCodes = codes;
  }

  public void setNotInterested(Long partyId, boolean notInterested) {
    this.notInterested.put(partyId, notInterested);
  }

  public boolean isNotInterested(Long partyId) {
    return notInterested.get(partyId);
  }

  public int getNrReminders(Long partyId) {
    return nrReminders.get(partyId);
  }

  public void setNrReminders(Long partyId, int nrReminders) {
    this.nrReminders.put(partyId, nrReminders);
  }

  public List<Party> getParties() {
    return parties;
  }

  public boolean hasAnyIcon(Long partyId) {
    return anb.get(partyId) || ta.get(partyId) || getNrReminders(partyId) > 0 || getNrNotes(partyId) > 0 || getNrNotesImported(partyId) > 0
        || getNrSingleTurnarounds(partyId) > 0;
  }
}
