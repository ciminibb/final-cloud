CREATE TABLE Transactions (
    Basket_num VARCHAR(100), -- Flexible size
    Hshd_num BIGINT NULL,
    Purchase_date DATE NULL, -- Added NULL to handle invalid dates
    Product_num VARCHAR(100) NULL, -- Match length with Products table
    Spend DECIMAL(18, 2) NULL, -- Increased precision
    Units BIGINT NULL, -- Changed from INT to BIGINT
    Store_r VARCHAR(100) NULL,
    Week_num BIGINT NULL,
    Year BIGINT NULL,
    FOREIGN KEY (Hshd_num) REFERENCES Households(Hshd_num),
    FOREIGN KEY (Product_num) REFERENCES Products(Product_num)
);
