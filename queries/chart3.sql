SELECT 
    T.Store_r, COUNT(H.Hshd_num) AS num_homeowners
FROM 
    Transactions T
JOIN 
    Households H ON T.Hshd_num = H.Hshd_num
WHERE
    H.Homeowner = 'Homeowner'
GROUP BY 
    T.Store_r;