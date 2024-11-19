CREATE TABLE Households (
    Hshd_num INT PRIMARY KEY,
    Loyalty CHAR(1) NULL, -- 'Y' or 'N'
    Age_range VARCHAR(100) NULL,
    Marital VARCHAR(100) NULL,
    Income_range VARCHAR(100) NULL,
    Homeowner VARCHAR(100) NULL,
    Hshd_composition VARCHAR(100) NULL,
    HH_size INT NULL,
    Children VARCHAR(100) NULL
);
