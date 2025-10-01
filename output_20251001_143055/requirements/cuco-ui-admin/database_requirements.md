# cuco-ui-admin - Database Layer Requirements

## 1. Overview

Brief purpose within the application for the database layer.

## 2. Components

### Component Type: service_layer

- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/popup/DeviceAsAServiceSurchargeDialog.ui.xml (xml)
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/portlet/DeviceAsAServicePriceConfigView.ui.xml (xml)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/DeviceAsAServicePriceConfigView.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/DeviceAsAServicePriceConfigPresenter.java (java)

### Component Type: unknown

- cuco-ui-admin/pom.xml (xml)
- cuco-ui-admin/src/main/resources/applicationContext-admin.xml (xml)
- cuco-ui-admin/src/main/resources/META-INF/web-fragment.xml (xml) [consumes_api]
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/Admin.gwt.xml (xml) [consumes_api]
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/popup/AttributeConfigView.ui.xml (xml)
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/popup/ConfigurableListSelectorRuntimeConfigurationDialog.ui.xml (xml) [db]
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/popup/CouponSeriesEditView.ui.xml (xml)
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/popup/CloneProductsDialog.ui.xml (xml) [db] domain:product
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/popup/EditBaseMarketingProductDialog.ui.xml (xml) domain:product
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/popup/InventoryProductGroupView.ui.xml (xml) domain:product
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/popup/QuoteClearanceRuleConfigView.ui.xml (xml) domain:quote
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/popup/EditSBSProductsConfigurationView.ui.xml (xml) domain:product
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/popup/UserAdminSegmentView.ui.xml (xml)
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/popup/ProductOverviewConfigurationView.ui.xml (xml) [db] domain:product
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/portlet/ProductAdministrationPortletView.ui.xml (xml) domain:product
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/portlet/QuoteValidationConfigurationPortletView.ui.xml (xml) domain:quote
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/portlet/SalesInfoReportingPortletView.ui.xml (xml) domain:sales
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/portlet/SalesInfoAdministrationPortletView.ui.xml (xml) domain:sales
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/portlet/SurchargePriceConfigView.ui.xml (xml)
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/portlet/SalesConvReportingPortletView.ui.xml (xml) domain:sales
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/portlet/ManageSBSProductsConfigurationView.ui.xml (xml) domain:product
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/portlet/UITextsEditorPortletView.ui.xml (xml)
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/portlet/MarketingProductView.ui.xml (xml) domain:product
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/portlet/CouponSeriesAdministrationView.ui.xml (xml)
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/portlet/ProductManageAdministrationPortletView.ui.xml (xml) [db] domain:product
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/portlet/SalesConvAdministrationPortletView.ui.xml (xml) domain:sales
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/cct/portlet/BusinessFirewallView.ui.xml (xml) [db]
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/ui/cct/portlet/BusinessInternetProfessionalView.ui.xml (xml) [db]
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/quoteflashinfo/popup/QuoteFlashInfoEditView.ui.xml (xml) domain:quote
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/gwtIbatis/GwtIbatisPortletView.ui.xml (xml) [db]
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/flashinfo/FlashAdministrationView.ui.xml (xml)
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/flashinfo/popup/RoleSelectionView.ui.xml (xml) [db]
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/flashinfo/popup/FlashInfoEditView.ui.xml (xml)
- cuco-ui-admin/src/main/resources/at/a1ta/cuco/ui/admin/client/flashinfo/popup/CustomerBlockEditView.ui.xml (xml) domain:customer
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/AdminHeader.ui.xml (xml)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/ProductOverviewConfigurationPresenter.java (java) [consumes_api, db] domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/EditSBSProductsConfigurationView.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/ConfigurableListSelectorRuntimeConfigurationDialog.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/QuoteClearanceRuleConfigPresenter.java (java) domain:quote
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/AttributeConfigView.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/ProductOverviewConfigurationView.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/AttributeConfigPresenter.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/EditSBSProductsConfigurationPresenter.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/QuoteClearanceRuleConfigView.java (java) domain:quote
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/SurchargePriceConfigView.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/ManageSBSProductsConfigurationView.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/ManageSBSProductsConfigurationPresenter.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/QuoteValidationConfigurationPortletPresenter.java (java) domain:quote
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/QuoteValidationConfigurationPortletView.java (java) domain:quote
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/cct/ConfigurableField.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/cct/ConfigurableItemRenderer.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/cct/portlet/BaseCctConfigurationView.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/cct/portlet/CctConfigurationHelper.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/cct/portlet/BaseCctConfigurationPresenter.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/cct/portlet/BaseCctConfigurationTooltipItemHasCell.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/popup/EditSBSProductsConfigurationPopup.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/popup/AttributeConfigPopup.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/popup/QuoteClearanceRuleConfigPopup.java (java) domain:quote


## 3. Functionality

- **Main Features:** Heuristic summary based on component classification.
- **Technology Stack (top):** mybatis, spring_framework
- **Design Patterns (top):** n/a
- **Inputs/Outputs:** API exposure 0, API consumers 3, DB interactions 9.
- **Key Methods/Functions:** [To be derived in advanced analysis]

## 4. Dependencies

- [To be cross-linked]

## 5. Notes

- [Business rule nuances]
