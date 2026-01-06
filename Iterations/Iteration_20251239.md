 cat log_production_req_gen_2025-12-30_12-40-28.log
nohup: ignoring input
===================================
PRD Generation for: cuco-ui-admin
Source: /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin
===================================
Step 1: Running analysis pipeline...
Pipeline started (PID: 859641)
Log: ./logs/log_cuco-ui-admin_pipeline_2025-12-30_12-40-28.log
✓ Pipeline completed successfully

Step 2: Generating PRD documents...
Backend PRD generation started (PID: 950252)
Frontend PRD generation started (PID: 950253)

===================================
✗ PRD Generation Failed
===================================
Check log files:
  - Backend: ./logs/log_cuco-ui-admin_backend_prd_2025-12-30_12-40-28.log
  - Frontend: ./logs/log_cuco-ui-admin_frontend_prd_2025-12-30_12-40-28.log

 cat ./logs/log_cuco-ui-admin_backend_prd_2025-12-30_12-40-28.log
Usage: codeindex prd [OPTIONS] [[database|services|frontend|full]]
Try 'codeindex prd --help' for help.

Error: Invalid value for '[[database|services|frontend|full]]': 'backend' is not one of 'database', 'services', 'frontend', 'full'.

tkamsker@vlcucad001-eatnl:~/development/Iteration20/gha1javarag$ cat ./logs/log_cuco-ui-admin_frontend_prd_2025-12-30_12-40-28.log
2026-01-01 01:28:35 [INFO] codeindex.schemas: Weaviate is healthy: 1.32.13
2026-01-01 01:28:35 [INFO] codeindex.schemas: Weaviate is healthy: 1.32.13
2026-01-01 01:28:35 [INFO] codeindex.services.weaviate_store: Connected to Weaviate at http://localhost:8080
2026-01-01 01:28:35 [INFO] codeindex.schemas: Weaviate schema already exists, skipping creation
============================================================
PRD Generation Configuration
============================================================
Layer:         frontend
Project:       cuco-ui-admin
Source Dir:    /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c
Output Dir:    output/cuco-ui-admin/prd
Format:        markdown
Force Refresh: False
Parallel:      10 workers
LLM Timeout:   120s
LLM Retries:   3
============================================================

2026-01-01 01:28:35 [INFO] codeindex.services.ollama_client: OllamaClient initialized: model=qwen2.5-coder:32b, read_timeout=240.0s, connect_timeout=10.0s

============================================================
Starting PRD Generation
============================================================

