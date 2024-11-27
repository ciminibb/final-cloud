SELECT 
    H.Children, SUM(T.Spend) AS total_spend, SUM(T.Units) AS total_units
FROM 
    Transactions T
JOIN 
    Households H ON T.Hshd_num = H.Hshd_num
GROUP BY 
    H.Children
ORDER BY 
    H.Children;