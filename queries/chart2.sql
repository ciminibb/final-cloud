SELECT 
    H.Homeowner, SUM(T.Units) AS total_units
FROM 
    Transactions T
JOIN 
    Households H ON T.Hshd_num = H.Hshd_num
GROUP BY 
    H.Homeowner