package at.a1ta.cuco.admin.ui.common.client.bundle;

import at.a1ta.bite.ui.client.generator.textpool.Prefix;
import at.a1ta.bite.ui.client.generator.textpool.TextPool;

@Prefix("admin_")
public interface AdminCommonTextPool extends TextPool {

  String loading();

  String noData();

  String error();

  String yes();

  String no();

  String info();

  String save();

  String cancel();

  String delete();

  String deleteQuestion(String name);

  String deleted(String name);

  String saved(String name);

  String manage();

  String segSettingsName();

  String segSettingsDescription();

  /* VIP */
  String vipAmount();

  String vipBtnExport();

  String vipBtnSearch();

  String vipCreated();

  String vipCustomerID();

  String vipFrom();

  String vipName();

  String vipReporter();

  String vipSearch();

  String vipSearchTooltip();

  String vipSearchItem();

  String vipStatus();

  String vipTo();

  String vipAdminStatus();

  /* System messages */
  String systemMessageHeader();

  String smActive();

  String smCopy();

  String smDeleteImage();

  String smEditMessage();

  String smFrom();

  String smId();

  String smImage();

  String smImageFile();

  String smInactive();

  String smNewMessage();

  String smOptions();

  String smOptionsOneTime();

  String smOptionsOnlyMenue();

  String smPickImage();

  String smPreview();

  String smRoles();

  String smText();

  String smTitle();

  String smUntil();

  String smValidity();

  /* Check usage */
  String checkUsageAction();

  String checkUsageCustomerRequestOverview();

  String checkUsageDate();

  String checkUsageDistinct();

  String checkUsageLoginOverview();

  String checkUsageName();

  String checkUsageOperation();

  String checkUsageTotal();

  String checkUsageUuser();

  /* Reporting */
  String reportingButtonLoad();

  String reportingLabelJumpto();

  String reportingGridHeadId();

  String reportingGridHeadName();

  String reportingGridHeadQuery();

  String reportingGridHeadLongrunning();

  /* Ibatis */
  String administrationIbatisClearall();

  String administrationIbatisClearallDone();

  String administrationIbatisClearDone();

  String administrationIbatisFlush();

  String administrationIbatisColumnName();

  /* Team */
  String teamAddMember();

  String teamName();

  String teamNtAccount();

  String teamOe();

  String teamDelete();

  String teamTeam();

  String teamAddMemberError();

  String teamDeleteMemberQuestion();

  String teamDeleteTeammember();

  String teamDeleteText();

  String teamDeleteError();

  String teamAdd();

  String teamDesc();

  String teamCreation();

  String teamCreateDate();

  String teamDeleteTeamQuestion();

  String teamDeleteTeam();

  String teamAddService();

  String teamService();

  String teamCosts();

  String teamAddServiceError();

  String teamDeleteServiceQuestion();

  String teamDeleteService();

  String teamSelectServiceHeading();

  String teamButtonAdd();

  String teamButtonDelete();

  String teamSelectMemberDialog();

  String teamDialogNameLabel();

  String teamDialogDescriptionLabel();

  /* Import User-Shop Assignment */

  String importusershopdata_selectimportfile();

  String importusershopdata_logerase();

  String importusershopdata_logdownload();

  String importusershopdata_logentries();

  String importusershopdata_logfilename();

  String importusershopdata_fileseperator();

  /* Unknown area code */
  String unknownareacodeNew();

  String unknownareacodeGridColumnName();

  String unknownareacodeGridColumnDescription();

  String unknownareacodeGridColumnDelete();

  String unknownareacodeDeleteQuestion();

  String unknownareacodeLabel();

  String unknownareacodeMessageDelete();

  String unknownareacodeMessageSave();

  String unknownareacodeDialogHeading();

  String unknownareacodeDialogNameLabel();

  String unknownareacodeDialogDescriptionLabel();

  String unknownareacodeDialogValidation();

  /* Credit type */
  String credittypeNew();

  String credittypeGridColumnName();

  String credittypeGridColumnDescription();

  String credittypeGridColumnActive();

  String credittypeGridColumnDelete();

  String credittypeDeleteQuestion();

  String credittypeLabel();

  String credittypeMessageDelete();

  String credittypeMessageSave();

  String credittypeDialogHeading();

  String credittypeDialogNameLabel();

  String credittypeDialogDescriptionLabel();

  String credittypeDialogActivLabel();

  String credittypeDialogValidation();

  /* Services */
  String serviceDialogHeading();

  String serviceDialogCpServicedata();

  String serviceDialogFromLabel();

  String serviceDialogToLabel();

  String serviceDialogNameLabel();

  String serviceDialogDescription();

  String serviceDialogEmployeeinfo();

  String serviceDialogCpChargingdata();

  String serviceDialogCostsLabel();

  String serviceDialogCostsTooltip();

