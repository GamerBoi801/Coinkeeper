# **Coinkeeper**
# **Author:** __MSK(GamerBOi801)__
## Version 1.0
## Date: 10/06/2024


## Geting Started:
####  My Project **CoinKeeper** is a webApp made in Flask (python web framework) and helps individuals track their finances  by inputting their Expenses, Incomes, Investments Into the tracker. In Addtion to this users can keep track of their Investments, income and expenses by reviewing their logs and seeing each"s grpahical representation which was made possible by using a JavaScript FrameWork called chart.js. I utilised the Functions from the helpers file from the pset9 Finance file, the layout and the db from the same Finance pset. and the cs50 python library for the SQL. Moreover I used AI to help me design the frontend of CoinKeeper. 

#### **Homepage:** After the user presents their creditionals they are redirected to the home screen where the user is greeted by the app and their bank balance is shown on the top right side. The Homepage gives the user 3 options : First the page to view their Transaction History Secondly, to manage their income and third to View their Investment History.
![Screenshot of the Homepage](HomePage.png)

#### **Features:** Coinkeeper is equipped with a User Friendly  Interface and contains the features to Manage, Record, Display in a a graphical view their Past and Future incomes, Investments and Expenses. Furthermore it  allows the users to change their Username and Passwords in the Account Settings page.

#### **History Features:** Another Feature is the History Page that allows users to track what transactions they have made into the app, For example How many investments they have made it's durations and what type etc. It shows all of the records in a tabular form and then shows it graphically just south of the table, with date invested on the x-axis and the amount invested on each repsective date on the y-axis in the form of USD. 
![Screeshot of the History Page](Investment_History.png)

#### This project is made to help busy individuals provide a comprehensive view of one's spending habit making it easier to identify areas where they can cut costs or stay within one's budget Moreover it can enable people to make informed decisions.

## Database Schema _(finance.db)_ 
### User (stores the user info)
* **id** (integer, Primary Key)
*  **username** (string).0

* **password** (hashed password string)

### Bank (stores the user bank amount)
* **bank_id** (integer, Primary Key)
* **id** (integer, Foreign Key)
* **amount** (Decimal)

### Income(Stores each of user income logs & uniquely identifies by the id)
* **income_id** (integer, Primary Key)
* **id** (integer, Foreign Key)
* **amount** (Decimal)
* **Date** (Date)

### investments(Stores Each of user investment & uniquely identifies by the id)
* **invesment_id** (integer, Primay Key)
* **id** (integer, Foreign Key)
* **type** (CHECK, options(Stocks', 'Real Estate', 'Mutual Funds', 'Bonds'))
* **amount** (Decimal)
* **returns %** (Decimal stores %)
* **start_date** (DATE when invested)
* **end_date** (DATE when investment ended)
* **duration** (Integer, stores date which is differnce b/w end and start date)

### Expenses (Stores each of user expenses uniquely identified by the id)
* **expense_id** (integer, Foreign Key)
* **id** (integer, Foriegn Key)
* **amount** (Deicmal)
* **Category** (CHECK, options('personal expenses', 'leisure', 'investment'))
* **date** (Date)

## Evaluation
### Thank You! For your time to read about our project. We hope you find it useful.If you have any questions and suggestions, Please don't hesitate to reach out to me.

## Email: **MSK_working@proton.me**
