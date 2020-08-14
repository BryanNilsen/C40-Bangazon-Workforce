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
delete from hrapp_trainingprogram;
select c.id,
    c.make,
    c.purchase_date,
    c.decommission_date
from hrapp_computer c;
select e.id,
    e.first_name,
    e.last_name,
    ec.computer_id
from hrapp_employee e
    left join hrapp_employeecomputer ec on e.id = ec.employee_id
where ec.computer_id ISNULL
select c.id,
    c.make,
    ec.computer_id
from hrapp_computer c
    left join hrapp_employeecomputer ec on c.id = ec.computer_id
where ec.computer_id ISNULL
select ec.id,
    ec.computer_id,
    c.make,
    c.purchase_date,
    c.decommission_date
from hrapp_employeecomputer ec
    join hrapp_computer c on c.id = ec.computer_id
where ec.computer_id = 1;
SELECT c.id,
    c.make,
    c.purchase_date,
    c.decommission_date,
    e.first_name || ' ' || e.last_name as fullname,
    e.id as employee_id,
    ec.assign_date
FROM hrapp_computer c
    LEFT JOIN hrapp_employeecomputer ec on ec.computer_id = c.id
    LEFT JOIN hrapp_employee e on ec.employee_id = e.id
WHERE ec.unassign_date ISNULL;
SELECT d.id,
    d.name,
    d.budget,
    e.first_name || ' ' || e.last_name AS fullname,
    e.id as employee_id
FROM hrapp_department d
    LEFT JOIN hrapp_employee e ON e.department_id = d.id
WHERE d.id = 1;
-- EMPLOYEE DETAIL
SELECT e.id,
    e.first_name,
    e.last_name,
    e.start_date,
    e.is_supervisor,
    d.id AS department_id,
    d.name AS department_name,
    c.id AS computer_id,
    c.make AS computer_make,
    tp.title AS training_title,
    tp.id AS training_id
FROM hrapp_employee e
    LEFT JOIN hrapp_department d ON e.department_id = d.id
    LEFT JOIN hrapp_employeecomputer ec ON e.id = ec.employee_id
    LEFT JOIN hrapp_computer c ON ec.computer_id = c.id
    LEFT JOIN hrapp_employeetrainingprogram etp ON etp.employee_id = e.id
    LEFT JOIN hrapp_trainingprogram tp ON etp.trainingprogram_id = tp.id
WHERE ec.unassign_date ISNULL
    AND e.id = 3;
-- insert into hrapp_employeetrainingprogram ('employee_id', 'trainingprogram_id')
-- values (12, 5)
SELECT c.id,
    c.make,
    c.purchase_date,
    c.decommission_date
FROM hrapp_computer c
WHERE c.decommission_date ISNULL;
-- UPDATE EMPLOYEECOMPUTER
UPDATE hrapp_employeecomputer
SET unassign_date = "2018-05-05"
WHERE id = 1;
SELECT e.id,
    e.first_name,
    e.last_name,
    e.start_date,
    e.is_supervisor,
    d.id AS department_id,
    d.name AS department_name,
    c.id AS computer_id,
    c.make AS computer_make
FROM hrapp_employee e
    LEFT JOIN hrapp_department d ON e.department_id = d.id
    LEFT JOIN hrapp_employeecomputer ec ON e.id = ec.employee_id
    LEFT JOIN hrapp_computer c ON ec.computer_id = c.id
WHERE ec.unassign_date ISNULL;
SELECT e.id,
    e.first_name,
    e.last_name,
    e.start_date,
    e.is_supervisor,
    d.id AS department_id,
    d.name AS department_name,
    c.id AS computer_id,
    c.make AS computer_make,
    tp.title AS training_title,
    tp.id AS training_id
FROM hrapp_employee e
    LEFT JOIN hrapp_department d ON e.department_id = d.id
    LEFT JOIN hrapp_employeecomputer ec ON e.id = ec.employee_id
    LEFT JOIN hrapp_computer c ON ec.computer_id = c.id
    LEFT JOIN hrapp_employeetrainingprogram etp ON etp.employee_id = e.id
    LEFT JOIN hrapp_trainingprogram tp ON etp.trainingprogram_id = tp.id
WHERE ec.unassign_date ISNULL;