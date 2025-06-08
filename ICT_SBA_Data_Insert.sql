USE canteen_management;
-- 示例數據插入


-- 插入 OctopusCard 數據
INSERT INTO OctopusCard (CardNumber, Balance, RegistrationDate) VALUES
('1234567890123456', 100.00, '2025-01-15'),
('2345678901234567', 50.00, '2025-01-16'),
('3456789012345678', 75.50, '2025-01-20'),
('4567890123456789', 120.00, '2025-01-22'),
('5678901234567890', 30.00, '2025-02-01'),
('6789012345678901', 200.00, '2025-02-05'),
('7890123456789012', 85.00, '2025-02-10'),
('8901234567890123', 150.00, '2025-02-15'),
('9012345678901234', 60.00, '2025-03-01'),
('0123456789012345', 90.00, '2025-03-05');

-- 插入 User 數據
INSERT INTO User (Name, Role, ContactNumber, Email, Grade, OctopusID, JoinDate) VALUES
('張曉明', 'Student', '98765432', 'xiaoming.zhang@school.edu.hk', 'S3', 1, '2025-01-15'),
('李華', 'Student', '87654321', 'hua.li@school.edu.hk', 'S4', 2, '2025-01-16'),
('王小紅', 'Student', '76543210', 'xiaohong.wang@school.edu.hk', 'S2', 3, '2025-01-20'),
('陳大文', 'Teacher', '65432109', 'dawen.chen@school.edu.hk', NULL, 4, '2025-01-22'),
('黃老師', 'Teacher', '54321098', 'huang.teacher@school.edu.hk', NULL, 5, '2025-02-01'),
('趙敏', 'Student', '43210987', 'min.zhao@school.edu.hk', 'S5', 6, '2025-02-05'),
('劉偉', 'Student', '32109876', 'wei.liu@school.edu.hk', 'S1', 7, '2025-02-10'),
('張三', 'Staff', '21098765', 'san.zhang@school.edu.hk', NULL, 8, '2025-02-15'),
('李四', 'Student', '10987654', 'si.li@school.edu.hk', 'S6', 9, '2025-03-01'),
('王五', 'Student', '09876543', 'wu.wang@school.edu.hk', 'S3', 10, '2025-03-05');

-- 插入 Staff 數據
INSERT INTO Staff (Name, Position, ContactNumber, Password) VALUES
('陳經理', 'Manager', '98765400', 'hashed_password_1'),
('李小姐', 'Cashier', '87654300', 'hashed_password_2'),
('王先生', 'Stock Keeper', '76543200', 'hashed_password_3'),
('趙助理', 'Assistant', '65432100', 'hashed_password_4');

-- 插入 Supplier 數據
INSERT INTO Supplier (CompanyName, ContactPerson, Phone, Email, Address) VALUES
('健康食品有限公司', '張總', '23456789', 'contact@health-food.com', '九龍灣工業區A座10樓'),
('優質飲料公司', '李經理', '34567890', 'manager@quality-drinks.com', '觀塘商業中心B座5樓'),
('鮮果批發商', '王老闆', '45678901', 'owner@fresh-fruits.com', '新界元朗工業邨C區12號'),
('烘焙食品供應商', '陳師傅', '56789012', 'master@bakery-supply.com', '香港仔海濱道88號');

-- 插入 Product 數據
INSERT INTO Product (ProductName, Price, CostPrice, StockQuantity, MinStockThreshold, Category, SupplierID, ExpiryDate) VALUES
('三明治', 15.00, 10.00, 8, 10, '主食', 1, '2025-06-20'),
('牛奶', 8.50, 5.00, 100, 20, '飲料', 2, '2025-06-15'),
('蘋果', 5.00, 3.00, 10, 15, '水果', 3, '2025-06-10'),
('礦泉水', 6.00, 2.50, 150, 30, '飲料', 2, '2025-12-31'),
('巧克力', 10.00, 6.00, 5, 15, '零食', 1, '2025-08-15'),
('薯片', 12.00, 7.00, 75, 20, '零食', 1, '2025-07-20'),
('橙汁', 9.50, 6.50, 90, 25, '飲料', 2, '2025-06-30'),
('麵包', 7.50, 4.00, 12, 15, '主食', 4, '2025-06-05'),
('蛋糕', 18.00, 12.00, 25, 10, '甜點', 4, '2025-06-08'),
('壽司', 22.00, 15.00, 7, 10, '主食', 1, '2025-06-03');

