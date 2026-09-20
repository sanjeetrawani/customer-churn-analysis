-- Active: 1789800212082@@127.0.0.1@3306@churn_db
USE churn_db;
SELECT * FROM customer_churn;

-- Total customer
SELECT COUNT('Customer_ID') AS total_customer
FROM  customer_churn;

-- Total customer churn
SELECT COUNT(*) AS customer_churn
FROM customer_churn
WHERE Churn = 'Yes';

-- churn rate
SELECT 
ROUND(
SUM(CASE WHEN churn='Yes' THEN 1 ELSE 0 END)*100/
COUNT(*),2)
AS churn_rate
FROM
customer_churn;

-- Average Monthly charges
SELECT
AVG(Monthly_Charges)
FROM customer_churn;

-- Churn by Contract_Type
SELECT 
Contract_Type,COUNT(*)
FROM
customer_churn
GROUP BY Contract_Type;

-- Churn by Internet Service
SELECT 
Internet_Service,COUNT(*)
FROM
customer_churn
GROUP BY Internet_Service;

-- Churn by States
SELECT
State,COUNT(*) AS STATE
FROM
customer_churn
GROUP BY State
ORDER BY 2 DESC;

SELECT
State,COUNT(*) AS STATE
FROM
customer_churn
GROUP BY State
ORDER BY 1 DESC;

SELECT
State,COUNT(*) AS STATE
FROM
customer_churn
GROUP BY State
ORDER BY 1 ASC;


-- Payment method wise customer
SELECT
Payment_Method,COUNT(*) AS Payment_Method
FROM
customer_churn
GROUP BY Payment_Method;


SELECT
Payment_Method,SUM(Monthly_Charges) AS Payment_Method_by_charges
FROM
customer_churn
GROUP BY Payment_Method;

-- Subsciption types wise customer
SELECT
Subscription_Type,COUNT(*) AS Subscription_Type
FROM
customer_churn
GROUP BY Subscription_Type;

-- Highest Revenue State
SELECT
    state,
    SUM(Total_Charges) AS highest_revenue
FROM customer_churn
GROUP BY state
ORDER BY highest_revenue DESC;

-- Average Charges by Constract
SELECT
    Contract_Type,
    AVG(Total_Charges) AS Average_Total_Charges
FROM customer_churn
GROUP BY Contract_Type;

-- Senior citizens Churn
SELECT 
    Senior_Citizen,
    COUNT(*) AS Churned_Customers
FROM customer_churn
WHERE Churn = 'Yes'
GROUP BY Senior_Citizen;


-- Top 10 High Value Customers
-- Top 10 High Value Customers

SELECT
    Customer_ID,
    Customer_Value
FROM customer_churn
ORDER BY Customer_Value DESC
LIMIT 10; 

-- Customers without Tech supports
SELECT COUNT(*)
FROM customer_churn
WHERE Tech_Support = 'No';

SELECT * FROM customer_churn;