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

### 4. `Sample_Generater` Directory
- **用途**：包含用於生成大量樣本數據的Python腳本，每個表格有獨立的腳本。
- **主要文件**：
  - `generate_all_data.py` - 主腳本，運行所有表格的數據生成腳本
  - 各表格獨立腳本 - 為每個表格生成1000條樣本數據

## 使用方法

1. **初始化數據庫結構**
   - 在 MySQL 環境下運行 `ICT_SBA_Canteen_db_schema_init.sql`。
2. **插入測試數據**
   - 運行 `ICT_SBA_Data_Insert.sql`，將少量示例數據導入數據庫。
   - 或者使用Python腳本生成大量測試數據（見下方說明）。
3. **查詢與分析**
   - 根據需求，運行 `ICT_SBA_Select.sql` 中的查詢語句，獲取業務統計與分析結果。

## 使用Python腳本生成大量樣本數據

### 前置條件
1. 安裝Python 3.6+
2. 安裝所需依賴套件：
   ```
   pip install faker
   ```

### 生成數據步驟
1. 切換到Sample_Generater目錄
   ```
   cd /path/to/Sample_Generater
   ```
2. 運行主腳本以生成所有表格的樣本數據
   ```
   python generate_all_data.py
   ```
3. 或者，可單獨運行各個腳本生成特定表格的數據，例如：
   ```
   python generate_users.py
   python generate_products.py
   ```
4. 生成的SQL文件可直接導入數據庫

### 注意順序

為避免外鍵約束錯誤，若手動導入生成的SQL文件，請按以下順序執行：
1. octopus_cards_data.sql
2. suppliers_data.sql
3. staff_data.sql
4. users_data.sql
5. products_data.sql
6. promotions_data.sql
7. promotion_products_data.sql
8. transactions_data.sql
9. transaction_details_data.sql
10. restock_orders_data.sql

這個順序確保了引用關係正確建立。

---

**注意：** 
1. 所有密碼僅為示例，實際應用請使用加密存儲！
2. 生成的樣本數據僅供測試和評估系統性能，不包含敏感信息。
