package at.a1ta.cuco.core.shared.dto.salesinfo.salesconvnote;

import java.util.ArrayList;
import java.util.List;

import at.a1ta.cuco.core.shared.dto.Attribute;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.generic.FileAttachment;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSProductNote;

public class SalesConvNote extends SalesInfoNote {
  private static final long serialVersionUID = 1L;

  private ContactType contactType;

  private String campaignId;
  private String campaignName;
  private String campaignCallNumber;

  private List<Attribute> feedbackAttributes;
  private String feedbackText;

  private List<SBSProductNote> productNotes;

  private List<FileAttachment> fileAttachments;

  /**
   * Copy Constructor
   * 
   * @param salesConvNote a <code>SalesConvNote</code> object
   */
  public SalesConvNote(SalesConvNote salesConvNote) {
    super(salesConvNote);
    this.contactType = salesConvNote.contactType;
    this.campaignId = salesConvNote.campaignId;
    this.campaignName = salesConvNote.campaignName;
    this.campaignCallNumber = salesConvNote.campaignCallNumber;
    List<Attribute> attribs = new ArrayList<Attribute>();
    for (Attribute attrib : salesConvNote.getFeedbackAttributes()) {
      attribs.add(new Attribute(attrib));
    }
    this.feedbackAttributes = attribs;
    this.feedbackText = salesConvNote.feedbackText;
    List<SBSProductNote> notes = new ArrayList<SBSProductNote>();
    for (SBSProductNote note : salesConvNote.getProductNotes()) {
      notes.add(new SBSProductNote(note));
    }
    this.productNotes = salesConvNote.productNotes;
    List<FileAttachment> attachments = new ArrayList<FileAttachment>();
    for (FileAttachment atchment : salesConvNote.getFileAttachments()) {
      attachments.add(new FileAttachment(atchment));
    }
    this.fileAttachments = attachments;
  }

  public SalesConvNote() {
    super();
  }

  public List<FileAttachment> getFileAttachments() {
    return fileAttachments;
  }

  public void setFileAttachments(List<FileAttachment> fileAttachments) {
    this.fileAttachments = fileAttachments;
  }

  public ContactType getContactType() {
    return contactType;
  }

  public void setContactType(ContactType contactType) {
    this.contactType = contactType;
  }

  public List<Attribute> getFeedbackAttributes() {
    return feedbackAttributes;
  }

  public void setFeedbackAttributes(List<Attribute> feedbackAttributes) {
    this.feedbackAttributes = feedbackAttributes;
  }

  public String getFeedbackText() {
    return feedbackText;
  }

  public void setFeedbackText(String feedbackText) {
    this.feedbackText = feedbackText;
  }

  public String getCampaignId() {
    return campaignId;
  }

  public void setCampaignId(String CampaignId) {
    this.campaignId = CampaignId;
  }

  public String getCampaignName() {
    return campaignName;
  }

  public void setCampaignName(String CampaignName) {
    this.campaignName = CampaignName;
  }

  public List<SBSProductNote> getProductNotes() {
    return productNotes;
  }

  public void setProductNotes(List<SBSProductNote> productNotes) {
    this.productNotes = productNotes;
  }

  public String getCampaignCallNumber() {
    return campaignCallNumber;
  }

  public void setCampaignCallNumber(String campaignCallNumber) {
    this.campaignCallNumber = campaignCallNumber;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = super.hashCode();
    result = prime * result + ((campaignCallNumber == null) ? 0 : campaignCallNumber.hashCode());
    result = prime * result + ((campaignId == null) ? 0 : campaignId.hashCode());
    result = prime * result + ((campaignName == null) ? 0 : campaignName.hashCode());
    result = prime * result + ((contactType == null) ? 0 : contactType.hashCode());
    result = prime * result + ((feedbackAttributes == null) ? 0 : feedbackAttributes.hashCode());
    result = prime * result + ((feedbackText == null) ? 0 : feedbackText.hashCode());
    result = prime * result + ((fileAttachments == null) ? 0 : fileAttachments.hashCode());
    result = prime * result + ((productNotes == null) ? 0 : productNotes.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) {
      return true;
    }
    if (!super.equals(obj)) {
      return false;
    }
    if (getClass() != obj.getClass()) {
      return false;
    }
    SalesConvNote other = (SalesConvNote) obj;
    if (campaignCallNumber == null) {
      if (other.campaignCallNumber != null) {
        return false;
      }
    } else if (!campaignCallNumber.equals(other.campaignCallNumber)) {
      return false;
    }
    if (campaignId == null) {
      if (other.campaignId != null) {
        return false;
      }
    } else if (!campaignId.equals(other.campaignId)) {
      return false;
    }
    if (campaignName == null) {
      if (other.campaignName != null) {
        return false;
      }
    } else if (!campaignName.equals(other.campaignName)) {
      return false;
    }
    if (contactType != other.contactType) {
      return false;
    }
    if (feedbackAttributes == null) {
      if (other.feedbackAttributes != null) {
        return false;
      }
    } else if (!feedbackAttributes.equals(other.feedbackAttributes)) {
      return false;
    }
    if (feedbackText == null) {
      if (other.feedbackText != null) {
        return false;
      }
    } else if (!feedbackText.equals(other.feedbackText)) {
      return false;
    }
    if (fileAttachments == null) {
      if (other.fileAttachments != null) {
        return false;
      }
    } else if (!fileAttachments.equals(other.fileAttachments)) {
      return false;
    }
    if (productNotes == null) {
      if (other.productNotes != null) {
        return false;
      }
    } else if (!productNotes.equals(other.productNotes)) {
      return false;
    }
    return true;
  }
}
