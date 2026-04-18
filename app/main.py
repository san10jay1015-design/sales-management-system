import streamlit as st
import pandas as pd
from db import get_connection

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))

        user = cursor.fetchone()

        if user:
            st.session_state.logged_in = True
            st.session_state.role = user[4]
            st.session_state.branch_id = user[3]
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

if not st.session_state.logged_in:
    login()
else:
    st.title("Sales Management Dashboard")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    conn = get_connection()
    cursor = conn.cursor()

    st.subheader("Add New Sale")

    if st.session_state.role == "Admin":
        st.info("You can only add sales for your branch")

    if st.session_state.role == "Super Admin":
        branch_df = pd.read_sql("SELECT * FROM branches", conn)
        branch_options = dict(zip(branch_df['branch_name'], branch_df['branch_id']))
        selected_branch = st.selectbox("Select Branch", list(branch_options.keys()))
        branch_id = branch_options[selected_branch]
    else:
        branch_id = st.session_state.branch_id
        branch_df = pd.read_sql(f"""
            SELECT branch_name FROM branches
            WHERE branch_id = {branch_id}
        """, conn)

        if not branch_df.empty:
            branch_name = branch_df.iloc[0]['branch_name']
        else:
            branch_name = "Unknown"

        st.write(f"Branch: {branch_name}")

    date = st.date_input("Sale Date")
    name = st.text_input("Customer Name")
    mobile = st.text_input("Mobile Number")
    product = st.selectbox("Product", ["DS", "DA", "BA", "FSD"])
    gross = st.number_input("Gross Sales Amount", min_value=0.0)
    status = st.selectbox("Status", ["Open", "Close"])

    if st.button("Add Sale"):
        query = """
        INSERT INTO customer_sales 
        (branch_id, date, name, mobile_number, product_name, gross_sales, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (branch_id, date, name, mobile, product, gross, status))
        conn.commit()
        st.success("Sale added successfully!")
        st.rerun()

    st.subheader("Dashboard Summary")

    if st.session_state.role == "Super Admin":
        kpi_query = """
        SELECT 
            SUM(gross_sales) AS total_sales,
            SUM(received_amount) AS total_received,
            SUM(pending_amount) AS total_pending
        FROM customer_sales
        """
        title_suffix = "in all branches"
    else:
        kpi_query = f"""
        SELECT 
            SUM(gross_sales) AS total_sales,
            SUM(received_amount) AS total_received,
            SUM(pending_amount) AS total_pending
        FROM customer_sales
        WHERE branch_id = {st.session_state.branch_id}
        """

        branch_df = pd.read_sql(f"""
            SELECT branch_name FROM branches
            WHERE branch_id = {st.session_state.branch_id}
        """, conn)

        if not branch_df.empty:
            branch_name = branch_df.iloc[0]['branch_name']
        else:
            branch_name = "Unknown"

        title_suffix = f"in {branch_name} branch"

    kpi_df = pd.read_sql(kpi_query, conn)

    total_sales = kpi_df['total_sales'][0] or 0
    total_received = kpi_df['total_received'][0] or 0
    total_pending = kpi_df['total_pending'][0] or 0

    col1, col2, col3 = st.columns(3)

    col1.metric(f"Total Sales {title_suffix}", f"₹{total_sales}")
    col2.metric(f"Total Received {title_suffix}", f"₹{total_received}")
    col3.metric(f"Total Pending {title_suffix}", f"₹{total_pending}")

    st.subheader("Add Payment")

    if st.session_state.role == "Admin":
        st.info("You can only add payments for your branch")

    if st.session_state.role == "Super Admin":
        sales_df = pd.read_sql("SELECT sale_id, name FROM customer_sales", conn)
    else:
        sales_df = pd.read_sql(
            f"SELECT sale_id, name FROM customer_sales WHERE branch_id = {st.session_state.branch_id}",
            conn
        )

    sale_options = dict(zip(
        sales_df['sale_id'].astype(str) + " - " + sales_df['name'],
        sales_df['sale_id']
    ))

    selected_sale = st.selectbox("Select Sale", list(sale_options.keys()))
    sale_id = sale_options[selected_sale]

    payment_date = st.date_input("Payment Date")
    amount_paid = st.number_input("Amount Paid", min_value=0.0)
    payment_method = st.selectbox("Payment Method", ["Cash", "UPI", "Card"])

    if st.button("Add Payment"):
        query = """
        INSERT INTO payment_splits 
        (sale_id, payment_date, amount_paid, payment_method)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (sale_id, payment_date, amount_paid, payment_method))
        conn.commit()
        st.success("Payment added successfully!")
        st.rerun()

    st.subheader("Customer Sales Data")

    if st.session_state.role == "Super Admin":
        df = pd.read_sql("""
            SELECT cs.*, b.branch_name 
            FROM customer_sales cs
            JOIN branches b ON cs.branch_id = b.branch_id
        """, conn)
    else:
        df = pd.read_sql(f"""
            SELECT cs.*, b.branch_name 
            FROM customer_sales cs
            JOIN branches b ON cs.branch_id = b.branch_id
            WHERE cs.branch_id = {st.session_state.branch_id}
        """, conn)

    if st.session_state.role == "Super Admin":
        branch_df = pd.read_sql("SELECT * FROM branches", conn)
        branch_filter = st.selectbox("Filter by Branch", ["All"] + list(branch_df['branch_name']))

        if branch_filter != "All":
            df = df[df['branch_name'] == branch_filter]

    st.dataframe(df)

    st.subheader("Payment Method Summary")

    payment_df = pd.read_sql("""
        SELECT payment_method, SUM(amount_paid) AS total
        FROM payment_splits
        GROUP BY payment_method
    """, conn)

    st.bar_chart(payment_df.set_index("payment_method"))

    st.subheader("Run Queries")

    query_option = st.selectbox("Select Query", [
        "All Sales",
        "Pending > 5000"
    ])

    if query_option == "All Sales":
        result = pd.read_sql("SELECT * FROM customer_sales", conn)
    else:
        result = pd.read_sql("SELECT * FROM customer_sales WHERE pending_amount > 5000", conn)

    st.dataframe(result)