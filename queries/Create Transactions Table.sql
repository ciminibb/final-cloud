CREATE TABLE Transactions (
    Basket_num CHAR(8),
    Hshd_num INT NULL,
    Purchase_date DATE,
    Product_num CHAR(8),
    Spend DECIMAL(10, 2) NULL, -- To handle monetary values
    Units INT NULL,
    Store_r VARCHAR(100) NULL,
    Week_num INT NULL,
    Year INT NULL,
    PRIMARY KEY (Basket_num, Product_num, Purchase_date),
    FOREIGN KEY (Hshd_num) REFERENCES Households(Hshd_num),
    FOREIGN KEY (Product_num) REFERENCES Products(Product_num)
);
