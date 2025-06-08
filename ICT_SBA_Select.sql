USE canteen_management;
-- 六個對小食部有用的查詢

-- 查詢1：庫存低的產品（需要補貨的產品）
SELECT
    p.ProductID AS 產品ID,
    p.ProductName AS 產品名稱,
    p.StockQuantity AS 當前庫存,
    p.MinStockThreshold AS 最低庫存閾值,
    p.Category AS 產品類別,
    CONCAT(ROUND((p.StockQuantity / p.MinStockThreshold) * 100, 0), '%') AS 庫存百分比,
    CASE
        WHEN p.StockQuantity = 0 THEN '已售罄'
        WHEN p.StockQuantity < (p.MinStockThreshold * 0.3) THEN '極度緊急'
        WHEN p.StockQuantity < (p.MinStockThreshold * 0.6) THEN '緊急'
        WHEN p.StockQuantity < p.MinStockThreshold THEN '需要補貨'
        ELSE '庫存充足'
    END AS 補貨狀態,
    s.CompanyName AS 供應商名稱,
    s.ContactPerson AS 聯絡人,
    s.Phone AS 供應商電話,
    (SELECT Status FROM RestockOrder ro WHERE ro.ProductID = p.ProductID ORDER BY ro.OrderDate DESC LIMIT 1) AS 最近訂單狀態
FROM
    Product p
JOIN
    Supplier s ON p.SupplierID = s.SupplierID
WHERE
    p.StockQuantity <= p.MinStockThreshold
ORDER BY
    (p.StockQuantity / p.MinStockThreshold) ASC,
    p.Category ASC;


-- 查詢2：每天的銷售總額、銷售數量、貨物成本和盈利統計（按日期分組）
SELECT
    DATE(t.TransactionTime) AS 銷售日期,
    SUM(t.TotalAmount) AS 日總收入,
    COUNT(t.TransactionID) AS 交易次數,
    SUM(td.Quantity * p.CostPrice) AS 貨物成本,
    SUM(t.TotalAmount) - SUM(td.Quantity * p.CostPrice) AS 毛利潤,
    CONCAT(ROUND(((SUM(t.TotalAmount) - SUM(td.Quantity * p.CostPrice)) / SUM(t.TotalAmount)) * 100, 2), '%') AS 毛利率
FROM
    Transaction t
JOIN
    TransactionDetail td ON t.TransactionID = td.TransactionID
JOIN
    Product p ON td.ProductID = p.ProductID
WHERE
    t.PaymentStatus = 'Paid'
GROUP BY
    DATE(t.TransactionTime)
ORDER BY
    銷售日期 DESC;

-- 查詢3：最暢銷的產品排名（按銷售數量排序）
SELECT
    p.ProductID AS 產品ID,
    p.ProductName AS 產品名稱,
    p.Category AS 類別,
    SUM(td.Quantity) AS 總銷量,
    SUM(td.Quantity * td.UnitPrice) AS 總收入
FROM
    TransactionDetail td
JOIN
    Product p ON td.ProductID = p.ProductID
JOIN
    Transaction t ON td.TransactionID = t.TransactionID
WHERE
    t.PaymentStatus = 'Paid'
    AND t.TransactionTime >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) -- 最近30天
GROUP BY
    p.ProductID, p.ProductName, p.Category
ORDER BY
    總銷量 DESC
LIMIT 10;

-- 查詢4：按年級統計學生消費情況
SELECT
    u.Grade AS 年級,
    COUNT(DISTINCT u.UserID) AS 學生人數,
    COUNT(t.TransactionID) AS 交易次數,
    ROUND(AVG(t.TotalAmount), 2) AS 平均消費,
    SUM(t.TotalAmount) AS 總消費,
    MAX(t.TotalAmount) AS 最大交易額
FROM
    User u
JOIN
    Transaction t ON u.UserID = t.UserID
WHERE
    u.Role = 'Student'
    AND t.PaymentStatus = 'Paid'
    AND t.TransactionTime >= DATE_SUB(CURDATE(), INTERVAL 90 DAY) -- 最近90天
