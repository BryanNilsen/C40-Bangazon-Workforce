select e.id,
    e.first_name,
    e.last_name,
    e.start_date,
    e.is_supervisor,
    d.id as department_id,
    d.name as department_name,
    c.id as computer_id,
    c.make as computer_make
from hrapp_employee e
    left join hrapp_department d on e.department_id = d.id
    left join hrapp_employeecomputer ec on e.id = ec.employee_id
    left join hrapp_computer c on ec.computer_id = c.id;
select d.id,
    d.name,
    d.budget,
    COUNT(e.id) as employee_count
FROM hrapp_department d
    JOIN hrapp_employee e ON d.id = e.department_id
GROUP BY d.name;
select t.id,
    t.title,
    t.start_date,
    t.end_date,
    t.capacity
from hrapp_trainingprogram t
where t.end_date >= DATETIME('now');

