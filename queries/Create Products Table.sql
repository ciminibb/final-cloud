CREATE TABLE Products (
    Product_num CHAR(8) PRIMARY KEY, -- Assuming fixed-length product numbers
    Department VARCHAR(100) NULL,
    Commodity VARCHAR(100) NULL,
    Brand_ty VARCHAR(100) NULL,
    Natural_organic_flag CHAR(1) NULL -- 'Y' or 'N'
);
