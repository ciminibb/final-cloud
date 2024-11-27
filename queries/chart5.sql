SELECT 
    H.Income_range, SUM(T.Spend) AS total_spend
FROM 
    Transactions T
JOIN 
    Households H ON T.Hshd_num = H.Hshd_num
GROUP BY 
    H.Income_range
ORDER BY 
    H.Income_range;