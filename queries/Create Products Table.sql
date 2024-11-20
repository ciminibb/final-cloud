CREATE TABLE Products (
    Product_num VARCHAR(50) PRIMARY KEY, -- Increased length for flexibility
    Department VARCHAR(100) NULL,
    Commodity VARCHAR(100) NULL,
    Brand_ty VARCHAR(100) NULL,
    Natural_organic_flag CHAR(1) NULL -- 'Y' or 'N'
);
