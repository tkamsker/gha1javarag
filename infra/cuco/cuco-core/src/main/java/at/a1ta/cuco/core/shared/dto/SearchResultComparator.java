package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Comparator;

public class SearchResultComparator implements Comparator<Party>, Serializable {

	@Override
	public int compare(Party o1, Party o2) {
		String comp1 = buildComparisonString(o1);
		String comp2 = buildComparisonString(o2);
		return comp1.compareTo(comp2);
	}

	private String buildComparisonString(Party party) {
		return party.getLastname() + " " + party.getFirstname();
	}
}
