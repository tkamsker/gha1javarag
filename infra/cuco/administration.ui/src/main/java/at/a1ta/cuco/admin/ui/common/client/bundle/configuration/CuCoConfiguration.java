package at.a1ta.cuco.admin.ui.common.client.bundle.configuration;

public class CuCoConfiguration extends SettingsManager {
  public int applicationPagingSize() {
    return readInt("application_pagingSize");
  }

  public boolean segImportWriteCustomerInteractions() {
    try {
      final String s = readString("segimport_writeCustomerInteractions");
      return s == null ? false : Boolean.parseBoolean(s);
    } catch (Exception e) {
      return false;
    }
  }
}
