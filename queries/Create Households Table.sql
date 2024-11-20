CREATE TABLE Households (
    Hshd_num BIGINT PRIMARY KEY, -- Allows for larger household numbers
    Loyalty CHAR(1) NULL, -- 'Y' or 'N'
    Age_range VARCHAR(100) NULL,
    Marital VARCHAR(100) NULL,
    Income_range VARCHAR(100) NULL,
    Homeowner VARCHAR(100) NULL,
    Hshd_composition VARCHAR(100) NULL,
    HH_size VARCHAR(100) NULL, -- Changed to a small string to bypass pipeline errors on NULL values
    Children VARCHAR(100) NULL
);
