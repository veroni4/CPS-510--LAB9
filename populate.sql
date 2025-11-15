--Populate Employee Table
INSERT INTO Employee (Employee_Id, Department_Id, First_Name, Last_Name, Job_Title,
Hire_Date, Bank_Account, Email) VALUES (4506, 3, 'Bob', 'Johnson', 'Manager', '2006-10-19', 48832065, 'bob.johnson@work.com');
INSERT INTO Employee (Employee_Id, Department_Id, First_Name, Last_Name, Job_Title,
Hire_Date, Bank_Account, Email) VALUES (4507, 2, 'Alice', 'Cook', 'Developer', '2011-06-22', 58993947, 'alice.cook@work.com');
INSERT INTO Employee (Employee_Id, Department_Id, First_Name, Last_Name, Job_Title,
Hire_Date, Bank_Account, Email) VALUES (4508, 1, 'Shelly', 'Smith', 'Consultant', '2025-05-10', 78612400, 'shelly.smith@work.com');
INSERT INTO Employee (Employee_Id, Department_Id, First_Name, Last_Name, Job_Title,
Hire_Date, Bank_Account, Email) VALUES (4513,1,'Isabelle','Young', 'Consultant','2020-03-15', 42105382, 'isabelle.young@work.com');
INSERT INTO Employee (Employee_Id, Department_Id, First_Name, Last_Name, Job_Title,
Hire_Date, Bank_Account, Email) VALUES (4509,2, 'Mark', 'Fisher', 'Developer', '2018-01-15', 42294601, 'mark.fisher@work.com');
INSERT INTO Employee (Employee_Id, Department_Id, First_Name, Last_Name, Job_Title,
Hire_Date, Bank_Account, Email) VALUES (4510,3,'Lana', 'Tran', 'Director', '2015-05-01', 96021801, 'lana.tran@work.com');
INSERT INTO Employee (Employee_Id, Department_Id, First_Name, Last_Name, Job_Title,
Hire_Date, Bank_Account, Email) VALUES (4511, 4, 'Jerry','Lee', 'Manager','2016-01-30', 9367401, 'jerry.lee@work.com');
INSERT INTO Employee (Employee_Id, Department_Id, First_Name, Last_Name, Job_Title,
Hire_Date, Bank_Account, Email) VALUES (4512,1,'Daniel','Riccardo', 'Manger', '2021-09-15', 49634101, 'daniel.riccardo@work.com');
INSERT INTO Employee (Employee_Id, Department_Id, First_Name, Last_Name, Job_Title,
Hire_Date, Bank_Account, Email) VALUES (4514, 4, 'Andy', 'Willow', 'Recuiter', '2024-08-10', 44874668, 'andy.willow@work.com');
INSERT INTO Employee (Employee_Id, Department_Id, First_Name, Last_Name, Job_Title,
Hire_Date, Bank_Account, Email) VALUES (4515, 1, 'Sofia', 'Cain', 'Consultant', '2022-10-21', 45028691, 'sofia.cain@work.com');

--Populate Department Table
INSERT INTO Department (Department_Id, Department_Name) VALUES (1, 'Marketing');
INSERT INTO Department (Department_Id, Department_Name) VALUES (2, 'Engineering');
INSERT INTO Department (Department_Id, Department_Name) VALUES (3, 'Operations');
INSERT INTO Department (Department_Id, Department_Name) VALUES (4, 'Human Resources');