-- 插入 Promotion 數據
INSERT INTO Promotion (PromotionName, DiscountRate, StartDate, EndDate) VALUES
('特價促銷', 0.85, '2025-05-01', '2025-05-31'),
('開學特惠', 0.90, '2025-09-01', '2025-09-15'),
('節日折扣', 0.80, '2025-12-20', '2025-12-31'),
('清倉特賣', 0.70, '2025-07-15', '2025-07-31');

-- 插入 PromotionProduct 數據
INSERT INTO PromotionProduct (PromotionID, ProductID) VALUES
(1, 3),
(1, 5),
(2, 1),
(2, 2),
(2, 7),
(3, 5),
(3, 6),
(3, 9),
(4, 10),
(4, 8);

-- 插入 Transaction 數據
INSERT INTO Transaction (UserID, OctopusID, StaffID, PromotionID, TransactionTime, TotalAmount, PaymentStatus) VALUES
(1, 1, 2, NULL, '2025-06-01 08:30:00', 23.50, 'Paid'),
(2, 2, 2, 1, '2025-06-01 09:15:00', 17.00, 'Paid'),
(3, 3, 2, NULL, '2025-06-01 10:20:00', 30.00, 'Paid'),
(4, 4, 2, NULL, '2025-06-01 12:05:00', 27.50, 'Paid'),
(5, 5, 2, NULL, '2025-06-01 12:30:00', 18.00, 'Paid'),
(6, 6, 2, 1, '2025-06-01 13:10:00', 42.50, 'Paid'),
(7, 7, 2, NULL, '2025-06-01 13:45:00', 12.00, 'Paid'),
(8, 8, 2, NULL, '2025-06-01 14:25:00', 33.00, 'Paid'),
(9, 9, 2, NULL, '2025-06-01 15:00:00', 22.00, 'Failed'),
(2, 2, 2, NULL, '2025-06-02 08:45:00', 15.50, 'Paid'),
(3, 3, 2, NULL, '2025-06-02 09:30:00', 18.00, 'Paid'),
(1, 1, 2, 1, '2025-06-02 10:15:00', 25.50, 'Paid');

-- 插入 TransactionDetail 數據
INSERT INTO TransactionDetail (TransactionID, ProductID, Quantity, UnitPrice) VALUES
(1, 1, 1, 15.00),
(1, 2, 1, 8.50),
(2, 3, 2, 5.00),
(2, 5, 1, 10.00),
(3, 4, 5, 6.00),
(4, 8, 1, 7.50),
(4, 7, 1, 9.50),
(4, 2, 1, 8.50),
(5, 9, 1, 18.00),
(6, 10, 1, 22.00),
(6, 7, 1, 9.50),
(6, 5, 1, 10.00),
(7, 6, 1, 12.00),
(8, 1, 1, 15.00),
(8, 9, 1, 18.00),
(9, 10, 1, 22.00),
(10, 8, 1, 7.50),
(10, 2, 1, 8.50),
(11, 9, 1, 18.00),
(12, 1, 1, 15.00),
(12, 5, 1, 10.00);

-- 插入 RestockOrder 數據
INSERT INTO RestockOrder (ProductID, OrderQuantity, OrderDate, ArrivalDate, SupplierID, Status) VALUES
(1, 100, '2025-05-20', '2025-05-23', 1, 'Delivered'),
(2, 150, '2025-05-21', '2025-05-24', 2, 'Delivered'),
(3, 120, '2025-05-25', '2025-05-29', 3, 'Delivered'),
(4, 200, '2025-05-26', '2025-05-30', 2, 'Delivered'),
(5, 80, '2025-05-28', NULL, 1, 'Shipped'),
(6, 100, '2025-05-30', NULL, 1, 'Pending'),
(7, 120, '2025-06-01', NULL, 2, 'Pending'),
(8, 60, '2025-05-15', '2025-05-19', 4, 'Delivered'),
(9, 40, '2025-05-16', '2025-05-20', 4, 'Delivered'),
(10, 50, '2025-05-29', NULL, 1, 'Shipped');
