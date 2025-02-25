with he as
(
   select
     department_id,
     job_id,
     count(*) filter (where extract(QUARTER from datetime::timestamp) = 1) as Q1,
     count(*) filter (where extract(QUARTER from datetime::timestamp) = 2) as Q2,
     count(*) filter (where extract(QUARTER from datetime::timestamp) = 3) as Q3,
     count(*) filter (where extract(QUARTER from datetime::timestamp) = 4) as Q4
 from hired_employees
 where extract(year from datetime::date) = 2021
 group by 1,2
)
select departments.department, jobs.job, he.Q1, he.Q2, he.Q3, he.Q4
from he inner join departments on he.department_id = departments.id
        inner join jobs on he.job_id = jobs.id
order by 1, 2