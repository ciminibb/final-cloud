SELECT 
    H.Income_range, COUNT(H.Hshd_num) AS income_counts
FROM 
    Households H
GROUP BY 
    H.Income_range;