[INFO] Analyzing frontend layer...
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Found 1424 frontend files
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing 1424 files...
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: tiny_mce_src.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: Symbole.html
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: charmap.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in tiny_mce_src.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileCostsPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in Symbole.html, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: Kunden.html
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in charmap.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in MobileCostsPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in Kunden.html, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: ContactsPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: preview.html
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in ContactsPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: source_editor.htm
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: Kundensuche_ohne_frame.html
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in preview.html, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: InteractionPortletView.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SNGMobileAccessSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in Kundensuche_ohne_frame.html, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberEditPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: fullpage.htm
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in InteractionPortletView.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SNGAuenstelleSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteWidget.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberEditPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobilePasswordView.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SNGMobileAccessSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: BIZKOSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SNGAuenstelleSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: CustomerEquipmentSumsView.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteWidget.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: CustomerInteractionView.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: ImageListWidget.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in MobilePasswordView.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in BIZKOSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in CustomerEquipmentSumsView.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditSBSProductsConfigurationView.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: AttributeConfigView.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in ImageListWidget.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SNGAuenstelleSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in CustomerInteractionView.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: dialog.htm
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: RestrictedPartyDataPortletView.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in EditSBSProductsConfigurationView.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in AttributeConfigView.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SNGAuenstelleSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SNGAuenstelleSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: ApothekennetzSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: de.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in RestrictedPartyDataPortletView.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SNGAuenstelleSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: MergeNonCustomerWithCustomerView.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditUserDialog.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in ApothekennetzSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: mctabs.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in de.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in MergeNonCustomerWithCustomerView.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: HardwareSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in EditUserDialog.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in mctabs.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: props.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in HardwareSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in props.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: pasteword.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: Beispiel2.htm
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: ReminderDateBox.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in pasteword.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in ReminderDateBox.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in Beispiel2.htm, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: VipHistoryPortletView.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: CuCoAuditActivity.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: emotions.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: Vertriebsaktivitaeten.html
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketplaceGroupCostsPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in VipHistoryPortletView.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in CuCoAuditActivity.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: PortletHeader.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in Vertriebsaktivitaeten.html, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in emotions.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in MarketplaceGroupCostsPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileCostsPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: cite.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in PortletHeader.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in MobileCostsPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in cite.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: row.htm
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteWidget.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: Popup.html
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesConvReportingPortletView.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteWidget.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: Highlighten.html
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in Highlighten.html, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionEditPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in Popup.html, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: dialog.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SalesConvReportingPortletView.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyNotesView.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in dialog.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in MyNotesView.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: Beispiel5.htm
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionEditPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberEditPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: CustomerEquipmentSumsView.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: cell.htm
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in Beispiel5.htm, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: WLANSchuleProductAndServicesWidget.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberEditPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: tiny_mce_popup.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsPartyNodeView.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in CustomerEquipmentSumsView.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in WLANSchuleProductAndServicesWidget.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsPartyNodeView.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in tiny_mce_popup.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: Angebote - Kopie.html
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: PaST.html
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: InitiativeAdministrationDetailsWidget.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: NameValuePairView.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsSAPSubscriptionNodeView.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in Angebote - Kopie.html, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in NameValuePairView.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in PaST.html, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: FixedLineSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in FixedLineSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: A1dameApothekeSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditMetadataWidget.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsSAPSubscriptionNodeView.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: CustomerEquipmentView.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: NoteHistoryView.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in A1dameApothekeSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: AbstractDetailsNodeView.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in NoteHistoryView.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: Angebote.html
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in EditMetadataWidget.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in CustomerEquipmentView.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: DaaSMarketingProductListItemWidget.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in Angebote.html, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in AbstractDetailsNodeView.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in DaaSMarketingProductListItemWidget.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: CustomerBlockEditView.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SettingsAdministrationView.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: BPBSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in CustomerBlockEditView.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SettingsAdministrationView.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: pastetext.htm
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in BPBSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: del.htm
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: TableViewRegionalPromotionPopup.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in TableViewRegionalPromotionPopup.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductOverviewPortletView.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: TurnoverPortletView.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in ProductOverviewPortletView.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductPortletView.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in TurnoverPortletView.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: DeviceAsAServiceSurchargeDialog.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in DeviceAsAServiceSurchargeDialog.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: props.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in ProductPortletView.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferInteractionsView.java
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in props.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: FIBSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in FIBSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferInteractionsView.java, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: PricePanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: UsageDataMobilPointsView.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in PricePanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in ProductSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: AnbNoteEditView.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in UsageDataMobilPointsView.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in AnbNoteEditView.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionEditPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionEditPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: ToDoGroupWidget.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: GwtSelectServiceDialog.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in ToDoGroupWidget.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in GwtSelectServiceDialog.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: props.htm
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: HierarchischeAnsicht.html
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in HierarchischeAnsicht.html, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: A1dameApothekeSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in A1dameApothekeSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: de.js
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in de.js, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: InternetSectionPanel.ui.xml
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: No form found in InternetSectionPanel.ui.xml, skipping
2026-01-01 01:28:36 [INFO] codeindex.services.frontend_analyzer: Analyzing: rule.htm
2026-01-01 01:29:08 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: source
2026-01-01 01:29:08 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 01:29:08 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 01:29:08 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:29:08 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:29:08 [INFO] codeindex.services.frontend_analyzer: Analyzing: Portfolio.html
2026-01-01 01:29:08 [INFO] codeindex.services.frontend_analyzer: No form found in Portfolio.html, skipping
2026-01-01 01:29:08 [INFO] codeindex.services.frontend_analyzer: Analyzing: cite.htm
2026-01-01 01:29:08 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: example_dialog_form
2026-01-01 01:29:08 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessMobileInternetSectionPanel.ui.xml
2026-01-01 01:29:08 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessMobileInternetSectionPanel.ui.xml, skipping
2026-01-01 01:29:08 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 01:29:08 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 01:29:08 [INFO] codeindex.services.frontend_analyzer: Analyzing: InitiativeAdministrationDetailsWidget.ui.xml
2026-01-01 01:29:08 [INFO] codeindex.services.frontend_analyzer: Using GWT UiBinder parser for InitiativeAdministrationDetailsWidget.ui.xml
2026-01-01 01:29:08 [INFO] codeindex.parsers.uibinder_parser: Extracted 8 form fields from InitiativeAdministrationDetailsWidget.ui.xml
2026-01-01 01:29:08 [WARNING] codeindex.services.frontend_analyzer: GWT UiBinder parser failed, falling back to LLM: 'name'
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: InitiativeAdministrationDetailsWidgetForm
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: Analyzing: EcardSectionPanel.ui.xml
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: No form found in EcardSectionPanel.ui.xml, skipping
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: Analyzing: validate.js
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: No form found in validate.js, skipping
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: Analyzing: WLANSchuleProductAndServicesWidget.ui.xml
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: No form found in WLANSchuleProductAndServicesWidget.ui.xml, skipping
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: Analyzing: BillingsPortletView.ui.xml
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: No form found in BillingsPortletView.ui.xml, skipping
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: Analyzing: FixedLineSectionPanel.ui.xml
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: No form found in FixedLineSectionPanel.ui.xml, skipping
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: Analyzing: FixedLineSectionPanel.ui.xml
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: No form found in FixedLineSectionPanel.ui.xml, skipping
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: Analyzing: ContentView.ui.xml
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: No form found in ContentView.ui.xml, skipping
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyToDoNotesView.java
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: No form found in MyToDoNotesView.java, skipping
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: Analyzing: PastPortletView.java
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: No form found in PastPortletView.java, skipping
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:29:39 [INFO] codeindex.services.frontend_analyzer: Analyzing: acronym.htm
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: fullpage_form
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: UserAdminSegmentView.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in UserAdminSegmentView.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: TurnoverView.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in TurnoverView.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: ServiceNetzSchuleSectionPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in ServiceNetzSchuleSectionPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: TableViewInsuranceBrokerPopup.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in TableViewInsuranceBrokerPopup.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: template.htm
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in template.htm, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: FlashDataView.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in FlashDataView.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: CloudCommunicationSectionPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in CloudCommunicationSectionPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionSectionPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionSectionPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionSectionPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionSectionPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: Produktnutzung.html
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in Produktnutzung.html, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: advlink.js
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in advlink.js, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: TypeView.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in TypeView.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: OanCostsPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in OanCostsPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: CustomerDataPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in CustomerDataPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: InteractionDetailView.java
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in InteractionDetailView.java, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: OanSectionPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in OanSectionPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: example.html
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in example.html, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberCostsPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberCostsPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyToDoNotesView.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in MyToDoNotesView.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductAndServicesWidget.java
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in ProductAndServicesWidget.java, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketingProductListItemWidget.java
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in MarketingProductListItemWidget.java, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: Release Notes.html
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in Release Notes.html, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: Allgemein.html
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in Allgemein.html, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketplaceGroupCostsPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in MarketplaceGroupCostsPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: ContactPersonsGridWidget.java
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in ContactPersonsGridWidget.java, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: HardwareCostsPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in HardwareCostsPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: DaasMarketingProductListItemWidget.java
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in DaasMarketingProductListItemWidget.java, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: ImageDetailsWidget.java
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in ImageDetailsWidget.java, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: TurnoverRangeView.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in TurnoverRangeView.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: DaaSMarketingProductListItemWidget.java
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in DaaSMarketingProductListItemWidget.java, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: A1dameApothekeSectionPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in A1dameApothekeSectionPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: Interaktionen.html
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in Interaktionen.html, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: acronym.js
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in acronym.js, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesInfoPopup.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in SalesInfoPopup.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:30:06 [INFO] codeindex.services.frontend_analyzer: Analyzing: image.htm
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: style_form
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductOverviewConfigurationView.java
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in ProductOverviewConfigurationView.java, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberEditPanel.ui.xml
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberEditPanel.ui.xml, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferDetailsView.ui.xml
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferDetailsView.ui.xml, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: OanCostsPanel.ui.xml
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in OanCostsPanel.ui.xml, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: ContactPersonsGridWidget.ui.xml
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in ContactPersonsGridWidget.ui.xml, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: ContactEditPanel.ui.xml
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in ContactEditPanel.ui.xml, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: ContactEditPanel.ui.xml
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in ContactEditPanel.ui.xml, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: ConfigureTurnoverRangesView.ui.xml
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in ConfigureTurnoverRangesView.ui.xml, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberEditPanel.ui.xml
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberEditPanel.ui.xml, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: InternetSectionPanel.ui.xml
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in InternetSectionPanel.ui.xml, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: FixedLineSectionPanel.ui.xml
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in FixedLineSectionPanel.ui.xml, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: GamificationPanel.ui.xml
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in GamificationPanel.ui.xml, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: EquipmentSectionPanel.ui.xml
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in EquipmentSectionPanel.ui.xml, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductSectionPanel.ui.xml
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in ProductSectionPanel.ui.xml, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: TerminalTypeConfigurationPanel.ui.xml
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in TerminalTypeConfigurationPanel.ui.xml, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:31:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: attributes.htm
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: row_form
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: ShowProductHistoryView.java
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in ShowProductHistoryView.java, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberCostsPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberCostsPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: NoteHistoryView.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in NoteHistoryView.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_template.js
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in editor_template.js, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: Kundennotizen.html
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in Kundennotizen.html, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: LinksPortletView.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in LinksPortletView.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: about.js
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in about.js, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketingProductWidget.java
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in MarketingProductWidget.java, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: Anzeige_mehrerer_Kunden_im_CuCo.html
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in Anzeige_mehrerer_Kunden_im_CuCo.html, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: TariffAndBundleSectionPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in TariffAndBundleSectionPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: AllNotesView.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in AllNotesView.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: color_picker.js
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in color_picker.js, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: GwtSelectRolesDialog.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in GwtSelectRolesDialog.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: Tabellenansicht.html
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in Tabellenansicht.html, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: OrgStructView.java
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in OrgStructView.java, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: AbstractPortlet.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in AbstractPortlet.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: BillingsWidgetView.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in BillingsWidgetView.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberCostsPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberCostsPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: IPVoiceSectionPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in IPVoiceSectionPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: TableViewPriceView.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in TableViewPriceView.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: embed.js
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in embed.js, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditUnknownAreasCodeDialog.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in EditUnknownAreasCodeDialog.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: BillingCycleView.java
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in BillingCycleView.java, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: WaitingWidget.java
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in WaitingWidget.java, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: DaasMarketingProductListItemWidget.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in DaasMarketingProductListItemWidget.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: charmap.htm
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in charmap.htm, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberEditPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberEditPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: ReminderDateTimeBox.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in ReminderDateTimeBox.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: acronym.js
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in acronym.js, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductAdministrationPortletView.java
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in ProductAdministrationPortletView.java, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: MultiSelectorPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in MultiSelectorPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: pkb.html
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in pkb.html, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteListView.java
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteListView.java, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditBaseMarketingProductDialog.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in EditBaseMarketingProductDialog.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: IpVoiceCostsPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in IpVoiceCostsPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: IPVoiceSectionPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in IPVoiceSectionPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: SNGMobileAccessSectionPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in SNGMobileAccessSectionPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsPhysicalResourceNodeView.java
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsPhysicalResourceNodeView.java, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileCostsPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in MobileCostsPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionSectionPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionSectionPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: TvSectionPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in TvSectionPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: CctPrice.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in CctPrice.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteDropDownButton.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteDropDownButton.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:31:24 [INFO] codeindex.services.frontend_analyzer: Analyzing: merge_cells.htm
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: table_cell_form
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: unauthorized-pc-prod.html
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in unauthorized-pc-prod.html, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: LocationCostsPanel.ui.xml
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in LocationCostsPanel.ui.xml, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductSectionPanel.ui.xml
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in ProductSectionPanel.ui.xml, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessCasePortletView.java
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessCasePortletView.java, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: untrusted.html
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in untrusted.html, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: OptionalServicesSectionPanel.ui.xml
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in OptionalServicesSectionPanel.ui.xml, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionSectionPanel.ui.xml
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionSectionPanel.ui.xml, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: CASTCallbackView.ui.xml
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in CASTCallbackView.ui.xml, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: ExtendedNBOWidget.java
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in ExtendedNBOWidget.java, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobilePasswordView.java
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in MobilePasswordView.java, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: BIZKOSectionPanel.ui.xml
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in BIZKOSectionPanel.ui.xml, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: row.js
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in row.js, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: admin.html
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in admin.html, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: TabletProductSectionPanel.ui.xml
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in TabletProductSectionPanel.ui.xml, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditSupervisorList.ui.xml
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: No form found in EditSupervisorList.ui.xml, skipping
2026-01-01 01:31:29 [INFO] codeindex.services.frontend_analyzer: Analyzing: link.htm
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: del_form
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: GamificationWidget.ui.xml
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: No form found in GamificationWidget.ui.xml, skipping
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralView.java
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralView.java, skipping
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: NameValuePairView.java
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: No form found in NameValuePairView.java, skipping
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: WLANSchuleSectionPanel.ui.xml
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: No form found in WLANSchuleSectionPanel.ui.xml, skipping
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: TasksPanel.ui.xml
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: No form found in TasksPanel.ui.xml, skipping
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsAccountNodeView.java
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsAccountNodeView.java, skipping
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: RoleSelectionView.java
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: No form found in RoleSelectionView.java, skipping
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: ToDoPanel.ui.xml
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: No form found in ToDoPanel.ui.xml, skipping
2026-01-01 01:31:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: searchreplace.htm
2026-01-01 01:31:57 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: source
2026-01-01 01:31:57 [INFO] codeindex.services.frontend_analyzer: Analyzing: link.htm
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: AdvHRDialogForm
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: FixedLineSectionPanel.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in FixedLineSectionPanel.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketplaceCostsPanel.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in MarketplaceCostsPanel.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: attributes.js
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in attributes.js, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileTariffPanel.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in MobileTariffPanel.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyRemindersView.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in MyRemindersView.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: FeedbackReflectionPanel.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in FeedbackReflectionPanel.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketplaceGroupCostsPanel.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in MarketplaceGroupCostsPanel.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: Produktbrowser.html
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in Produktbrowser.html, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: PartyBarView.java
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in PartyBarView.java, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: BPBSectionPanel.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in BPBSectionPanel.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: ImageThumbnail.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in ImageThumbnail.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: GroupCostsPanel.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in GroupCostsPanel.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: AbstractSalesConvNoteView.java
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in AbstractSalesConvNoteView.java, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: Kundensuche.html
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in Kundensuche.html, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: NBOOverviewView.java
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in NBOOverviewView.java, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: ServiceNetzSchuleSectionPanel.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in ServiceNetzSchuleSectionPanel.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteValidationConfigurationPortletView.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteValidationConfigurationPortletView.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: GroupCostsPanel.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in GroupCostsPanel.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:32:13 [INFO] codeindex.services.frontend_analyzer: Analyzing: dialog.htm
2026-01-01 01:33:08 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:33:08 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:33:08 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:33:08 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: merge_cells_form
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesInfoReportingPortletView.java
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in SalesInfoReportingPortletView.java, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: IPVoiceSectionPanel.ui.xml
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in IPVoiceSectionPanel.ui.xml, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsSAPPhysicalResourceNodeView.java
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsSAPPhysicalResourceNodeView.java, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: GwtSelectTeamMemberDialog.ui.xml
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in GwtSelectTeamMemberDialog.ui.xml, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: dialog.js
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in dialog.js, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionEditPanel.ui.xml
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionEditPanel.ui.xml, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: TurnoverView.java
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in TurnoverView.java, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuotePanel.ui.xml
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in QuotePanel.ui.xml, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: embed.js
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in embed.js, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferInteractionsView.ui.xml
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferInteractionsView.ui.xml, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: BillingsPortletView.java
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in BillingsPortletView.java, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsPartyNodeView.ui.xml
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsPartyNodeView.ui.xml, skipping
2026-01-01 01:33:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: link.htm
2026-01-01 01:33:39 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:33:39 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:34:06 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:34:06 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: link_form
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: ContentView.java
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in ContentView.java, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: Portlet.html
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in Portlet.html, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: Beispiel6.htm
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in Beispiel6.htm, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: InternetTVSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in InternetTVSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: PriceEditPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in PriceEditPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: InitiativeAdministrationComponent.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in InitiativeAdministrationComponent.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: Stammblatt.html
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in Stammblatt.html, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: merge_cells.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in merge_cells.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessInternetSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessInternetSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SNGGemeindeamtSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in SNGGemeindeamtSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: NoInterestView.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in NoInterestView.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: OanSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in OanSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: about.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in about.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileCostsPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in MobileCostsPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileCostsPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in MobileCostsPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: IpVoiceCostsPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in IpVoiceCostsPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SBSNoteView.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in SBSNoteView.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesInfoAdministrationPortletView.java
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in SalesInfoAdministrationPortletView.java, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: DigitalSellingNoteView.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in DigitalSellingNoteView.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: BPBSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in BPBSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsSAPProductNodeView.java
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsSAPProductNodeView.java, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: template.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in template.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: ImageUploadWidget.java
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in ImageUploadWidget.java, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: IPVoiceSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in IPVoiceSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: emotions.htm
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in emotions.htm, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: A1dameArztSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in A1dameArztSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: PosEditView.java
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in PosEditView.java, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: BIPSectionPanel.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in BIPSectionPanel.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: CreateNonCustomerContactView.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in CreateNonCustomerContactView.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: PartnerCenterUserDetailsPopup.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in PartnerCenterUserDetailsPopup.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: AbstractVisitReportView.java
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in AbstractVisitReportView.java, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: TouchpointView.ui.xml
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: No form found in TouchpointView.ui.xml, skipping
2026-01-01 01:34:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: abbr.htm
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: searchreplace_form
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: Auftragsabwicklung.html
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: No form found in Auftragsabwicklung.html, skipping
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: cell.js
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: No form found in cell.js, skipping
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyFlashInfosView.java
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: No form found in MyFlashInfosView.java, skipping
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: SipTrunkSectionPanel.ui.xml
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: No form found in SipTrunkSectionPanel.ui.xml, skipping
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: Navigationsmenue.html
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: No form found in Navigationsmenue.html, skipping
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: Produktuebersicht.html
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: No form found in Produktuebersicht.html, skipping
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: de.js
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: No form found in de.js, skipping
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: HardwareSectionPanel.ui.xml
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: No form found in HardwareSectionPanel.ui.xml, skipping
2026-01-01 01:34:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: pastetext.htm
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: link_form
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: FeedbackReflectionPanel.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in FeedbackReflectionPanel.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: preview.html
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in preview.html, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: HardwareSectionPanel.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in HardwareSectionPanel.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferOverviewView.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferOverviewView.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: SNGAuenstelleSectionPanel.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in SNGAuenstelleSectionPanel.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferNotesView.java
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferNotesView.java, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: InventoryProductGroupView.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in InventoryProductGroupView.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: GucciNBODetailView.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in GucciNBODetailView.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferMobileView.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferMobileView.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: SNGGemeindeamtSectionPanel.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in SNGGemeindeamtSectionPanel.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: InitiativeAdministrationDetailsComponent.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in InitiativeAdministrationDetailsComponent.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketplaceCostsPanel.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in MarketplaceCostsPanel.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductAndServicesWidget.java
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in ProductAndServicesWidget.java, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: AuthorityAdministrationComponent.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in AuthorityAdministrationComponent.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferCustomerFeedbackView.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferCustomerFeedbackView.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: MainView.java
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in MainView.java, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: TvSectionPanel.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in TvSectionPanel.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: AssignToDoPanel.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in AssignToDoPanel.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: cite.js
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in cite.js, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionSectionPanel.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionSectionPanel.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: tiny_mce.js
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in tiny_mce.js, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: InternetSpeedPanel.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in InternetSpeedPanel.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: PhoneNumberListView.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in PhoneNumberListView.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: PartyWidget.java
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in PartyWidget.java, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: blank.htm
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in blank.htm, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesConvReportingPortletView.java
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in SalesConvReportingPortletView.java, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: ApothekennetzSectionPanel.ui.xml
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: No form found in ApothekennetzSectionPanel.ui.xml, skipping
2026-01-01 01:34:49 [INFO] codeindex.services.frontend_analyzer: Analyzing: image.htm
2026-01-01 01:35:09 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:35:09 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:36:13 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:36:13 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:36:52 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: cite_form
2026-01-01 01:36:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessFirewallSectionPanel.ui.xml
2026-01-01 01:36:52 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessFirewallSectionPanel.ui.xml, skipping
2026-01-01 01:36:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: OanCostsPanel.ui.xml
2026-01-01 01:36:52 [INFO] codeindex.services.frontend_analyzer: No form found in OanCostsPanel.ui.xml, skipping
2026-01-01 01:36:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: abbr.htm
2026-01-01 01:37:09 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:37:09 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:37:34 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:37:34 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:37:40 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:37:40 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:38:07 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:38:07 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: source
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: InternetSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in InternetSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: BPBSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in BPBSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: IpVoiceCostsPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in IpVoiceCostsPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileCostsPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in MobileCostsPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: A1dameArztSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in A1dameArztSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: GwtEditMessageDialog.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in GwtEditMessageDialog.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_template_src.js
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in editor_template_src.js, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferAdministrationComponent.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in OfferAdministrationComponent.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferCouponsView.java
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferCouponsView.java, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: IPVoiceSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in IPVoiceSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: FIBSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in FIBSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: HostedCommunicationServiceSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in HostedCommunicationServiceSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketingProductListItemWidget.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in MarketingProductListItemWidget.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsDefaultProductNodeView.java
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsDefaultProductNodeView.java, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessInternetProfessionalView.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessInternetProfessionalView.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in ProductSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyCuCoMainView.java
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in MyCuCoMainView.java, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteOverviewView.java
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteOverviewView.java, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: LastOfferInteractionsWidget.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in LastOfferInteractionsWidget.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: en.js
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in en.js, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: template.js
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in template.js, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessGlasfaserInternetSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessGlasfaserInternetSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: InternetSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in InternetSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: table.js
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in table.js, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferBusinessView.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferBusinessView.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionEditPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionEditPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionEditPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionEditPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: less.js
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in less.js, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: HostedCommunicationServiceSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in HostedCommunicationServiceSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessInternetSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessInternetSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: IpVoiceCostsPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in IpVoiceCostsPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: Einleitung.html
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in Einleitung.html, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: GwtEditServiceDialog.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in GwtEditServiceDialog.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: pasteword.js
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in pasteword.js, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: BillingAddressPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in BillingAddressPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: FixedLineSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in FixedLineSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: IPVoiceSectionPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in IPVoiceSectionPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileCostsPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in MobileCostsPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: UsageDataView.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in UsageDataView.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: SecurityPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in SecurityPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesInfoAdministrationPortletView.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in SalesInfoAdministrationPortletView.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: PosEditView.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in PosEditView.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberCostsPanel.ui.xml
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberCostsPanel.ui.xml, skipping
2026-01-01 01:38:14 [INFO] codeindex.services.frontend_analyzer: Analyzing: pasteword.htm
2026-01-01 01:38:19 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:38:19 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:38:49 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:38:49 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:39:10 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:39:10 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:40:14 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:40:14 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: abbr_form
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: EcardSectionPanel.ui.xml
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: No form found in EcardSectionPanel.ui.xml, skipping
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberCostsPanel.ui.xml
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberCostsPanel.ui.xml, skipping
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: CouponSeriesAdministrationView.java
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: No form found in CouponSeriesAdministrationView.java, skipping
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductSectionPanel.ui.xml
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: No form found in ProductSectionPanel.ui.xml, skipping
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessInternetProfessionalView.java
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessInternetProfessionalView.java, skipping
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: InteractionDetailView.ui.xml
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: No form found in InteractionDetailView.ui.xml, skipping
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductBrowserView.java
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: No form found in ProductBrowserView.java, skipping
2026-01-01 01:40:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: link.htm
2026-01-01 01:41:11 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:41:11 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 01:41:11 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/pkb.ui/src/main/resources/at/a1ta/pkb/ui/client/portlet/offer/InitiativeAdministrationDetailsWidget.ui.xml: Ollama request timed out: timed out
2026-01-01 01:41:11 [INFO] codeindex.services.frontend_analyzer: Analyzing: media.htm
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: source
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: InternetSectionPanel.ui.xml
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in InternetSectionPanel.ui.xml, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: searchreplace.js
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in searchreplace.js, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: InternetSectionPanel.ui.xml
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in InternetSectionPanel.ui.xml, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: Angebote.html
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in Angebote.html, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: UITextsEditorPortletView.ui.xml
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in UITextsEditorPortletView.ui.xml, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: MusicPanel.ui.xml
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in MusicPanel.ui.xml, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyBindingsDetailsView.java
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in MyBindingsDetailsView.java, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: CctSwitchDiscountBox.ui.xml
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in CctSwitchDiscountBox.ui.xml, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: tiny_mce_popup.js
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in tiny_mce_popup.js, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: SurchargePriceConfigView.ui.xml
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in SurchargePriceConfigView.ui.xml, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberEditPanel.ui.xml
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberEditPanel.ui.xml, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: TableViewPriceView.java
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in TableViewPriceView.java, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: WLANSchuleSectionPanel.ui.xml
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in WLANSchuleSectionPanel.ui.xml, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: FlashAdministrationView.java
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in FlashAdministrationView.java, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: cell.js
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: No form found in cell.js, skipping
2026-01-01 01:41:33 [INFO] codeindex.services.frontend_analyzer: Analyzing: color_picker.htm
2026-01-01 01:41:35 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:41:35 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:41:42 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:41:42 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 01:41:42 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-common/src/main/resources/at/a1ta/cuco/ui/common/public/tiny_mce/plugins/xhtmlxtras/acronym.htm: Ollama request timed out: timed out
2026-01-01 01:41:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:41:42 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:41:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: template.htm
2026-01-01 01:42:09 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:42:09 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 01:42:09 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-common/src/main/resources/at/a1ta/cuco/ui/common/public/tiny_mce/plugins/advimage/image.htm: Ollama request timed out: timed out
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: NBOPortletView.ui.xml
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: No form found in NBOPortletView.ui.xml, skipping
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: HostedCommunicationServiceSectionPanel.ui.xml
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: No form found in HostedCommunicationServiceSectionPanel.ui.xml, skipping
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyBindingsView.java
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: No form found in MyBindingsView.java, skipping
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: OanSectionPanel.ui.xml
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: No form found in OanSectionPanel.ui.xml, skipping
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: Die_Kundensuche_im_Suchformular.html
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: No form found in Die_Kundensuche_im_Suchformular.html, skipping
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesInfoNoteHistoryView.ui.xml
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: No form found in SalesInfoNoteHistoryView.ui.xml, skipping
2026-01-01 01:42:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: media.htm
2026-01-01 01:42:20 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:42:20 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: example_dialog_form
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionEditPanel.ui.xml
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionEditPanel.ui.xml, skipping
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteListView.ui.xml
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteListView.ui.xml, skipping
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditPdfMetadataWidget.ui.xml
2026-01-01 01:42:43 [INFO] codeindex.services.frontend_analyzer: Using GWT UiBinder parser for EditPdfMetadataWidget.ui.xml
2026-01-01 01:42:43 [INFO] codeindex.parsers.uibinder_parser: Extracted 4 form fields from EditPdfMetadataWidget.ui.xml
2026-01-01 01:42:43 [WARNING] codeindex.services.frontend_analyzer: GWT UiBinder parser failed, falling back to LLM: 'name'
2026-01-01 01:42:50 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:42:50 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:43:12 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:43:12 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 01:43:12 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/xhtmlxtras/attributes.htm: Ollama request timed out: timed out
2026-01-01 01:43:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: validate.js
2026-01-01 01:43:12 [INFO] codeindex.services.frontend_analyzer: No form found in validate.js, skipping
2026-01-01 01:43:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteComponentBase.ui.xml
2026-01-01 01:43:12 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteComponentBase.ui.xml, skipping
2026-01-01 01:43:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: FIBSectionPanel.ui.xml
2026-01-01 01:43:12 [INFO] codeindex.services.frontend_analyzer: No form found in FIBSectionPanel.ui.xml, skipping
2026-01-01 01:43:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: en.js
2026-01-01 01:43:12 [INFO] codeindex.services.frontend_analyzer: No form found in en.js, skipping
2026-01-01 01:43:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberCostsPanel.ui.xml
2026-01-01 01:43:12 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberCostsPanel.ui.xml, skipping
2026-01-01 01:43:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: attributes.htm
2026-01-01 01:43:27 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: colorpicker_form
2026-01-01 01:43:27 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:43:27 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:43:27 [INFO] codeindex.services.frontend_analyzer: Analyzing: NoteEditView.ui.xml
2026-01-01 01:43:27 [INFO] codeindex.services.frontend_analyzer: No form found in NoteEditView.ui.xml, skipping
2026-01-01 01:43:27 [INFO] codeindex.services.frontend_analyzer: Analyzing: FIBSectionPanel.ui.xml
2026-01-01 01:43:27 [INFO] codeindex.services.frontend_analyzer: No form found in FIBSectionPanel.ui.xml, skipping
2026-01-01 01:43:27 [INFO] codeindex.services.frontend_analyzer: Analyzing: NewContactPersonPortletView.java
2026-01-01 01:43:27 [INFO] codeindex.services.frontend_analyzer: No form found in NewContactPersonPortletView.java, skipping
2026-01-01 01:43:27 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyCustomersDetailsView.ui.xml
2026-01-01 01:43:27 [INFO] codeindex.services.frontend_analyzer: No form found in MyCustomersDetailsView.ui.xml, skipping
2026-01-01 01:43:27 [INFO] codeindex.services.frontend_analyzer: Analyzing: SNGGemeindeamtSectionPanel.ui.xml
2026-01-01 01:43:27 [INFO] codeindex.services.frontend_analyzer: No form found in SNGGemeindeamtSectionPanel.ui.xml, skipping
2026-01-01 01:43:27 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralPanel.ui.xml
2026-01-01 01:43:27 [INFO] codeindex.services.frontend_analyzer: Using GWT UiBinder parser for GeneralPanel.ui.xml
2026-01-01 01:43:27 [INFO] codeindex.parsers.uibinder_parser: Extracted 11 form fields from GeneralPanel.ui.xml
2026-01-01 01:43:27 [WARNING] codeindex.services.frontend_analyzer: GWT UiBinder parser failed, falling back to LLM: 'name'
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: template_form
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: Vertriebsaktivitaeten.html
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in Vertriebsaktivitaeten.html, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: NewSalesInfoView.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in NewSalesInfoView.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: rule.js
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in rule.js, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsLocationNodeView.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsLocationNodeView.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditSBSProductsConfigurationView.java
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in EditSBSProductsConfigurationView.java, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: EmailSectionPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in EmailSectionPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: pastetext.js
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in pastetext.js, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyOpportunitiesView.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in MyOpportunitiesView.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: PartyDataDetailsView.java
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in PartyDataDetailsView.java, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesInfoNoteHistoryView.java
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in SalesInfoNoteHistoryView.java, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductAndServicesWidget.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in ProductAndServicesWidget.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: FixedLineSectionPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in FixedLineSectionPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: form_utils.js
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in form_utils.js, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: A1VoipHardwareWidget.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in A1VoipHardwareWidget.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: IpVoiceCostsPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in IpVoiceCostsPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberCostsPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberCostsPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: del.js
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in del.js, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditStandorte.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in EditStandorte.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsLocationNodeView.java
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsLocationNodeView.java, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: rule.js
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in rule.js, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: example.html
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in example.html, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: mycuco.html
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in mycuco.html, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: TvSectionPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in TvSectionPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: VipPortletView.java
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in VipPortletView.java, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyCuCoHeaderInfoView.java
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in MyCuCoHeaderInfoView.java, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: SurchargePriceConfigView.java
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in SurchargePriceConfigView.java, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: CctSelectorPricePanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in CctSelectorPricePanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductBrowserTableFilter.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in ProductBrowserTableFilter.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketplaceCostsPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in MarketplaceCostsPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileCostsPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in MobileCostsPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: DigitalSellingNoteHistoryView.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in DigitalSellingNoteHistoryView.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditRoleGroupManagementDialog.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in EditRoleGroupManagementDialog.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: ContactPersonEditPanel.ui.xml
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in ContactPersonEditPanel.ui.xml, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:43:45 [INFO] codeindex.services.frontend_analyzer: Analyzing: table.htm
2026-01-01 01:44:34 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:44:34 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: media_form
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: DigitalSellingNoteView.java
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in DigitalSellingNoteView.java, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: NBOList.ui.xml
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in NBOList.ui.xml, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: Produktnutzungsdaten.html
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in Produktnutzungsdaten.html, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: ServiceNetzSchuleSectionPanel.ui.xml
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in ServiceNetzSchuleSectionPanel.ui.xml, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: FlashInfoEditView.java
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in FlashInfoEditView.java, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: FreeUnitsView.ui.xml
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in FreeUnitsView.ui.xml, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: TvSectionPanel.ui.xml
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in TvSectionPanel.ui.xml, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: blank.htm
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in blank.htm, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileCostsPanel.ui.xml
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in MobileCostsPanel.ui.xml, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: ServiceNetzSchuleSectionPanel.ui.xml
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in ServiceNetzSchuleSectionPanel.ui.xml, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: anchor.js
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in anchor.js, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: WLANSchuleProductAndServicesWidget.ui.xml
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in WLANSchuleProductAndServicesWidget.ui.xml, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: OpportunityWidget.java
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in OpportunityWidget.java, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: TariffAndBundleSectionPanel.ui.xml
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in TariffAndBundleSectionPanel.ui.xml, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessInternetSectionPanel.ui.xml
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessInternetSectionPanel.ui.xml, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:44:54 [INFO] codeindex.services.frontend_analyzer: Analyzing: anchor.htm
2026-01-01 01:45:31 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: EditPdfMetadataWidgetForm
2026-01-01 01:45:31 [INFO] codeindex.services.frontend_analyzer: Analyzing: TariffAndBundleSectionPanel.ui.xml
2026-01-01 01:45:31 [INFO] codeindex.services.frontend_analyzer: No form found in TariffAndBundleSectionPanel.ui.xml, skipping
2026-01-01 01:45:31 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketplaceCostsPanel.ui.xml
2026-01-01 01:45:31 [INFO] codeindex.services.frontend_analyzer: No form found in MarketplaceCostsPanel.ui.xml, skipping
2026-01-01 01:45:31 [INFO] codeindex.services.frontend_analyzer: Analyzing: cite.htm
2026-01-01 01:45:37 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:45:37 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 01:45:37 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advlink/link.htm: Ollama request timed out: timed out
2026-01-01 01:45:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductAndServicesWidget.java
2026-01-01 01:45:37 [INFO] codeindex.services.frontend_analyzer: No form found in ProductAndServicesWidget.java, skipping
2026-01-01 01:45:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:45:37 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:45:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: searchreplace.htm
2026-01-01 01:46:09 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:46:09 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:46:22 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:46:22 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 01:46:22 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/xhtmlxtras/abbr.htm: Ollama request timed out: timed out
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: IpVoiceCostsPanel.ui.xml
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in IpVoiceCostsPanel.ui.xml, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: ApothekennetzSectionPanel.ui.xml
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in ApothekennetzSectionPanel.ui.xml, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: TextWidget.java
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in TextWidget.java, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: TransactionFeesPanel.ui.xml
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in TransactionFeesPanel.ui.xml, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileCostsPanel.ui.xml
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in MobileCostsPanel.ui.xml, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: FilterView.java
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in FilterView.java, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionEditPanel.ui.xml
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionEditPanel.ui.xml, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: ImageDetailsWidget.ui.xml
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in ImageDetailsWidget.ui.xml, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteFlashInfoEditView.java
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteFlashInfoEditView.java, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_template.js
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in editor_template.js, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: GroupCostsPanel.ui.xml
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in GroupCostsPanel.ui.xml, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: ApothekennetzSectionPanel.ui.xml
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in ApothekennetzSectionPanel.ui.xml, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferCustomerFeedbackView.java
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferCustomerFeedbackView.java, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:46:22 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditPdfMetadataWidget.java
2026-01-01 01:46:52 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:46:52 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 01:46:52 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advimage/image.htm: Ollama request timed out: timed out
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: Produktubersicht.html
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in Produktubersicht.html, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: Vertriebsaktivitaeten.html
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in Vertriebsaktivitaeten.html, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: color_picker.js
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in color_picker.js, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: CreateNonCustomerContactView.java
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in CreateNonCustomerContactView.java, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: Portlet.html
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in Portlet.html, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: PaymentServiceSectionPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in PaymentServiceSectionPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferCouponsView.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferCouponsView.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: InternetSectionPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in InternetSectionPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsDefaultSubscriptionNodeView.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsDefaultSubscriptionNodeView.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: InventoryProductGroupView.java
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in InventoryProductGroupView.java, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessInternetSectionPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessInternetSectionPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: abbr.js
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in abbr.js, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: Navigationsleiste.html
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in Navigationsleiste.html, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: FixedLineSectionPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in FixedLineSectionPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: OanCostsPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in OanCostsPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: TvSectionPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in TvSectionPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: HostedCommunicationServiceSectionPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in HostedCommunicationServiceSectionPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberCostsPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberCostsPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: EmailSectionPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in EmailSectionPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsDefaultSubscriptionNodeView.java
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsDefaultSubscriptionNodeView.java, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: RestrictedPartyDataPortletView.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in RestrictedPartyDataPortletView.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: CctQuantityWithCustomPriceBox.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in CctQuantityWithCustomPriceBox.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: Beispiel4.htm
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in Beispiel4.htm, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: TvSectionPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in TvSectionPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: ConfigureTurnoverRangesView.java
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in ConfigureTurnoverRangesView.java, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferView.java
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferView.java, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesConvNoteView.java
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in SalesConvNoteView.java, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: SNGMobileAccessSectionPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in SNGMobileAccessSectionPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: HardwareCostsPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in HardwareCostsPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketingProductWidget.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in MarketingProductWidget.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: CollateralOfferAssignmentComponent.ui.xml
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in CollateralOfferAssignmentComponent.ui.xml, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: NewSalesInfoView.java
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: No form found in NewSalesInfoView.java, skipping
2026-01-01 01:46:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: fullscreen.htm
2026-01-01 01:47:12 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:47:12 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:47:27 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:47:27 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: AnchorForm
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: attributes.js
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: No form found in attributes.js, skipping
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: Rechnungsinformationen.html
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: No form found in Rechnungsinformationen.html, skipping
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_template.js
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: No form found in editor_template.js, skipping
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionEditPanel.ui.xml
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionEditPanel.ui.xml, skipping
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: unauthorized-pc-int.html
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: No form found in unauthorized-pc-int.html, skipping
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketplaceGroupCostsPanel.ui.xml
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: No form found in MarketplaceGroupCostsPanel.ui.xml, skipping
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: FixedLineSectionPanel.ui.xml
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: No form found in FixedLineSectionPanel.ui.xml, skipping
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileCostsPanel.ui.xml
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: No form found in MobileCostsPanel.ui.xml, skipping
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: PaymentServiceSectionPanel.ui.xml
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: No form found in PaymentServiceSectionPanel.ui.xml, skipping
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: AlleStandort.html
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: No form found in AlleStandort.html, skipping
2026-01-01 01:47:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: cell.htm
2026-01-01 01:47:45 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:47:45 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:48:35 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:48:35 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: searchreplace_form
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: BIZKOSectionPanel.ui.xml
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in BIZKOSectionPanel.ui.xml, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberCostsPanel.ui.xml
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberCostsPanel.ui.xml, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: A1dameArztSectionPanel.ui.xml
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in A1dameArztSectionPanel.ui.xml, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: CollateralOfferTimeLineWidget.java
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in CollateralOfferTimeLineWidget.java, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: charmap.js
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in charmap.js, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: ServicesPanel.ui.xml
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in ServicesPanel.ui.xml, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: lead.html
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in lead.html, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyBindingsDetailsView.ui.xml
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in MyBindingsDetailsView.ui.xml, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyCustomersView.ui.xml
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in MyCustomersView.ui.xml, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: FixedLineSectionPanel.ui.xml
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in FixedLineSectionPanel.ui.xml, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: link.js
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in link.js, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: standard.js
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in standard.js, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketingProductView.ui.xml
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in MarketingProductView.ui.xml, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: PaymentPanel.ui.xml
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: No form found in PaymentPanel.ui.xml, skipping
2026-01-01 01:48:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: row.htm
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: fullscreen_form
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: Inhalt.html
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in Inhalt.html, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductAndServicesWidget.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in ProductAndServicesWidget.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberEditPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberEditPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: Beispiel1.htm
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in Beispiel1.htm, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: FreeUnitsView.java
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in FreeUnitsView.java, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketplaceGroupCostsPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in MarketplaceGroupCostsPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: BankAccountPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in BankAccountPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: OanSectionPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in OanSectionPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyCustomersView.java
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in MyCustomersView.java, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: Einleitung.html
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in Einleitung.html, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: SBSNoteView.java
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in SBSNoteView.java, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditStandorte.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in EditStandorte.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: LastOfferInteractionsWidget.java
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in LastOfferInteractionsWidget.java, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessCasePortletView.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessCasePortletView.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: abbr.js
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in abbr.js, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: ConfigurableListSelectorRuntimeConfigurationDialog.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in ConfigurableListSelectorRuntimeConfigurationDialog.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: Informationen.html
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in Informationen.html, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: GenericNoteView.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in GenericNoteView.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: SEG.html
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in SEG.html, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: image.js
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in image.js, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: TouchpointView.java
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in TouchpointView.java, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: CASTCallbackView.java
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in CASTCallbackView.java, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: BIZKOSectionPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in BIZKOSectionPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: BPBSectionPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in BPBSectionPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: OpportunityWidget.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in OpportunityWidget.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteDropDownButton.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteDropDownButton.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: PriceInputBox.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in PriceInputBox.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: VipHistoryPortletView.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in VipHistoryPortletView.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: PartyDropDownButton.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in PartyDropDownButton.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: element_common.js
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in element_common.js, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionEditPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionEditPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: SmartHomePanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in SmartHomePanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: VipPortletView.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in VipPortletView.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: IPVoiceSectionPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in IPVoiceSectionPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: NewProductHistoryView.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in NewProductHistoryView.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: ImageUploadWidget.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in ImageUploadWidget.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: NBOWidget.java
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in NBOWidget.java, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: HardwareSectionPanel.ui.xml
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in HardwareSectionPanel.ui.xml, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyOpportunitiesView.java
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: No form found in MyOpportunitiesView.java, skipping
2026-01-01 01:49:09 [INFO] codeindex.services.frontend_analyzer: Analyzing: props.htm
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: EditPdfMetadataWidgetForm
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: AttributeView.java
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in AttributeView.java, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketplaceGroupCostsPanel.ui.xml
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in MarketplaceGroupCostsPanel.ui.xml, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: template.htm
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in template.htm, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductSectionPanel.ui.xml
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in ProductSectionPanel.ui.xml, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: NBO.html
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in NBO.html, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralView.ui.xml
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralView.ui.xml, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: tiny_mce_src.js
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in tiny_mce_src.js, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: embed.js
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in embed.js, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: searchreplace.js
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in searchreplace.js, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: PhoneNumberListView.java
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in PhoneNumberListView.java, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:49:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: ins.htm
2026-01-01 01:49:31 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:49:31 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:50:10 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:50:10 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: GeneralPanelForm
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: row.js
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in row.js, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditableListBox.ui.xml
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in EditableListBox.ui.xml, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: Welcome.html
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in Welcome.html, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: about.htm
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in about.htm, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: emotions.htm
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in emotions.htm, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: DaasProductWidget.java
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in DaasProductWidget.java, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: IPVoiceSectionPanel.ui.xml
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in IPVoiceSectionPanel.ui.xml, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductAndServicesWidget.ui.xml
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in ProductAndServicesWidget.ui.xml, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesInfoOverviewView.java
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in SalesInfoOverviewView.java, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: SelectImageComponent.ui.xml
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in SelectImageComponent.ui.xml, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: form_utils.js
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in form_utils.js, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferAdministrationDetailsComponent.ui.xml
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in OfferAdministrationDetailsComponent.ui.xml, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: en.js
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in en.js, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:50:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: table.htm
2026-01-01 01:51:13 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:51:13 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:51:35 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:51:35 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:51:46 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:51:46 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:52:37 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:52:37 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 01:52:37 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-common/src/main/resources/at/a1ta/cuco/ui/common/public/tiny_mce/plugins/advlink/link.htm: Ollama request timed out: timed out
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: SNGAuenstelleSectionPanel.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in SNGAuenstelleSectionPanel.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: ShowProductHistoryView.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in ShowProductHistoryView.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: IpVoiceCostsPanel.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in IpVoiceCostsPanel.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: FIBSectionPanel.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in FIBSectionPanel.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: GwtIbatisPortletView.java
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in GwtIbatisPortletView.java, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesInfoReportingPortletView.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in SalesInfoReportingPortletView.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: FeedbackAdministrationComponent.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in FeedbackAdministrationComponent.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberEditPanel.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberEditPanel.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessGlasfaserInternetSectionPanel.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessGlasfaserInternetSectionPanel.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: table.js
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in table.js, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: FIBSectionPanel.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in FIBSectionPanel.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: SearchResultWidgetView.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in SearchResultWidgetView.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberCostsPanel.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberCostsPanel.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: FlashAdministrationView.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in FlashAdministrationView.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: Interaktionen.htm
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in Interaktionen.htm, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferView.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferView.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: IpVoiceCostsPanel.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in IpVoiceCostsPanel.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: fullpage.js
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in fullpage.js, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: InternetSectionPanel.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in InternetSectionPanel.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: TerminAndCommunicationPanel.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in TerminAndCommunicationPanel.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductAndServicesWidget.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in ProductAndServicesWidget.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: image.js
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: No form found in image.js, skipping
2026-01-01 01:52:37 [INFO] codeindex.services.frontend_analyzer: Analyzing: fullpage.htm
2026-01-01 01:52:52 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:52:52 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:53:09 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:53:09 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:53:15 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:53:15 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:53:32 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:53:32 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:54:12 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:54:12 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 01:54:12 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/media/media.htm: Ollama request timed out: timed out
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: en.js
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: No form found in en.js, skipping
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: SecuritySectionPanel.ui.xml
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: No form found in SecuritySectionPanel.ui.xml, skipping
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: VipSearchComponent.ui.xml
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: No form found in VipSearchComponent.ui.xml, skipping
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: en.js
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: No form found in en.js, skipping
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: AttachmentsPanel.ui.xml
2026-01-01 01:54:12 [INFO] codeindex.services.frontend_analyzer: Using GWT UiBinder parser for AttachmentsPanel.ui.xml
2026-01-01 01:54:12 [INFO] codeindex.parsers.uibinder_parser: Extracted 1 form fields from AttachmentsPanel.ui.xml
2026-01-01 01:54:12 [WARNING] codeindex.services.frontend_analyzer: GWT UiBinder parser failed, falling back to LLM: 'name'
2026-01-01 01:54:46 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:54:46 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:55:15 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:55:15 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 01:55:15 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-common/src/main/resources/at/a1ta/cuco/ui/common/public/tiny_mce/plugins/xhtmlxtras/attributes.htm: Ollama request timed out: timed out
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: source_editor.js
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: No form found in source_editor.js, skipping
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: TurnoverPortletView.ui.xml
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: No form found in TurnoverPortletView.ui.xml, skipping
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: SNGGemeindeamtSectionPanel.ui.xml
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: No form found in SNGGemeindeamtSectionPanel.ui.xml, skipping
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: ReportingWidget.java
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: No form found in ReportingWidget.java, skipping
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductAndServicesWidget.java
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: No form found in ProductAndServicesWidget.java, skipping
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: DaasProductWidget.ui.xml
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: No form found in DaasProductWidget.ui.xml, skipping
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: CctQuantitySelectorBox.ui.xml
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: No form found in CctQuantitySelectorBox.ui.xml, skipping
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: NewProductHistoryView.java
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: No form found in NewProductHistoryView.java, skipping
2026-01-01 01:55:15 [INFO] codeindex.services.frontend_analyzer: Analyzing: pasteword.htm
2026-01-01 01:55:35 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: table_cell_form
2026-01-01 01:55:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:55:35 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:55:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: NBOPortletView.java
2026-01-01 01:55:35 [INFO] codeindex.services.frontend_analyzer: No form found in NBOPortletView.java, skipping
2026-01-01 01:55:35 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferMobileView.java
2026-01-01 01:55:48 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:55:48 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 01:55:48 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-common/src/main/resources/at/a1ta/cuco/ui/common/public/tiny_mce/plugins/table/table.htm: Ollama request timed out: timed out
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsSAPProductNodeView.ui.xml
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsSAPProductNodeView.ui.xml, skipping
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketingProductView.java
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: No form found in MarketingProductView.java, skipping
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileCostsPanel.ui.xml
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: No form found in MobileCostsPanel.ui.xml, skipping
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: Analyzing: LocationView.ui.xml
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: No form found in LocationView.ui.xml, skipping
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: Analyzing: A1dameArztSectionPanel.ui.xml
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: No form found in A1dameArztSectionPanel.ui.xml, skipping
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductNotesPanel.ui.xml
2026-01-01 01:55:48 [INFO] codeindex.services.frontend_analyzer: Using GWT UiBinder parser for ProductNotesPanel.ui.xml
2026-01-01 01:55:48 [INFO] codeindex.parsers.uibinder_parser: Extracted 18 form fields from ProductNotesPanel.ui.xml
2026-01-01 01:55:48 [WARNING] codeindex.services.frontend_analyzer: GWT UiBinder parser failed, falling back to LLM: 'name'
2026-01-01 01:56:37 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:56:37 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:56:53 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:56:53 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:57:10 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:57:10 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:57:17 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:57:17 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: AttachmentsPanelForm
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberEditPanel.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberEditPanel.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesInfoAttributesView.java
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in SalesInfoAttributesView.java, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductSectionPanel.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in ProductSectionPanel.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: PastTicketView.java
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in PastTicketView.java, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessInternetSectionPanel.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessInternetSectionPanel.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionEditPanel.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionEditPanel.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: OanCostsPanel.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in OanCostsPanel.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessFirewallView.java
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessFirewallView.java, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: SearchView.java
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in SearchView.java, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: NBO-Uebersicht.html
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in NBO-Uebersicht.html, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteValidationConfigurationPortletView.java
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteValidationConfigurationPortletView.java, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: BillingCycleView.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in BillingCycleView.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: PartyBarView.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in PartyBarView.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: NBOLink.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in NBOLink.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductAdministrationPortletView.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in ProductAdministrationPortletView.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: ActivityDetailsView.java
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in ActivityDetailsView.java, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferNotesView.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferNotesView.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessFirewallSectionPanel.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessFirewallSectionPanel.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: SecuritySectionPanel.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in SecuritySectionPanel.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: CctSwitchPriceBox.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in CctSwitchPriceBox.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: EcardSectionPanel.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in EcardSectionPanel.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: en.js
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in en.js, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: Geschaeftsfaelle.html
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in Geschaeftsfaelle.html, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsSAPPhysicalResourceNodeView.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsSAPPhysicalResourceNodeView.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductSectionPanel.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in ProductSectionPanel.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: FlashInfoEditView.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in FlashInfoEditView.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: LabelValueWidget.ui.xml
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: No form found in LabelValueWidget.ui.xml, skipping
2026-01-01 01:57:23 [INFO] codeindex.services.frontend_analyzer: Analyzing: image.htm
2026-01-01 01:57:34 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:57:34 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 01:57:34 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-common/src/main/resources/at/a1ta/cuco/ui/common/public/tiny_mce/plugins/xhtmlxtras/cite.htm: Ollama request timed out: timed out
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductOverviewConfigurationView.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in ProductOverviewConfigurationView.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: NewContactPersonPortletView.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in NewContactPersonPortletView.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: OanSectionPanel.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in OanSectionPanel.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: CouponSeriesAdministrationView.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in CouponSeriesAdministrationView.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: GamificationWidget.java
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in GamificationWidget.java, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesInfoAttributesHistoryView.java
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in SalesInfoAttributesHistoryView.java, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductManageAdministrationPortletView.java
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in ProductManageAdministrationPortletView.java, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionSectionPanel.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionSectionPanel.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: BIZKOSectionPanel.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in BIZKOSectionPanel.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: Rollenkonzept.html
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in Rollenkonzept.html, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: ContactPersonPortletView.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in ContactPersonPortletView.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: element_common.js
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in element_common.js, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: ActivityDetailsView.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in ActivityDetailsView.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessInternetSectionPanel.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessInternetSectionPanel.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyCustomersDetailsView.java
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in MyCustomersDetailsView.java, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: Suchergebnis_zur_Kundensuche.html
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in Suchergebnis_zur_Kundensuche.html, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: RoleSelectionView.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in RoleSelectionView.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileCostsPanel.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in MobileCostsPanel.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: TvSectionPanel.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in TvSectionPanel.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: del.js
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in del.js, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyFlashInfosView.ui.xml
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in MyFlashInfosView.ui.xml, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferTimeLineWidget.java
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: No form found in OfferTimeLineWidget.java, skipping
2026-01-01 01:57:34 [INFO] codeindex.services.frontend_analyzer: Analyzing: image.htm
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: OfferedOfferMobileViewForm
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: IpVoiceCostsPanel.ui.xml
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in IpVoiceCostsPanel.ui.xml, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionSectionPanel.ui.xml
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionSectionPanel.ui.xml, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: CctQuantityPriceBox.ui.xml
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in CctQuantityPriceBox.ui.xml, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: CctSwitchBoxWithQuantityAndPrice.ui.xml
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in CctSwitchBoxWithQuantityAndPrice.ui.xml, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: CctEnumSelectorWithQuantityAndPrice.ui.xml
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in CctEnumSelectorWithQuantityAndPrice.ui.xml, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: AdminHeader.ui.xml
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in AdminHeader.ui.xml, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: A1dameApothekeSectionPanel.ui.xml
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in A1dameApothekeSectionPanel.ui.xml, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: NBOOverviewView.ui.xml
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in NBOOverviewView.ui.xml, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesConvAdministrationPortletView.ui.xml
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in SalesConvAdministrationPortletView.ui.xml, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: BIZKOSectionPanel.ui.xml
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in BIZKOSectionPanel.ui.xml, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: IpVoiceCostsPanel.ui.xml
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in IpVoiceCostsPanel.ui.xml, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessMobileInternetSectionPanel.ui.xml
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessMobileInternetSectionPanel.ui.xml, skipping
2026-01-01 01:57:52 [INFO] codeindex.services.frontend_analyzer: Analyzing: merge_cells.htm
2026-01-01 01:58:47 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:58:47 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 01:59:05 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: fullpage_form
2026-01-01 01:59:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: source_editor.htm
2026-01-01 01:59:15 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:59:15 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 01:59:48 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 01:59:48 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 02:00:55 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 02:00:55 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 02:00:55 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/table/row.htm: Ollama request timed out: timed out
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: NBOWidget.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in NBOWidget.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductNotesPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in ProductNotesPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionEditPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionEditPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: en.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in en.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: ToDoGroupWidget.java
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in ToDoGroupWidget.java, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: FixedLineSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in FixedLineSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyNotesView.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in MyNotesView.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: Allgemein.html
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in Allgemein.html, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: advlink.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in advlink.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: link.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in link.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: BIZKOSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in BIZKOSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: GucciNBODetailView.java
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in GucciNBODetailView.java, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: ExtendedNBOWidget.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in ExtendedNBOWidget.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: IdentificationDataPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in IdentificationDataPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: UserAdminSegmentView.java
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in UserAdminSegmentView.java, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketplaceCostsPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in MarketplaceCostsPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: ins.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in ins.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: A1VoipHardwareWidget.java
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in A1VoipHardwareWidget.java, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: DeviceAsAServicePriceConfigView.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in DeviceAsAServicePriceConfigView.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessGlasfaserInternetSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessGlasfaserInternetSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobilePhonePanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in MobilePhonePanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: en.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in en.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: BPBSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in BPBSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberEditPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberEditPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: WebspaceAndCloudSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in WebspaceAndCloudSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberCostsPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberCostsPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: FIBSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in FIBSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: BPBSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in BPBSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsSAPSubscriptionNodeView.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsSAPSubscriptionNodeView.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionEditPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionEditPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: CloneProductsDialog.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in CloneProductsDialog.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: IPVoiceSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in IPVoiceSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editable_selects.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editable_selects.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: WLANSchuleSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in WLANSchuleSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductAndServicesWidget.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in ProductAndServicesWidget.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: CouponSeriesEditView.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in CouponSeriesEditView.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesInfoAttributesView.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in SalesInfoAttributesView.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberCostsPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberCostsPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: Elearning.htm
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in Elearning.htm, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: WLANSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in WLANSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: emotions.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in emotions.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: A1dameApothekeSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in A1dameApothekeSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: UITextsEditorPortletView.java
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in UITextsEditorPortletView.java, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessInternetSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessInternetSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: AdditionalProductSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in AdditionalProductSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: CuCoHistoryPopup.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in CuCoHistoryPopup.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: Produktdetail.html
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in Produktdetail.html, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: Ansprechpartner.html
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in Ansprechpartner.html, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: InternetSectionPanel.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in InternetSectionPanel.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: BaseCctConfigurationView.java
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in BaseCctConfigurationView.java, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesConvNoteView.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in SalesConvNoteView.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: PastTicketView.ui.xml
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in PastTicketView.ui.xml, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_template_src.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_template_src.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: DigitalSellingNoteHistoryView.java
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in DigitalSellingNoteHistoryView.java, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 02:00:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: rule.htm
2026-01-01 02:01:12 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 02:01:12 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 02:01:12 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/style/props.htm: Ollama request timed out: timed out
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: Temporaeres_Ausblenden_eines_Kunden.html
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in Temporaeres_Ausblenden_eines_Kunden.html, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: image.js
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in image.js, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberCostsPanel.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberCostsPanel.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferDetailsView.java
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferDetailsView.java, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: Bindungen.html
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in Bindungen.html, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: PartyDataDetailsView.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in PartyDataDetailsView.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessFirewallView.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessFirewallView.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: GenericNoteView.java
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in GenericNoteView.java, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: AttributeConfigView.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in AttributeConfigView.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: IpVoiceCostsPanel.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in IpVoiceCostsPanel.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: CouponSeriesEditView.java
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in CouponSeriesEditView.java, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketplaceCostsPanel.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in MarketplaceCostsPanel.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: OanSectionPanel.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in OanSectionPanel.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsPhysicalResourceNodeView.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsPhysicalResourceNodeView.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: tiny_mce.js
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in tiny_mce.js, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: IPVoiceSectionPanel.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in IPVoiceSectionPanel.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionSectionPanel.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionSectionPanel.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: SearchView.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in SearchView.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: editable_selects.js
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in editable_selects.js, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: TvSectionPanel.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in TvSectionPanel.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductBrowserView.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in ProductBrowserView.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyCuCoHeaderInfoView.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in MyCuCoHeaderInfoView.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:01:12 [INFO] codeindex.services.frontend_analyzer: Analyzing: anchor.htm
2026-01-01 02:01:19 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 02:01:19 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 02:01:19 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/xhtmlxtras/ins.htm: Ollama request timed out: timed out
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteFlashInfoEditView.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteFlashInfoEditView.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileProductSectionPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in MobileProductSectionPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: LocationView.java
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in LocationView.java, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: Ueberblick.html
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in Ueberblick.html, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: UsageDataView.java
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in UsageDataView.java, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: CctSwitchDiscountBoxSelector.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in CctSwitchDiscountBoxSelector.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: FlashDataView.java
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in FlashDataView.java, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: DeviceAsAServicePriceConfigView.java
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in DeviceAsAServicePriceConfigView.java, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: de.js
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in de.js, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteWidget.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteWidget.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsAccountNodeView.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsAccountNodeView.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: HouseholdPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in HouseholdPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: de.js
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in de.js, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditMetadataWidget.java
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in EditMetadataWidget.java, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditTeamsDialog.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in EditTeamsDialog.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductSectionPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in ProductSectionPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobilPointsPopup.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in MobilPointsPopup.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: MergeNonCustomerWithCustomerView.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in MergeNonCustomerWithCustomerView.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessInternetSectionPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessInternetSectionPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: TVPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in TVPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: Umsatz_und_Deckungsbeitrag.html
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in Umsatz_und_Deckungsbeitrag.html, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: IpVoiceCostsPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in IpVoiceCostsPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: EcardSectionPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in EcardSectionPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteClearanceRuleConfigView.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteClearanceRuleConfigView.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: A1dameArztSectionPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in A1dameArztSectionPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: MyBindingsView.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in MyBindingsView.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: WLANSectionPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in WLANSectionPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketplaceGroupCostsPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in MarketplaceGroupCostsPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: CustomerValueView.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in CustomerValueView.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductSectionPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in ProductSectionPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: Inventaranzeige.html
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in Inventaranzeige.html, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_template.js
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in editor_template.js, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionEditPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionEditPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: DialogComponent.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in DialogComponent.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 02:01:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: ins.htm
2026-01-01 02:01:23 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 02:01:23 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 02:01:34 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 02:01:34 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: merge_cells_form
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: IPVoiceSectionPanel.ui.xml
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: No form found in IPVoiceSectionPanel.ui.xml, skipping
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: PartyWidget.ui.xml
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: No form found in PartyWidget.ui.xml, skipping
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: WLANSchuleProductAndServicesWidget.java
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: No form found in WLANSchuleProductAndServicesWidget.java, skipping
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: mctabs.js
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: No form found in mctabs.js, skipping
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: LocationCostsPanel.ui.xml
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: No form found in LocationCostsPanel.ui.xml, skipping
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: Aufbau_des_Customer_Cockpits.html
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: No form found in Aufbau_des_Customer_Cockpits.html, skipping
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: about.htm
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: No form found in about.htm, skipping
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: HardwareCostsPanel.ui.xml
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: No form found in HardwareCostsPanel.ui.xml, skipping
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: BIZKOSectionPanel.ui.xml
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: No form found in BIZKOSectionPanel.ui.xml, skipping
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: SearchResultWidgetView.java
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: No form found in SearchResultWidgetView.java, skipping
2026-01-01 02:01:42 [INFO] codeindex.services.frontend_analyzer: Analyzing: fullscreen.htm
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: source
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductOverviewPortletView.java
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: No form found in ProductOverviewPortletView.java, skipping
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: TvSectionPanel.ui.xml
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: No form found in TvSectionPanel.ui.xml, skipping
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: media.js
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: No form found in media.js, skipping
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsEmptyView.java
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsEmptyView.java, skipping
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesInfoOverviewView.ui.xml
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: No form found in SalesInfoOverviewView.ui.xml, skipping
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: Beispiel3.htm
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: No form found in Beispiel3.htm, skipping
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:01:55 [INFO] codeindex.services.frontend_analyzer: Analyzing: del.htm
2026-01-01 02:02:04 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: source
2026-01-01 02:02:04 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 02:02:04 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 02:02:04 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:02:04 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:02:04 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteClearanceRuleConfigView.java
2026-01-01 02:02:04 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteClearanceRuleConfigView.java, skipping
2026-01-01 02:02:04 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesInfoAttributesHistoryView.ui.xml
2026-01-01 02:02:04 [INFO] codeindex.services.frontend_analyzer: No form found in SalesInfoAttributesHistoryView.ui.xml, skipping
2026-01-01 02:02:04 [INFO] codeindex.services.frontend_analyzer: Analyzing: CustomerEquipmentView.java
2026-01-01 02:02:04 [INFO] codeindex.services.frontend_analyzer: No form found in CustomerEquipmentView.java, skipping
2026-01-01 02:02:04 [INFO] codeindex.services.frontend_analyzer: Analyzing: SendSalesConvEmailView.ui.xml
2026-01-01 02:02:04 [INFO] codeindex.services.frontend_analyzer: No form found in SendSalesConvEmailView.ui.xml, skipping
2026-01-01 02:02:04 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferBusinessView.java
2026-01-01 02:02:19 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: AnchorForm
2026-01-01 02:02:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessFirewallSectionPanel.ui.xml
2026-01-01 02:02:19 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessFirewallSectionPanel.ui.xml, skipping
2026-01-01 02:02:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: WebspaceAndCloudSectionPanel.ui.xml
2026-01-01 02:02:19 [INFO] codeindex.services.frontend_analyzer: No form found in WebspaceAndCloudSectionPanel.ui.xml, skipping
2026-01-01 02:02:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: ManageSBSProductsConfigurationView.java
2026-01-01 02:02:19 [INFO] codeindex.services.frontend_analyzer: No form found in ManageSBSProductsConfigurationView.java, skipping
2026-01-01 02:02:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 02:02:19 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 02:02:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 02:02:19 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 02:02:19 [INFO] codeindex.services.frontend_analyzer: Analyzing: ImageListWidget.java
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: AdvHRForm
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: Finanzdaten.html
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in Finanzdaten.html, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: en.js
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in en.js, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: TurnoverRangeView.java
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in TurnoverRangeView.java, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileCostsPanel.ui.xml
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in MobileCostsPanel.ui.xml, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionSectionPanel.ui.xml
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionSectionPanel.ui.xml, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: RestrictedStammblatt.html
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in RestrictedStammblatt.html, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductAndServicesWidget.java
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in ProductAndServicesWidget.java, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: CustomerInteractionView.ui.xml
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in CustomerInteractionView.ui.xml, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: IPVoiceSectionPanel.ui.xml
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in IPVoiceSectionPanel.ui.xml, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: MarketplaceCostsPanel.ui.xml
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in MarketplaceCostsPanel.ui.xml, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: Anzeige_eines_Kunden_im_CuCo.html
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in Anzeige_eines_Kunden_im_CuCo.html, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: ServiceNetzSchuleSectionPanel.ui.xml
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: No form found in ServiceNetzSchuleSectionPanel.ui.xml, skipping
2026-01-01 02:02:47 [INFO] codeindex.services.frontend_analyzer: Analyzing: color_picker.htm
2026-01-01 02:02:50 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 02:02:50 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 02:02:50 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/table/table.htm: Ollama request timed out: timed out
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: PartyDataPortletView.java
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in PartyDataPortletView.java, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: Anwendungsbeispiele.html
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in Anwendungsbeispiele.html, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: PartyDataPortletView.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in PartyDataPortletView.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: InternetSectionPanel.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in InternetSectionPanel.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: Kundennotiz.html
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in Kundennotiz.html, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: WLANSchuleProductAndServicesWidget.java
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in WLANSchuleProductAndServicesWidget.java, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: index.html
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in index.html, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: TvSectionPanel.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in TvSectionPanel.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: LinksPortletView.java
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in LinksPortletView.java, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberEditPanel.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberEditPanel.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: InternetSectionPanel.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in InternetSectionPanel.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: BillingsWidgetView.java
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in BillingsWidgetView.java, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: TvSectionPanel.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in TvSectionPanel.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: EcardSectionPanel.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in EcardSectionPanel.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessFirewallSectionPanel.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessFirewallSectionPanel.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: SNGMobileAccessSectionPanel.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in SNGMobileAccessSectionPanel.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: charmap.htm
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in charmap.htm, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: SNGGemeindeamtSectionPanel.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in SNGGemeindeamtSectionPanel.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: image.js
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in image.js, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: WLANSchuleProductAndServicesWidget.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in WLANSchuleProductAndServicesWidget.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: DetailsDefaultProductNodeView.ui.xml
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in DetailsDefaultProductNodeView.ui.xml, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: PkbMainView.java
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: No form found in PkbMainView.java, skipping
2026-01-01 02:02:50 [INFO] codeindex.services.frontend_analyzer: Analyzing: acronym.htm
2026-01-01 02:03:46 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: ProductNotesPanelForm
2026-01-01 02:03:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:03:46 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:03:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 02:03:46 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 02:03:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: CustomerBlockEditView.java
2026-01-01 02:03:46 [INFO] codeindex.services.frontend_analyzer: No form found in CustomerBlockEditView.java, skipping
2026-01-01 02:03:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:03:46 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:03:46 [INFO] codeindex.services.frontend_analyzer: Analyzing: template.htm
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: fullscreen_form
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: OanCostsPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in OanCostsPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: en.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in en.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: BaseMarketingProductListItemWidget.java
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in BaseMarketingProductListItemWidget.java, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberEditPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberEditPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: de.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in de.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: index.html
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in index.html, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: QuoteOverviewView.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in QuoteOverviewView.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: HostedCommunicationServiceSectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in HostedCommunicationServiceSectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SNGMobileAccessSectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SNGMobileAccessSectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: ins.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in ins.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: media.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in media.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: Header.html
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in Header.html, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: TypeView.java
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in TypeView.java, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: OfferedOfferOverviewView.java
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in OfferedOfferOverviewView.java, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SendSalesConvEmailView.java
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SendSalesConvEmailView.java, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_template_src.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in editor_template_src.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: CallNumberEditPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in CallNumberEditPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: run.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in run.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: ContactEditPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in ContactEditPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessFirewallSectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessFirewallSectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: PastPortletView.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in PastPortletView.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: EditCreditTypesDialog.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in EditCreditTypesDialog.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: BIZKOSectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in BIZKOSectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: UsageDataMobilPointsView.java
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in UsageDataMobilPointsView.java, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: LastOfferInteractionView.java
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in LastOfferInteractionView.java, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: OrgStructView.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in OrgStructView.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: ManageSBSProductsConfigurationView.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in ManageSBSProductsConfigurationView.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: ProductManageAdministrationPortletView.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in ProductManageAdministrationPortletView.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: AdminMainView.java
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in AdminMainView.java, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: CustomerValueView.java
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in CustomerValueView.java, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: merge_cells.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in merge_cells.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: Aufruf_und_Aufbau_des_Suchformulares.html
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in Aufruf_und_Aufbau_des_Suchformulares.html, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: CostsPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in CostsPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SpecialAgreementSectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SpecialAgreementSectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: anchor.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in anchor.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SalesConvAdministrationPortletView.java
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SalesConvAdministrationPortletView.java, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: pastetext.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in pastetext.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: Produkte.html
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in Produkte.html, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: GeneralSectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in GeneralSectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: GwtIbatisPortletView.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in GwtIbatisPortletView.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: de_dlg.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in de_dlg.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: Header.html
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in Header.html, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: InteractionPortletView.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in InteractionPortletView.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: ApothekennetzSectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in ApothekennetzSectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: CctClearanceContainer.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in CctClearanceContainer.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: BusinessFirewallSectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in BusinessFirewallSectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: ValueWidget.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in ValueWidget.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: source_editor.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in source_editor.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: ContactPersonPortletView.java
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in ContactPersonPortletView.java, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummaryPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SummaryPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_template_src.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in editor_template_src.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: AdditionalProductSectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in AdditionalProductSectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: SummarySectionPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in SummarySectionPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: embed.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in embed.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: editor_plugin_src.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in editor_plugin_src.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: MobileSubscriptionEditPanel.ui.xml
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in MobileSubscriptionEditPanel.ui.xml, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: en_dlg.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in en_dlg.js, skipping
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: Analyzing: fullpage.js
2026-01-01 02:04:05 [INFO] codeindex.services.frontend_analyzer: No form found in fullpage.js, skipping
2026-01-01 02:04:41 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: ins_form
2026-01-01 02:05:03 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: OfferedOfferBusinessForm
2026-01-01 02:05:24 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 02:05:24 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 02:05:35 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 02:05:35 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 2/3): Ollama request timed out: timed out. Retrying in 2.0 seconds...
2026-01-01 02:05:44 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: ImageListWidgetForm
2026-01-01 02:05:50 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: colorpicker_form
2026-01-01 02:05:55 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 02:05:55 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 02:06:08 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: template_form
2026-01-01 02:06:50 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 02:06:50 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out. Retrying in 1.0 seconds...
2026-01-01 02:07:05 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: image_form
2026-01-01 02:08:05 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: del_form
2026-01-01 02:08:20 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: acronym_form
2026-01-01 02:09:37 [WARNING] codeindex.services.ollama_client: Ollama timeout after 240.0s: timed out
2026-01-01 02:09:37 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
2026-01-01 02:09:37 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-common/src/main/resources/at/a1ta/cuco/ui/common/public/tiny_mce/themes/advanced/image.htm: Ollama request timed out: timed out
[INFO] Generating frontend index...
[INFO] Generating frontend PRD...
[INFO] Frontend analysis complete: 47 forms, 0 components

============================================================
PRD Generation Complete
============================================================

Summary:
------------------------------------------------------------
Frontend:  47 forms, 0 components
           (1424 analyzed, 0 skipped, 17 failed)
------------------------------------------------------------

Output directory: output/cuco-ui-admin/prd
  - database/: Entity definitions and index
  - services/: Service definitions and endpoints
  - frontend/: Forms and UI components
  - business_rules/: Business rule definitions
  - prd/: Generated PRD markdown documents
2026-01-01 02:09:37 [INFO] codeindex.codeindex.cli.prd: PRD generation complete: layer=frontend, output_dir=output/cuco-ui-admin/prd
