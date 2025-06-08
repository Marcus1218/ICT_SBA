-- 創建小食部管理數據庫

DROP DATABASE IF EXISTS canteen_management;
-- For Testing SQL Code
CREATE DATABASE IF NOT EXISTS canteen_management;
-- Create the database if it does not exist
USE canteen_management;
-- Use the database
-- 創建 User 表格（用戶）
CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Role ENUM('Student', 'Teacher', 'Staff') NOT NULL,
    ContactNumber VARCHAR(15),
    Email VARCHAR(50),
    Grade VARCHAR(10),  -- 學生年級，如'S1', 'S2', 教師可為NULL
    OctopusID INT UNIQUE,  -- 關聯八達通卡ID
    JoinDate DATE NOT NULL
);

-- 創建 OctopusCard 表格（八達通卡）
CREATE TABLE OctopusCard (
    OctopusID INT AUTO_INCREMENT PRIMARY KEY,
    CardNumber VARCHAR(16) NOT NULL UNIQUE,
    Balance DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    RegistrationDate DATE NOT NULL
);

-- 添加外鍵關係: User - OctopusCard
ALTER TABLE User
ADD CONSTRAINT FK_User_OctopusCard FOREIGN KEY (OctopusID)
    REFERENCES OctopusCard(OctopusID) ON DELETE SET NULL;

-- 創建 Staff 表格（職員）
CREATE TABLE Staff (
    StaffID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Position VARCHAR(30) NOT NULL,
    ContactNumber VARCHAR(15) NOT NULL,
    Password VARCHAR(255) NOT NULL  -- 存儲加密後的密碼
);

-- 創建 Supplier 表格（供應商）
CREATE TABLE Supplier (
    SupplierID INT AUTO_INCREMENT PRIMARY KEY,
    CompanyName VARCHAR(100) NOT NULL,
    ContactPerson VARCHAR(50) NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Email VARCHAR(50),
    Address VARCHAR(200) NOT NULL
);

-- 創建 Promotion 表格（促銷活動）
CREATE TABLE Promotion (
    PromotionID INT AUTO_INCREMENT PRIMARY KEY,
    PromotionName VARCHAR(100) NOT NULL,
    DiscountRate DECIMAL(5,2) NOT NULL,  -- 折扣率，如0.90表示9折
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL
);

-- 創建 Product 表格（產品）
CREATE TABLE Product (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(100) NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    CostPrice DECIMAL(10,2) NOT NULL,  -- 添加成本價格欄位
    StockQuantity INT NOT NULL DEFAULT 0,
    MinStockThreshold INT NOT NULL DEFAULT 10,
    Category VARCHAR(50) NOT NULL,
    SupplierID INT,
    ExpiryDate DATE,
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID) ON DELETE SET NULL
);

-- 創建 Transaction 表格（交易）
CREATE TABLE Transaction (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    OctopusID INT NOT NULL,
    StaffID INT,
    PromotionID INT,
    TransactionTime DATETIME NOT NULL,
    TotalAmount DECIMAL(10,2) NOT NULL,
    PaymentStatus ENUM('Paid', 'Failed', 'Refunded') NOT NULL DEFAULT 'Paid',
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE SET NULL,
    FOREIGN KEY (OctopusID) REFERENCES OctopusCard(OctopusID) ON DELETE CASCADE,
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE SET NULL,
    FOREIGN KEY (PromotionID) REFERENCES Promotion(PromotionID) ON DELETE SET NULL
);

-- 創建 TransactionDetail 表格（交易明細）
CREATE TABLE TransactionDetail (
    DetailID INT AUTO_INCREMENT PRIMARY KEY,
    TransactionID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,  -- 記錄當時的單價
    FOREIGN KEY (TransactionID) REFERENCES Transaction(TransactionID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE CASCADE
);

-- 創建 RestockOrder 表格（補貨訂單）
CREATE TABLE RestockOrder (
    RestockID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT NOT NULL,
    OrderQuantity INT NOT NULL,
    OrderDate DATE NOT NULL,
    ArrivalDate DATE,
    SupplierID INT NOT NULL,
    Status ENUM('Pending', 'Shipped', 'Delivered', 'Cancelled') NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE CASCADE,
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID) ON DELETE CASCADE
);

-- 創建 PromotionProduct 表格（促銷產品關聯表）
CREATE TABLE PromotionProduct (
    PromotionID INT,
    ProductID INT,
    PRIMARY KEY (PromotionID, ProductID),
    FOREIGN KEY (PromotionID) REFERENCES Promotion(PromotionID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE CASCADE
);

-- 創建索引以提高查詢性能
CREATE INDEX idx_user_role ON User(Role);
CREATE INDEX idx_product_category ON Product(Category);
CREATE INDEX idx_transaction_time ON Transaction(TransactionTime);
CREATE INDEX idx_transaction_octopus ON Transaction(OctopusID);
CREATE INDEX idx_product_stock ON Product(StockQuantity);
CREATE INDEX idx_restock_status ON RestockOrder(Status);