  String serviceDialogMultiLabel();

  String serviceDialogProductcodeLabel();

  String serviceDialogChargingtypeLabel();

  String serviceDialogCredittypeLabel();

  String serviceDialogCpClarifydata();

  String serviceDialogReason3Value();

  String serviceDialogProductLabel();

  String serviceDialogReason1Label();

  String serviceDialogReason2Label();

  String serviceDialogReason3Label();

  String serviceDialogResultLabel();

  String serviceDialogValidation();

  String serviceDialogValidationCosts();

  String serviceDialogValidationMulti();

  String serviceNew();

  String serviceGridColumnName();

  String serviceGridColumnFrom();

  String serviceGridColumnTo();

  String serviceGridColumnCosts();

  String serviceGridColumnDelete();

  String serviceDeleteQuestion();

  String serviceLabel();

  String serviceMessageDelete();

  String serviceMessageSave();

  /* Authority configuration */
  String authName();

  String authGridColumnId();

  String authGridColumnName();

  String authGridColumnDescription();

  String authGridColumnApp();

  String authGridColumnDelete();

  /* Configuration */
  String configName();

  String configGridColumnKey();

  String configGridColumnValue();

  String configGridColumnType();

  String configGridColumnApp();

  String configGridColumnSensitive();

  String configGridColumnDelete();

  /* App configuration portlet */
  String appName();

  String appGridColumnTabs();

  String appGridColumnId();

  String appGridColumnName();

  String appGridColumnShort();

  String appGridColumnType();

  String appGridColumnDelete();

  String messageboxDelete();

  String messageboxSave();

  String messageboxDeleteError();

  String messageboxSaveError();

  String dialogSave();

  String dialogUse();

  String dialogCancel();

  String rtcodeSave();

  String rtcodeSaveDone();

  String rtcodeSaveError();

  String uitexts_searchData();

  String uitexts_saveData();

  String uitexts_resetData();

  String uitexts_changes();

  String uitexts_searchInfo();

  String uitexts_changesFailed(String errorcount);

  String uitexts_sendEmailFailed();

  String uitexts_changesFailedDetails(String key, String value);

  String uitexts_changesDone(String amount);

  String uitexts_UIkey();

  String uitexts_UIvalue();

  String uitexts_cancelSave();

  String uitexts_acceptSave();

  String uitexts_confirmationSave(String amount);

  String adminGotoCuCo();

  // new product overview configurations
  String productBrowserTableViewAdminMenuName();

  String productBrowserTableViewAmountOfSubscriptionToPreloadLabel();

  String productBrowserTableViewDepthOfProductTreeLabel();

  String productBrowserTableViewModeLabel();

  String productBrowserTableViewWhitelistLabel();

  String productBrowserTableViewBlacklistLabel();

  String productBrowserTableViewWhitelist();

  String productBrowserTableViewBlacklist();

  String productBrowserTableViewWhitelistChoiceLabel();

  String productBrowserTableViewBlacklistChoiceLabel();

  String reset();

  // Visit Product Entries Tab

  String productEntries_administration_newProductEntry();

  String productEntries_categorieColumn();

  String productEntries_nameColumn();

  String productEntries_aliasColumn();

  String productEntries_activationColumn();

  String productEntries_OrderToColumn();

  String productEntries_ProductId();

  String productEntries_ProductAlternativeId();

  String productEntries_ProductDisplayName();

  String productEntries_ProductCategory();

  String productEntries_Active();

  String productEntries_Sequence();

  String productEntries_SetupType();

  String productEntries_SetupCategory();

  String productEntries_QuoteStatus();

  String productEntries_AssigneeType();

  String productEntries_DefaultConfig();

  String productEntries_SINoteClass();

  String productEntries_SaveButtonText();

  String productEntries_NewSBSProductEntryButtonText();

  String productEntries_columnKey();

  String productEntries_columnValue();

  String productEntries_typeOfContractsColumn();

  String featureSegDisplay1Label();

  String featureSegDisplay2Label();

  String featureSegDisplay3Label();

  String featureSegDisplay4Label();

  String featureSegDisplay5Label();

  // Org-Structure Tab

  String importCalcOrgStructure();

  String exportUserId();

  String exportUserName();

  String exportRole();

  String exportLevel();

  String exportTeam();

  String exportSAPId();

  String exportSupervisorID();

  String exportSupervisorName();

  String portletOrgStructureInfo();

  String portletOrgStructureSuccessMessage();

  String portletOrgStructureWaitingMessage();

  String portletOrgStructureErrorFileStructureMessage();

  String portletOrgStructureUnknownErrorMessage();

  String portletOrgStructureMissingRights();

  String portletOrgStructureFailureReportMessage();

  String portletOrgStructureErrorReportGenerationFailure();

  String portletOrgStructureFailureUserNotInDB();

