WITH department_hires AS (
    SELECT department_id, 
           COUNT(*) AS num_hired
    FROM hired_employees
    WHERE EXTRACT(year from datetime::timestamp) = 2021
    GROUP BY department_id
),
avg_hires AS (
    SELECT AVG(num_hired) AS mean_hires FROM department_hires
)
SELECT d.id, d.department, dh.num_hired
FROM department_hires dh
JOIN departments d ON dh.department_id = d.id
WHERE dh.num_hired > (SELECT mean_hires FROM avg_hires)
ORDER BY dh.num_hired DESC;