# Data Structures Summary

## Overview
- **Entities Found**: 6
- **DTOs Found**: 28
- **Relationships**: 0

## Entity Details

### RTCodeModel
- **Package**: at.a1ta.cuco.admin.ui.common.client.dto
- **Fields**: 3
- **Business Domain**: customer, product, order, support, admin
- **Key Fields**:
  - serialVersionUID: long
  - b: Boolean
  - null: return

### PartySummaryPrintModel
- **Package**: at.a1ta.cuco.core.shared.dto
- **Fields**: 9
- **Business Domain**: product
- **Key Fields**:
  - serialVersionUID: long
  - party: Party
  - party: return
  - products: return
  - subscriptions: return

### PartyModel
- **Package**: at.a1ta.cuco.core.shared.model
- **Fields**: 65
- **Business Domain**: customer, product, support
- **Key Fields**:
  - serialVersionUID: long
  - id: Long
  - bans: String
  - commercialRegisterNumber: String
  - businessSegment: String

### PartyModelFactory
- **Package**: at.a1ta.cuco.core.shared.model
- **Fields**: 18
- **Business Domain**: customer, product, billing, order, support
- **Key Fields**:
  - order: int
  - order: return
  - result: PartyModel
  - result: return
  - sb: StringBuilder

### DigitalSellingNotePrintModel
- **Package**: at.a1ta.cuco.core.service.visitreport
- **Fields**: 10
- **Business Domain**: product, billing
- **Key Fields**:
  - title: String
  - priceOld: String
  - noteOld: String
  - priceNew: String
  - noteNew: String

### ProductAdministrationPortletView
- **Package**: at.a1ta.cuco.ui.admin.client.ui.portlet
- **Fields**: 37
- **Business Domain**: customer, product, order, admin
- **Key Fields**:
  - uiBinder: ProductAdministrationPortletViewUiBinder
  - productTree: ArrayList<ProductLevel>
  - productGroupsDataProvider: ListDataProvider<InventoryProductGroup>
  - productTreeSelectionModel: SingleSelectionModel<InventoryProductGroupAssignable>
  - productGroupAssignmentDataProvider: ListDataProvider<InventoryProductGroupAssignable>

## DTO Details

### ApplicationInitData
- **Package**: at.a1ta.framework.ui.client.dto
- **Fields**: 2

### ModelDataCombo
- **Package**: at.a1ta.framework.ui.client.ui
- **Fields**: 12

### ModelDataSuggestBox
- **Package**: at.a1ta.framework.ui.client.ui
- **Fields**: 8

### ModelData
- **Package**: at.a1ta.framework.ui.client.ui
- **Fields**: 2

### HasTableDataStore
- **Package**: at.a1ta.framework.ui.client.ui
- **Fields**: 0

### DataTableFilter
- **Package**: at.a1ta.framework.ui.client.ui.table
- **Fields**: 0

### TableDataComparator
- **Package**: at.a1ta.framework.ui.client.ui.table
- **Fields**: 1

### TableDataStore
- **Package**: at.a1ta.framework.ui.client.ui.table
- **Fields**: 12

### DataTheftRapidAlertJobTest
- **Package**: at.a1ta.cuco.core.service.cron
- **Fields**: 10

### StandardAddress
- **Package**: at.a1ta.cuco.core.shared.dto
- **Fields**: 81
