# cuco-ui-admin - Backend Layer Requirements

## 1. Overview

Brief purpose within the application for the backend layer.

## 2. Components

### Component Type: service_layer

- cuco-ui-admin/src/test/java/at/a1ta/cuco/test/AsyncServiceCaller.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/DeviceAsAServiceSurchargeDialog.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/DeviceAsAServiceProductsPresenter.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/DeviceAsAServiceAdditionalProductsPresenter.java (java) domain:product

### Component Type: servlet

- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/server/servlet/QuoteFlashInfoServletImpl.java (java) domain:quote
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/server/servlet/ProductOverviewConfigurationServletImpl.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/server/servlet/FlashInfoServletImpl.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/server/servlet/UserAdminSegmentServletImpl.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/server/servlet/ProductAdminServletImpl.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/server/servlet/SalesInfoServletImpl.java (java) domain:sales
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/server/servlet/SettingsEditorServletImpl.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/server/servlet/UITextsEditorServletImpl.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/ProductAdminServlet.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/ProductAdminServletAsync.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/UITextsEditorServlet.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/SalesInfoServlet.java (java) domain:sales
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/FlashInfoServlet.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/SettingsEditorServlet.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/ProductOverviewConfigurationServletAsync.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/QuoteFlashInfoServlet.java (java) domain:quote
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/QuoteFlashInfoServletAsync.java (java) domain:quote
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/ProductOverviewConfigurationServlet.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/FlashInfoServletAsync.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/UserAdminSegmentServletAsync.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/UserAdminSegmentServlet.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/UITextsEditorServletAsync.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/SalesInfoServletAsync.java (java) domain:sales
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/servlet/SettingsEditorServletAsync.java (java)

### Component Type: unknown