GROUP BY
    u.Grade
ORDER BY
    總消費 DESC;

-- 查詢5：即將過期的產品（7天內將過期）及其促銷狀態
SELECT
    p.ProductID AS 產品ID,
    p.ProductName AS 產品名稱,
    p.Category AS 類別,
    p.StockQuantity AS 庫存量,
    p.ExpiryDate AS 到期日,
    DATEDIFF(p.ExpiryDate, CURDATE()) AS 剩餘天數,
    CASE
        WHEN p5.PromotionID IS NOT NULL THEN CONCAT('已有五折優惠 (至 ', p5.EndDate, ')')
        WHEN p9.PromotionID IS NOT NULL THEN CONCAT('已有九折優惠 (至 ', p9.EndDate, ')')
        WHEN po.PromotionID IS NOT NULL THEN CONCAT('已有促銷: ', po.PromotionName, ' (', po.DiscountRate*10, '折, 至 ', po.EndDate, ')')
        ELSE '無優惠'
    END AS 促銷狀態
FROM
    Product p
LEFT JOIN
    PromotionProduct pp ON p.ProductID = pp.ProductID
LEFT JOIN
    Promotion p5 ON pp.PromotionID = p5.PromotionID
        AND p5.EndDate >= CURDATE()
        AND p5.PromotionName LIKE '滯銷商品特惠: %'
LEFT JOIN
    Promotion p9 ON pp.PromotionID = p9.PromotionID
        AND p9.EndDate >= CURDATE()
        AND p9.PromotionName LIKE '滯銷商品優惠: %'
LEFT JOIN
    Promotion po ON pp.PromotionID = po.PromotionID
        AND po.EndDate >= CURDATE()
        AND po.PromotionName NOT LIKE '滯銷商品特惠: %'
        AND po.PromotionName NOT LIKE '滯銷商品優惠: %'
WHERE
    p.ExpiryDate IS NOT NULL
    AND p.ExpiryDate BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
    AND p.StockQuantity > 0
ORDER BY
    p.ExpiryDate ASC;

-- 查詢6：檢查滯銷產品（不受歡迎商品）及分級，並為極度滯銷產品自動添加五折優惠
-- 先建立一個暫存表來存儲查詢結果
DROP TEMPORARY TABLE IF EXISTS temp_slow_selling_products;
CREATE TEMPORARY TABLE temp_slow_selling_products AS
SELECT
    p.ProductID AS 產品ID,
    p.ProductName AS 產品名稱,
    p.Category AS 類別,
    IFNULL(SUM(td.Quantity), 0) AS 最近30天銷量,
    CASE
        WHEN IFNULL(SUM(td.Quantity), 0) < 3 THEN '極度滯銷'
        WHEN IFNULL(SUM(td.Quantity), 0) < 6 THEN '滯銷'
        WHEN IFNULL(SUM(td.Quantity), 0) <= 10 THEN '一般'
        ELSE '正常'
    END AS 滯銷等級
FROM
    Product p
LEFT JOIN
    TransactionDetail td ON p.ProductID = td.ProductID
LEFT JOIN
    Transaction t ON td.TransactionID = t.TransactionID AND t.PaymentStatus = 'Paid'
    AND t.TransactionTime >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY
    p.ProductID, p.ProductName, p.Category
HAVING
    最近30天銷量 <= 10;

-- 為極度滯銷產品添加五折優惠（如果不存在）
-- 並為滯銷產品添加九折優惠（如果不存在）
INSERT INTO Promotion (PromotionName, DiscountRate, StartDate, EndDate)
SELECT
    CONCAT('滯銷商品特惠: ', 產品名稱),
    0.50, -- 五折優惠
    CURDATE(), -- 從今天開始
    DATE_ADD(CURDATE(), INTERVAL 14 DAY) -- 為期兩週
FROM
    temp_slow_selling_products tsp
