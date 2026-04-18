# Sales Management System

## Overview

This project is a branch-based sales management system built using MySQL, Python, and Streamlit.
It helps track sales, manage customer payments, and monitor pending amounts across different branches.

## Features

* Add and manage sales records
* Handle split payments for each sale
* Automatic calculation of received and pending amounts using triggers
* Role-based login (Admin and Super Admin)
* Dashboard showing total sales, received amount, and pending amount
* Branch-wise filtering (for Super Admin)
* Payment method summary
* SQL query execution section

## Technologies Used

* Python
* MySQL
* Streamlit

## How to Run

1. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:

   ```bash
   streamlit run app/main.py
   ```

## Notes

* Make sure MySQL server is running
* Update database credentials in `db.py` if needed
* Import sample data before running the app

## Author

Sanjay S
