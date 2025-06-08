# 小食部管理系統數據庫（Canteen Management System Database）

本專案為學校小食部管理系統的數據庫設計與數據初始化腳本，包含數據庫結構、示例數據插入及常用查詢語句。

## 文件說明

### 1. `ICT_SBA_Canteen_db_schema_init.sql`
- **用途**：初始化小食部管理系統的數據庫結構。
- **內容**：
  - 創建數據庫 `canteen_management`。
  - 創建主要業務表格，包括：
    - `User`（用戶/學生/教師/職員）
    - `OctopusCard`（八達通卡）
    - `Staff`（職員）
    - `Supplier`（供應商）
    - `Product`（產品）
    - `Promotion`（促銷活動）
    - `PromotionProduct`（促銷產品關聯）
    - `Transaction`（交易）
    - `TransactionDetail`（交易明細）
    - `RestockOrder`（補貨訂單）
  - 設置外鍵約束與索引以保證數據一致性與查詢效率。

### 2. `ICT_SBA_Data_Insert.sql`
- **用途**：插入示例數據，便於測試和演示。
- **內容**：
  - 為每個表格插入多條真實場景下的測試數據。
  - 包含學生、教師、職員、產品、供應商、促銷、交易、補貨等多維度數據。

### 3. `ICT_SBA_Select.sql`
- **用途**：常用查詢語句示例，便於數據分析與報表生成。
- **內容**：
  - 日銷售統計、毛利率計算
  - 最暢銷產品排名
  - 按年級統計學生消費情況
  - 其他業務相關查詢

## 使用方法

1. **初始化數據庫結構**
   - 在 MySQL 環境下運行 `ICT_SBA_Canteen_db_schema_init.sql`。
2. **插入測試數據**
   - 運行 `ICT_SBA_Data_Insert.sql`，將示例數據導入數據庫。
3. **查詢與分析**
   - 根據需求，運行 `ICT_SBA_Select.sql` 中的查詢語句，獲取業務統計與分析結果。

## 適用場景
- 學校資訊科技科 SBA 專題
- 小食部日常管理與數據分析
- 數據庫設計與 SQL 練習

## 聯絡方式
如有疑問，請聯絡專案負責人或指導老師。

---

**注意：** 所有密碼僅為示例，實際應用請使用加密存儲！

