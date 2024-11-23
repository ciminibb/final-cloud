SELECT
    H.Hshd_num,
    T.Basket_num,
    T.Purchase_date,
    T.Product_num,
    P.Department,
    P.Commodity,
    P.Brand_ty,
    P.Natural_organic_flag,
    T.Spend,
    T.Units,
    T.Store_r,
    T.Week_num,
    T.Year,
    H.Loyalty,
    H.Age_range,
    H.Marital,
    H.Income_range,
    H.Homeowner,
    H.Hshd_composition,
    H.HH_size,
    H.Children
FROM
    Households H
JOIN
    Transactions T ON H.Hshd_num = T.Hshd_num
JOIN
    Products P ON T.Product_num = P.Product_num
WHERE
    H.Hshd_num = ?
ORDER BY
    P.Commodity;