--Populate Leave Table
INSERT INTO Leave (Leave_Id, Employee_Id, Leave_Type, Request_Status, Request_Date,
Start_Date, End_Date) VALUES (86742, 4506, 'Paid', 'Approved', '2025-05-12', '2025-08-10','2025-08-14');
INSERT INTO Leave (Leave_Id, Employee_Id, Leave_Type, Request_Status, Request_Date,
Start_Date, End_Date) VALUES (283357, 4507, 'Paid', 'Denied', '2025-09-08', '2025-09-09', '2025-09-30');
INSERT INTO Leave (Leave_Id, Employee_Id, Leave_Type, Request_Status, Request_Date,
Start_Date, End_Date) VALUES (435675, 4508, 'Unpaid', 'Pending', '2025-09-09', '2026-01-12', '2026-01-15');
INSERT INTO Leave (Leave_Id, Employee_Id, Leave_Type, Request_Status, Request_Date,
Start_Date, End_Date) VALUES (86741, 4513, 'Paid', 'Denied', '2025-05-12', '2025-05-10', '2025-05-14');
INSERT INTO Leave (Leave_Id, Employee_Id, Leave_Type, Request_Status, Request_Date,
Start_Date, End_Date) VALUES (86744, 4509, 'Sick', 'Approved','25-01-05', '2025-01-21', '2025-01-19');
INSERT INTO Leave (Leave_Id, Employee_Id, Leave_Type, Request_Status, Request_Date,
Start_Date, End_Date) VALUES (86739, 4511, 'Unpaid', 'Approved', '2025-03-01', '2025-04-02', '2025-03-29');
INSERT INTO Leave (Leave_Id, Employee_Id, Leave_Type, Request_Status, Request_Date,
Start_Date, End_Date) VALUES (86738, 4514, 'Paid', 'Approved', '25-04-05', '25-05-20', '2025-05-08');

--Populate Payroll_Record Table
INSERT INTO Payroll_Record (Payroll_Record_Id, Employee_Id, Payroll_Period_Id, Gross_Pay,
Net_Pay, Total_Adjustment, Payout_Date) VALUES (011, 4506, 001, 9000, 9600, 600, '2025-09-30');
INSERT INTO Payroll_Record (Payroll_Record_Id, Employee_Id, Payroll_Period_Id, Gross_Pay,
Net_Pay, Total_Adjustment, Payout_Date) VALUES (012, 4507, 002, 5000, 4550, -450, '2025-09-16');
INSERT INTO Payroll_Record (Payroll_Record_Id, Employee_Id, Payroll_Period_Id, Gross_Pay,
Net_Pay, Total_Adjustment, Payout_Date) VALUES (013, 4508, 003, 5500, 5400, -100, '2025-10-16');
INSERT INTO Payroll_Record (Payroll_Record_Id, Employee_Id, Payroll_Period_Id, Gross_Pay,
Net_Pay, Total_Adjustment, Payout_Date) VALUES (014, 4509, 003, 5500, 5000, -500, '2025-10-16');
INSERT INTO Payroll_Record (Payroll_Record_Id, Employee_Id, Payroll_Period_Id, Gross_Pay,
Net_Pay, Total_Adjustment, Payout_Date) VALUES (015, 4511, 004, 6000, 6800, 800, '2025-02-02');

--Populate Payroll_Period Table
INSERT INTO Payroll_Period (Payroll_Period_Id, Period_Name, Start_Date, End_Date) VALUES
(001, 'Monthly', '2025-09-01', '2025-09-30');
INSERT INTO Payroll_Period (Payroll_Period_Id, Period_Name, Start_Date, End_Date) VALUES
(002, 'Bi-Weekly', '2025-09-01', '2025-09-15');
INSERT INTO Payroll_Period (Payroll_Period_Id, Period_Name, Start_Date, End_Date) VALUES
(003, 'Monthly', '2025-09-15', '2025-10-15');
INSERT INTO Payroll_Period (Payroll_Period_Id, Period_Name, Start_Date, End_Date) VALUES
(004, 'Monthly', '2025-01-01', '2025-02-01');

--Populate Adjustment Table
INSERT INTO Adjustment (Adjustment_Id, Adjustment_Type, Payroll_Record_Id, Amount) VALUES
(501,'Overtime', 011, 800);
INSERT INTO Adjustment (Adjustment_Id, Adjustment_Type, Payroll_Record_Id, Amount) VALUES
(502, 'CPP', 012, -450);
INSERT INTO Adjustment (Adjustment_Id, Adjustment_Type, Payroll_Record_Id, Amount) VALUES
(503, 'Insurance', 013, -200);
INSERT INTO Adjustment (Adjustment_Id, Adjustment_Type, Payroll_Record_Id, Amount) VALUES
(504, 'CPP', 014, -500);
INSERT INTO Adjustment (Adjustment_Id, Adjustment_Type, Payroll_Record_Id, Amount) VALUES
(505, 'Overtime', 015, 1000);
INSERT INTO Adjustment (Adjustment_Id, Adjustment_Type, Payroll_Record_Id, Amount) VALUES
(506, 'Insurance', 015, -200);