WHERE
    滯銷等級 = '極度滯銷'
    AND NOT EXISTS (
        -- 確保該商品沒有現存有效的促銷活動
        SELECT 1 FROM Promotion p
        JOIN PromotionProduct pp ON p.PromotionID = pp.PromotionID
        WHERE pp.ProductID = tsp.產品ID
        AND p.EndDate >= CURDATE()
        AND p.PromotionName LIKE CONCAT('滯銷商品特惠: ', tsp.產品名稱, '%')
    );

-- 為滯銷產品添加九折優惠（如果不存在）
INSERT INTO Promotion (PromotionName, DiscountRate, StartDate, EndDate)
SELECT
    CONCAT('滯銷商品優惠: ', 產品名稱),
    0.90, -- 九折優惠
    CURDATE(), -- 從今天開始
    DATE_ADD(CURDATE(), INTERVAL 14 DAY) -- 為期兩週
FROM
    temp_slow_selling_products tsp
WHERE
    滯銷等級 = '滯銷'
    AND NOT EXISTS (
        -- 確保該商品沒有現存有效的促銷活動
        SELECT 1 FROM Promotion p
        JOIN PromotionProduct pp ON p.PromotionID = pp.PromotionID
        WHERE pp.ProductID = tsp.產品ID
        AND p.EndDate >= CURDATE()
        AND (p.PromotionName LIKE CONCAT('滯銷商品優惠: ', tsp.產品名稱, '%')
             OR p.PromotionName LIKE CONCAT('滯銷商品特惠: ', tsp.產品名稱, '%'))
    );

-- 將新增的促銷活動與對應的產品關聯起來
INSERT INTO PromotionProduct (PromotionID, ProductID)
SELECT
    p.PromotionID,
    tsp.產品ID
FROM
    Promotion p
JOIN
    temp_slow_selling_products tsp ON p.PromotionName = CONCAT('滯銷商品特惠: ', tsp.產品名稱)
WHERE
    p.StartDate = CURDATE()
    AND p.DiscountRate = 0.50
    AND p.PromotionName LIKE '滯銷商品特惠: %'
    AND NOT EXISTS (
        SELECT 1 FROM PromotionProduct pp
        WHERE pp.PromotionID = p.PromotionID
        AND pp.ProductID = tsp.產品ID
    );

INSERT INTO PromotionProduct (PromotionID, ProductID)
SELECT
    p.PromotionID,
    tsp.產品ID
FROM
    Promotion p
JOIN
    temp_slow_selling_products tsp ON p.PromotionName = CONCAT('滯銷商品優惠: ', tsp.產品名稱)
WHERE
    p.StartDate = CURDATE()
    AND p.DiscountRate = 0.90
    AND p.PromotionName LIKE '滯銷商品優惠: %'
    AND NOT EXISTS (
        SELECT 1 FROM PromotionProduct pp
        WHERE pp.PromotionID = p.PromotionID
        AND pp.ProductID = tsp.產品ID
    );

-- 查詢6：檢查滯銷產品（不受歡迎商品）及分級，並為極度滯銷產品自動添加五折優惠，滯銷產品添加九折優惠
SELECT
    tsp.產品ID,
    tsp.產品名稱,
    tsp.類別,
    tsp.最近30天銷量,
    tsp.滯銷等級,
    CASE
        WHEN p1.PromotionID IS NOT NULL THEN '已添加五折優惠'
        WHEN p2.PromotionID IS NOT NULL THEN '已添加九折優惠'
        ELSE '無'
    END AS 優惠狀態
FROM
    temp_slow_selling_products tsp
LEFT JOIN
    Promotion p1 ON p1.PromotionName = CONCAT('滯銷商品特惠: ', tsp.產品名稱)
        AND p1.EndDate >= CURDATE()
LEFT JOIN
    Promotion p2 ON p2.PromotionName = CONCAT('滯銷商品優惠: ', tsp.產品名稱)
        AND p2.EndDate >= CURDATE()
ORDER BY
    tsp.最近30天銷量 ASC, tsp.產品名稱 ASC;

-- 清理臨時表
DROP TEMPORARY TABLE IF EXISTS temp_slow_selling_products;