  String portletOrgStructureFailureSupervisorNotInDB();

  String portletOrgStructureFailureSupervisorNotInUserList();

  String portletOrgStructureFailureMultipleSheetsInXLS();

  String portletOrgStructureFailureHeadersMismatch();

  String marketingProduct_NameColumn();

  String marketingProduct_ValueColumn();

  String marketingProduct_TooltipColumn();

  String marketingProduct_UrlColumn();

  String marketingProduct_BindingColumn();

  String marketingProduct_BillingFrequencyColumn();

  String marketingProduct_SaleProductPriceColumn();

  String marketingProduct_SaleOneTimePriceColumn();

  String marketingProduct_LeaseProductPriceColumn();

  String marketingProduct_LeaseOneTimePriceColumn();

  String marketingProduct_SaleTypeValueSale();

  String marketingProduct_SaleTypeValueLease();

  String marketingProduct_AddColumnBaseMarketingProduct();

  String marketingProduct_AddColumnGroup();

  String marketingProduct_ActionColumnEdit();

  String marketingProduct_ActionColumnExpand();

  String marketingProduct_ActionColumnCollapse();

  String marketingProduct_ActionColumnMoveDown();

  String marketingProduct_ActionColumnMoveUp();

  String marketingProduct_ActionColumnEnable();

  String marketingProduct_ActionColumnDelete();

  String marketingProduct_DeleteDialogMessageDeleteBaseMarketingProduct();

  String marketingProduct_DeleteDialogMessageDeleteGroup();

  String marketingProduct_DialogAddGroupLabel();

  String marketingProduct_DialogEditGroupLabel();

  String marketingProduct_DialogEditMarketingProductLabel();

  String marketingProduct_DialogAddMarketingProductLabel();

  String marketingProduct_DialogMarketingProductName();

  String marketingProduct_DialogMarketingProductValue();

  String marketingProduct_DialogMarketingProductMinQuantity();

  String marketingProduct_DialogMarketingProductMaxQuantity();

  String marketingProduct_DialogMarketingProductBinding();

  String marketingProduct_DialogMarketingProductBillingFrequency();

  String marketingProduct_DialogMarketingProductUrl();

  String marketingProduct_DialogMarketingGroupName();

  String marketingProduct_DialogMarketingProductTooltip();
  
  String marketingProduct_DialogMarketingProductInfoText();

  String marketingProduct_DialogMarketingProductPrice();

  String marketingProduct_DialogMarketingProductOneTimePrice();

  String marketingProduct_DialogMarketingProductDiscount();

  String marketingProduct_DialogMarketingProductSalesType();

  String marketingProduct_DialogNameIsEmptyErrorMessage();

  String marketingProduct_DialogSaveButton();

  String marketingProduct_DialogCancelButton();

  String marketingProduct_DialogInvalidPriceErrorMessage();

  String marketingProduct_DialogInvalidDiscountErrorMessage();

  String marketingProduct_DialogInvalidDiscountPercentErrorMessage();

  String marketingProduct_AddNewProductButtonText();

  String marketingProduct_ExpandAllProductsButtonText();

  String marketingProduct_CollapseAllProductsButtonText();

  String marketingProduct_LoadProductsErrorMessage();

  String marketingProduct_AddBaseMarketingProductErrorMessage();

  String marketingProduct_EditBaseMarketingProductErrorMessage();

  String marketingProduct_DeleteBaseMarketingProductErrorMessage();

  String marketingProduct_DisableBaseMarketingProductErrorMessage();

  String marketingProduct_MoveBaseMarketingProductErrorMessage();

  String marketingProduct_DeleteDialogDeleteButton();

  String marketingProduct_DeleteDialogDisableButton();

  String marketingProduct_DeleteDialogCancelButton();

  String daas_MaxDiscountLabel();

  String daas_SurchargeConfig();

  String daas_DevicesHeading();

  String daas_OptionsHeading();

  String daas_DiscountColumn();

  String daas_SurchargeColumn();

  String daas_AddSurcharge();

  String daas_DiscountEmpty();

  String daas_SurchargeEmpty();

  String daas_LoadPriceConfigErrorMessage();

  String daas_SavePriceConfigErrorMessage();

  String daas_DiscountPriceConfigExistsErrorMessage();

  // clone products dialog

  String marketplaceProduct_DialogCloneProducts_product_name_label();

  String marketplaceProduct_DialogCloneProducts_product_offering_label();

  String marketplaceProduct_DialogCloneProducts_clone_product_label();

  // configurableListSelector dialog

  String configurableListSelector_ConfigurationTitle();

  String configurableListSelector_DialogEditConfigurableListSelectorLabel();

  String configurableListSelector_DialogCreateConfigurableListSelectorLabel();

  String configurableListSelector_DialogValueIsEmptyErrorMessage();

