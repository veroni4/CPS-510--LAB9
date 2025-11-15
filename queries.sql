--Query 1: returns the intersection of consultants and employees in marketing whos leave request is approved
SELECT e.first_name, e.last_name FROM employee e 
WHERE e.job_title = 'Consultant' AND EXISTS (
SELECT e.first_name, e.last_name, d.department_name, l.leave_type FROM department d, leave l
WHERE d.department_name = 'Marketing' AND l.request_status = 'Approved' );

-- Query 2: Employees who DON'T have approved leave, removing empoyees with approved leave (from subquery)
(SELECT * FROM employee)
MINUS
(SELECT e.* FROM leave l, employee e WHERE l.employee_id = e.employee_id AND l.request_status = 'Approved');

--Query 3: union of all employees who have approved leave requests and an adjustment type
SELECT e.first_name, e.last_name, e.job_title, l.request_status
FROM employee e, leave l
WHERE e.employee_id = l.employee_id AND l.request_status = 'Approved'
UNION
SELECT e.first_name, e.last_name, e.job_title, a.adjustment_type
FROM employee e, adjustment a, payroll_record p
WHERE e.employee_id = p.employee_id AND p.payroll_record_id = a.payroll_record_id;

-- Query 4: count of employees per department
SELECT COUNT(e.Employee_Id) AS Employee_Count,  d.department_name  FROM employee e, department d 
WHERE e.department_id = d.department_id 
GROUP BY  e.department_id, d.department_name;

-- Query 5: Count of employees who's average net_pay is more than 1000
SELECT d.department_name, p.net_pay,
COUNT(e.employee_id) as emp_count
FROM employee e, department d, payroll_record p
WHERE e.employee_id = p.employee_id AND e.department_id = d.department_id
GROUP BY d.department_name, p.net_pay
HAVING AVG(p.net_pay) > 1000;

-- Query 6: max pay for each consultant and manager
SELECT MAX(p.net_pay) as max_pay, e.first_name, e.last_name, e.job_title 
FROM employee e, payroll_record p
GROUP BY e.first_name, e.last_name, e.job_title
HAVING e.job_title = 'Consultant' OR e.job_title = 'Manager'
ORDER BY max_pay;