- cuco-ui-admin/src/test/java/at/a1ta/cuco/ui/admin/shared/helper/SbsNoteReportTreeGeneratorTest.java (java)
- cuco-ui-admin/src/test/java/at/a1ta/cuco/ui/admin/shared/helper/SbsNoteReportGeneratorTest.java (java)
- cuco-ui-admin/src/test/java/at/a1ta/cuco/ui/admin/client/presenter/popup/CouponSeriesEditPresenterTest.java (java)
- cuco-ui-admin/src/test/java/at/a1ta/cuco/ui/admin/client/presenter/portlet/CouponSeriesAdministrationPresenterTest.java (java)
- cuco-ui-admin/src/test/java/at/a1ta/cuco/ui/admin/client/presenter/portlet/ProductAdministrationPortletPresenterTest.java (java) domain:product
- cuco-ui-admin/src/test/java/at/a1ta/cuco/ui/admin/client/flashinfo/FlashAdministrationPresenterTest.java (java)
- cuco-ui-admin/src/test/java/at/a1ta/cuco/ui/admin/client/flashinfo/popup/FlashInfoEditPresenterTest.java (java)
- cuco-ui-admin/src/test/java/at/a1ta/cuco/test/TestUtils.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/shared/bean/InitData.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/shared/helper/SbsNoteReportTreeGenerator.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/shared/helper/AbstractReportExcelGenerator.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/shared/helper/TreeNode.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/shared/helper/SortedList.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/shared/helper/SbsNoteTreeData.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/shared/helper/TreeNodeIter.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/shared/helper/SalesConvNoteReportExcelGenerator.java (java) domain:sales
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/shared/helper/SbsNoteReportExcelGenerator.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/shared/helper/GranularityKey.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/AdminPortletFactory.java (java) [consumes_api, db]
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/LegacyInitializer.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/AdminEventBus.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/handler/InitializationHandler.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/AdminMainView.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/AdminUI.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/AdminHeader.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/AdminPortletPresenter.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/AdminMainPresenter.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/CouponSeriesEditPresenter.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/InventoryProductGroupPresenter.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/CloneProductsHelper.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/CouponSeriesEditView.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/UserAdminSegmentView.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/DeleteBaseMarketingProductPopup.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/CloneProductsDialog.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/EditBaseMarketingProductDialog.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/UserAdminSegmentPresenter.java (java) [consumes_api, db]
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/InventoryProductGroupView.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/PaymentHardwarePresenter.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/KimCellTree.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/UITextsEditorPortletView.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/ETGTProductsPresenter.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/SalesConvAdministrationPortletPresenter.java (java) domain:sales
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/UITextsEditorPortletPresenter.java (java) [consumes_api, db]
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/MarketingProductActionItemHasCell.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/MarketplaceProductsPresenter.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/CloudCommunicationHardwarePresenter.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/CloudCommunicationProductsPresenter.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/MarketingProductTooltipItemHasCell.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/SalesInfoReportingPortletPresenter.java (java) domain:sales
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/SalesInfoAdministrationPortletView.java (java) domain:sales
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/ProductAdministrationPortletView.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/SalesConvReportingPortletPresenter.java (java) domain:sales
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/SalesConvAdministrationPortletView.java (java) domain:sales
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/CouponSeriesAdministrationView.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/ProductManageAdministrationPortletView.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/BaseMarketingProductPresenter.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/BusinessInternetProductsPresenter.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/MarketingProductView.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/BusinessNetworkProductsPresenter.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/MarketingProductViewInterface.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/ProductAdministrationPortletPresenter.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/BusinessNetworkHardwarePresenter.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/ProductManageAdministrationPortletPresenter.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/CouponSeriesAdministrationPresenter.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/SalesConvReportingPortletView.java (java) domain:sales
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/SalesInfoReportingPortletView.java (java) domain:sales
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/SalesInfoAdministrationPortletPresenter.java (java) domain:sales
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/coupon/AdminCouponSeriesTextPool.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/cct/portlet/BusinessInternetProfessionalPresenter.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/cct/portlet/BusinessFirewallPresenter.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/cct/portlet/BusinessInternetProfessionalView.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/cct/portlet/BusinessFirewallView.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/popup/InventoryProductGroupPopup.java (java) domain:product
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/popup/CouponSeriesEditPopup.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/quoteflashinfo/popup/QuoteFlashInfoEditPresenter.java (java) domain:quote
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/quoteflashinfo/popup/QuoteFlashInfoEditPopup.java (java) domain:quote
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/quoteflashinfo/popup/QuoteFlashInfoEditView.java (java) domain:quote
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/gwtIbatis/GwtIbatisPortletPresenter.java (java) [consumes_api, db]
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/gwtIbatis/GwtIbatis.java (java) [db]
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/gwtIbatis/GwtIbatisPortletView.java (java) [consumes_api, db]
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/flashinfo/FlashAdministrationPresenter.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/flashinfo/FlashAdministrationView.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/flashinfo/AdminFlashInfoTextPool.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/flashinfo/popup/FlashInfoEditPresenter.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/flashinfo/popup/CustomerBlockEditView.java (java) domain:customer
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/flashinfo/popup/FlashInfoEditView.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/flashinfo/popup/RoleSelectionPresenter.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/flashinfo/popup/FlashInfoEditPopup.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/flashinfo/popup/CustomerBlockEditPresenter.java (java) domain:customer
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/flashinfo/popup/RoleSelectionPopup.java (java)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/flashinfo/popup/CustomerBlockEditPopup.java (java) domain:customer
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/flashinfo/popup/RoleSelectionView.java (java)


## 3. Functionality

- **Main Features:** Heuristic summary based on component classification.
- **Technology Stack (top):** mybatis
- **Design Patterns (top):** n/a
- **Inputs/Outputs:** API exposure 0, API consumers 5, DB interactions 6.
- **Key Methods/Functions:** [To be derived in advanced analysis]

### API Endpoints Summary

- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/AdminPortletFactory.java (consumes)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/popup/UserAdminSegmentPresenter.java (consumes)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/ui/portlet/UITextsEditorPortletPresenter.java (consumes)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/gwtIbatis/GwtIbatisPortletPresenter.java (consumes)
- cuco-ui-admin/src/main/java/at/a1ta/cuco/ui/admin/client/gwtIbatis/GwtIbatisPortletView.java (consumes)

## 4. Dependencies

- [To be cross-linked]

## 5. Notes

- [Business rule nuances]
