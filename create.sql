CREATE TABLE EMPLOYEE (
Employee_Id NUMBER PRIMARY KEY,
Department_Id NUMBER REFERENCES Department(Department_Id),
First_Name VARCHAR2(30),
Last_Name VARCHAR2(30),
Job_Title VARCHAR2(30),
Hire_Date DATE,
Bank_Account NUMBER UNIQUE NOT NULL,
Email VARCHAR2(30) UNIQUE

);

--- DEPARTMENT TABLE
CREATE TABLE DEPARTMENT(
Department_Id NUMBER PRIMARY KEY,
Department_Name VARCHAR2(50) UNIQUE
);


--- LEAVE TABLE
-- Using check constraint as ENUM
CREATE TABLE LEAVE(
Leave_Id NUMBER PRIMARY KEY,
Employee_Id NUMBER REFERENCES Employee(Employee_Id),
Leave_Type VARCHAR2(7) CHECK(Leave_Type IN ('Paid', 'Unpaid', 'Sick')),
Request_Status VARCHAR2(8) CHECK(Request_Status IN ('Approved', 'Denied', 'Pending')),
Request_Date DATE,
End_Date DATE,
Start_Date DATE
);


--- PAYROLL_RECORD TABLE

CREATE TABLE PAYROLL_RECORD(
Payroll_Record_Id NUMBER PRIMARY KEY,
Employee_Id NUMBER REFERENCES Employee(Employee_Id),
Payroll_Period_Id NUMBER,
Gross_Pay FLOAT,
Net_Pay NUMBER,
Total_Adjustment NUMBER,
Payout_Date DATE
);


--- PAYROLL_PERIOD TABLE
CREATE TABLE PAYROLL_PERIOD(
Payroll_Period_Id NUMBER PRIMARY KEY,
Period_Name VARCHAR2(30) CHECK(Period_Name IN ('Monthly', 'Bi-Weekly')),
Start_Date DATE,
End_Date DATE
);


--- ADJUSTMENT TABLE
CREATE TABLE ADJUSTMENT(
Adjustment_Id NUMBER PRIMARY KEY,
Adjustment_Type VARCHAR(10) CHECK(Adjustment_Type IN ('Overtime', 'CPP', 'Insurance',
'Tax')),
Payroll_Record_Id NUMBER REFERENCES Payroll_Record(Payroll_Record_Id),Amount NUMBER);
