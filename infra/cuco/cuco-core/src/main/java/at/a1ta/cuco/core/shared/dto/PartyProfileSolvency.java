package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class PartyProfileSolvency implements Serializable {
	
	private static final long serialVersionUID = 1L;
	
	private String creditLimit;
	
	public PartyProfileSolvency() {
		// default constructor to support GWT parsing
	}

	public String getCreditLimit() {
		return creditLimit;
	}

	public void setCreditLimit(String creditLimit) {
		this.creditLimit = creditLimit;
	}

}
