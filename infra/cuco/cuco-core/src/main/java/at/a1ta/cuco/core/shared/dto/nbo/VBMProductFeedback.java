package at.a1ta.cuco.core.shared.dto.nbo;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class VBMProductFeedback implements Serializable {
	private Long customerId;
	private String productId;
	private String monthYearPeriod;
	private VBMDeclineReason selectedDeclineReason=new VBMDeclineReason();
	private Date feedbackTime;
	private String feedbackUserName;
	private String feedbackUserId;
	private String feedBackGiven="N";
	public VBMDeclineReason getSelectedDeclineReason() {
		return selectedDeclineReason;
	}
	public void setSelectedDeclineReason(VBMDeclineReason selectedDeclineReason) {
		this.selectedDeclineReason = selectedDeclineReason;
	}
	public Date getFeedbackTime() {
		return feedbackTime;
	}
	public void setFeedbackTime(Date feedbackTime) {
		this.feedbackTime = feedbackTime;
	}
	public String getFeedbackUserName() {
		return feedbackUserName;
	}
	public void setFeedbackUserName(String feedbackUserName) {
		this.feedbackUserName = feedbackUserName;
	}
	public String getFeedbackUserId() {
		return feedbackUserId;
	}
	public void setFeedbackUserId(String feedbackUserId) {
		this.feedbackUserId = feedbackUserId;
	}
	public String getFeedBackGiven() {
		return feedBackGiven;
	}
	public void setFeedBackGiven(String feedBackGiven) {
		this.feedBackGiven = feedBackGiven;
	}
	
	public boolean isFeedbackGiven(){
		return feedBackGiven!=null;
	}
	public boolean isAccepted(){
		return feedBackGiven!=null && (selectedDeclineReason==null || selectedDeclineReason.getDeclineReasonId()==null || selectedDeclineReason.getDeclineReasonId().isEmpty());
	}
	public Long getCustomerId() {
		return customerId;
	}
	public void setCustomerId(Long customerId) {
		this.customerId = customerId;
	}
	public String getProductId() {
		return productId;
	}
	public void setProductId(String productId) {
		this.productId = productId;
	}
	public String getMonthYearPeriod() {
		return monthYearPeriod;
	}
	public void setMonthYearPeriod(String monthYearPeriod) {
		this.monthYearPeriod = monthYearPeriod;
	}
	
	


}