  String dialogConfigurableListSelector_DialogConfigurableListSelectorValue();

  String dialogConfigurableListSelector_DialogConfigurableListSelectorKey();

  String dialogConfigurableListSelector_DialogConfigurableListSelectorFilterForValues();

  String dialogConfigurableListSelector_DialogConfigurableListSelectorButtonName();

  String dialogConfigurableListSelector_DialogConfigurableListSelectorTooltip();

  String dialogConfigurableListSelector_DialogConfigurableListSelectorOfficialName();

  String dialogConfigurableListSelector_DialogConfigurableListSelectorOverviewName();

  String dialogConfigurableListSelector_DialogConfigurableListSelectorCuscoId();

  String dialogConfigurableListSelector_DialogConfigurableListSelectorDefaultValue();

  String dialogConfigurableListSelector_DialogConfigurableListSelectorMonthlyPrice();

  String dialogConfigurableListSelector_DialogConfigurableListSelectorYearlyPrice();

  String dialogConfigurableListSelector_DialogConfigurableListSelectorOneTimePrice();

  String dialogConfigurableListSelector_DialogConfigurableListSelectorDiscountPrice();

  String dialogConfigurableListSelector_DialogConfigurableListSelectorDiscountPercent();

  String dialogConfigurableListSelector_DialogSaveButton();

  String dialogConfigurableListSelector_DialogCancelButton();

  String configurableListSelector_FieldLabel();

  String configurableListSelector_AddButton();

  String configurableListSelector_SaveButton();

  String configurableListSelector_ProductSearchPlaceholder();

  String configurableListSelector_ProductSearch();

  String configurableListSelector_ProductResetSearch();

  String configurableListSelector_LoadError();

  String configurableListSelector_SaveError();

  String configurableListSelector_ProductInstanceSaved();

  String configurableListSelector_Value();

  String configurableListSelector_FilterForValues();

  String configurableListSelector_ButtonName();

  String configurableListSelector_Tooltip();

  String configurableListSelector_OfficialName();

  String configurableListSelector_OverviewName();

  String configurableListSelector_CuscoId();

  String configurableListSelector_DefaultValue();

  String configurableListSelector_MonthlyPrice();

  String configurableListSelector_YearlyPrice();

  String configurableListSelector_OneTimePrice();

  String configurableListSelector_Discount();

  String configurableListSelector_DiscountTo();

  String configurableListSelector_DiscountFrom();

  String configurableListSelector_TooltipMoveDown();

  String configurableListSelector_TooltipMoveUp();

  String configurableListSelector_TooltipEdit();

  String configurableListSelector_TooltipDelete();

  String configurableListSelector_DeletePopupMessage();

  String configurableListSelector_Enable();

  String configurableListSelector_Disable();

  String cct_bfw_v1_BusinessCase_label();

  String cct_bfw_v1_Access_label();

  String cct_bfw_v1_A1BusinessFirewall_label();

  String cct_bfw_v1_AdvancedRemoteAccess_label();

  String cct_bfw_v1_Sla_label();

  String cct_bfw_v1_Monitoring_label();

  String cct_bfw_v1_MinimumContractPeriod_label();

  String cct_a1bip_v1_GeneralSection_BusinessCase_label();

  String cct_a1bip_v1_GeneralSection_OanGpon_label();

  String cct_a1bip_v1_GeneralSection_ContractChange_label();

  String cct_a1bip_v1_GeneralSection_AddMeinA1BusinessRegistration_label();

  String cct_a1bip_v1_GeneralSection_Transfer_label();

  String cct_a1bip_v1_GeneralSection_PrintAllContractPeriods_label();

  String cct_a1bip_v1_GeneralSection_ContractPeriod_label();

  String cct_a1bip_v1_BIPSection_TopService_label();

  String cct_a1bip_v1_BIPSection_Speed_label();

  String cct_a1bip_v1_BIPSection_AdditionalOptions_label();

  String cct_a1bip_v1_BIPSection_ContractPeriod_label();

  String cct_a1bip_v1_BIPSection_VpnAccess_label();

  String cct_a1bip_v1_BIPSection_RouterConfig_label();

  String cct_a1bip_v1_BIPSection_AdditionalIpPackets_label();

  String cct_a1bip_v1_BusinessFirewallSection_A1BusinessFirewall_label();

  String cct_a1bip_v1_BusinessFirewallSection_AdvancedRemoteAccess_label();

  String cct_a1bip_v1_BusinessFirewallSection_Sla_label();

  String cct_a1bip_v1_BusinessFirewallSection_Monitoring_label();

  String cct_a1bip_v1_BusinessFirewallSection_MinimumContractPeriod_label();

  String cct_a1bip_v1_BIPSection_ShowBusinessFirewall_label();

  String cct_a1bip_v1_GeneralSection_ConfirmMcd_label();
}
