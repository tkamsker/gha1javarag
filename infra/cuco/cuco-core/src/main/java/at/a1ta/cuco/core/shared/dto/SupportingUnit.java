package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class SupportingUnit implements Serializable {

    public static final int ERROR = 99;

    public static final int LOADING = -1;

    public static final int NOT_RECEIVED = 98;

    public static final int LOADED = 0;

    private int status = LOADING;

    private String skzText;

    private String supportName;

    private String emailAddress;

    private String phoneNumber;

    private boolean shopSupport;

    public SupportingUnit() {

    }

    public int getStatus() {
        return status;
    }

    public void setStatus(int status) {
        this.status = status;
    }

    public String getSkzText() {
        return skzText;
    }

    public void setSkzText(String skzText) {
        this.skzText = skzText;
    }

    public String getSupportName() {
        return supportName;
    }

    public void setSupportName(String supportName) {
        this.supportName = supportName;
    }

    public String getEmailAddress() {
        return emailAddress;
    }

    public void setEmailAddress(String emailAddress) {
        this.emailAddress = emailAddress;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public boolean isShopSupport() {
        return shopSupport;
    }

    public void setShopSupport(boolean shopSupport) {
        this.shopSupport = shopSupport;
    }

}
