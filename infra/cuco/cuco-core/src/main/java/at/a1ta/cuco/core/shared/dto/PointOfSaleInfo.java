package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

import at.a1ta.bite.core.shared.util.CommonUtils;

public class PointOfSaleInfo implements Serializable {

    private int staus = LOADING;

    private String dealerId;

    private String dealerName;

    private String delearEmailId;

    private String dealerPhonenumber;

    private StandardAddress address;

    public static final int ERROR = 99;

    public static final int LOADING = -1;

    public static final int NOT_RECEIVED = 98;

    public static final int LOADED = 0;

    public PointOfSaleInfo() {
    }

    public PointOfSaleInfo(int staus, String dealerId, String dealerName) {
        this.staus = staus;
        this.dealerId = dealerId;
        this.dealerName = dealerName;
    }

    public int getStaus() {
        return staus;
    }

    public void setStaus(int staus) {
        this.staus = staus;
    }

    public StandardAddress getAddress() {
        return address;
    }

    public void setAddress(StandardAddress address) {
        this.address = address;
    }

    public String getDealerName() {
        return dealerName;
    }

    public void setDealerName(String dealerName) {
        this.dealerName = dealerName;
    }

    public String getDealerId() {
        return dealerId;
    }

    public void setDealerId(String dealerId) {
        this.dealerId = dealerId;
    }

    public String getNameAddressString() {
        return getDealerName() + (getAddress() != null ? ", " + buildCompleteAddressString() : "");
    }

    private String buildCompleteAddressString() {
        String addressString = CommonUtils.defaultString(getAddress().getStreet()) + " "
                + CommonUtils.defaultString(getAddress().getHouseNumber()) + ", "
                + CommonUtils.defaultString(getAddress().getPostcode()) + " "
                + CommonUtils.defaultString(getAddress().getCity()) + " ("
                + CommonUtils.defaultString(getAddress().getVillage()) + ")";

        return addressString.trim();
    }

    public String getDelearEmailId() {
        return delearEmailId;
    }

    public void setDelearEmailId(String delearEmailId) {
        this.delearEmailId = delearEmailId;
    }

    public String getDealerPhonenumber() {
        return dealerPhonenumber;
    }

    public void setDealerPhonenumber(String dealerPhonenumber) {
        this.dealerPhonenumber = dealerPhonenumber;
    }

}
