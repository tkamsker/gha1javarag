package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class PartyProfileInfo implements Serializable {

    private static final long serialVersionUID = 1L;

    public static final int ERROR = 99;

    public static final int LOADING = -1;

    public static final int NOT_RECEIVED = 98;

    public static final int LOADED = 0;

    private int staus = LOADING;

    private List<PartyProfileNPSInfo> scores = new ArrayList<PartyProfileNPSInfo>();

    private PartyProfileSolvency solvency;
    
    private PointOfSaleInfo posInfo;
    
    private SupportingUnit supportingUnit;

    private String teamName;
    
    private String supportUserName;
    
    private String supportUserId;
    
    private boolean shopSupport;
    
    private String accountManagementSegment;

    public PartyProfileInfo() {
        // default constructor to support GWT parsing
    }

    public PartyProfileInfo(int staus) {
        this.staus = staus;
    }

    public int getStaus() {
        return staus;
    }

    public void setStaus(int staus) {
        this.staus = staus;
    }

    public List<PartyProfileNPSInfo> getScores() {
        return scores;
    }

    public void setScores(List<PartyProfileNPSInfo> scores) {
        this.scores = scores;
    }

    public void addToScores(PartyProfileNPSInfo score) {
        if (this.scores == null) {
            this.scores = new ArrayList<PartyProfileNPSInfo>();
        }
        this.scores.add(score);
    }

    public PartyProfileSolvency getSolvency() {
        return solvency;
    }

    public void setSolvency(PartyProfileSolvency solvency) {
        this.solvency = solvency;
    }

    public PointOfSaleInfo getPosInfo() {
        return posInfo;
    }

    public void setPosInfo(PointOfSaleInfo posInfo) {
        this.posInfo = posInfo;
    }
    
    public String getTeamName() {
        return teamName;
    }

    public void setTeamName(String teamName) {
        this.teamName = teamName;
    }

    public String getSupportUserName() {
        return supportUserName;
    }

    public void setSupportUserName(String supportUserName) {
        this.supportUserName = supportUserName;
    }
    
    public boolean isShopSupport() {
        return shopSupport;
    }

    public void setShopSupport(boolean shopSupport) {
        this.shopSupport = shopSupport;
    }

    public String getSupportUserId() {
        return supportUserId;
    }

    public void setSupportUserId(String supportUserId) {
        this.supportUserId = supportUserId;
    }

    public String getAccountManagementSegment() {
        return accountManagementSegment;
    }

    public void setAccountManagementSegment(String accountManagementSegment) {
        this.accountManagementSegment = accountManagementSegment;
    }

    public SupportingUnit getSupportingUnit() {
        return supportingUnit;
    }

    public void setSupportingUnit(SupportingUnit supportingUnit) {
        this.supportingUnit = supportingUnit;
    }
}
