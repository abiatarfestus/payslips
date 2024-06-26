import sqlite3
from sqlite3 import Error
from popups import display_message


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        display_message(repr(e))

    return conn


def create_table(conn, create_table_sql):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except Error as e:
        display_message(repr(e))


def create_employee(conn, employee):
    """
    Create a new employee into the employees table
    :param conn:
    :param employee:
    :return:
    """
    file_name = employee[3]
    if len(file_name) > 4 and file_name[len(file_name) - 4 :].lower() == ".pdf":
        for field in employee:
            if len(field) < 2:
                display_message(
                    "Record not added! No field should be blank or have less than 2 characters."
                )
                return False
        try:
            sql = """ INSERT INTO employees(employee_code,surname,first_name, file_name, email)
                    VALUES(?,?,?,?,?) """
            cur = conn.cursor()
            cur.execute(sql, employee)
            conn.commit()
            display_message("success_create")
        except Error as e:
            display_message(repr(e))
            return False
    else:
        display_message(
            "The file name must be more than 4 characters and end with '.pdf'."
        )
        return False
    return True


def create_account(conn, account):
    """
    Create a new account
    :param conn:
    :param account:
    :return:
    """
    for field in account:
        if field == "":
            display_message("Record not added! No field should be blank.")
            return False
    try:
        sql = """ INSERT INTO accounts(name,email,password,smtp,port, secure)
                VALUES(?,?,?,?,?,?) """
        cur = conn.cursor()
        cur.execute(sql, account)
        conn.commit()
        display_message("success_create")
    except Error as e:
        display_message(repr(e))
        return False
    return True


def create_message(conn, message):
    """
    Create a new message
    :param conn:
    :param message:
    :return:
    """
    try:
        sql = """ INSERT INTO messages(message)
                VALUES(?) """
        cur = conn.cursor()
        cur.execute(sql, message)
        conn.commit()
    except Error as e:
        display_message(repr(e))
    return


def create_office(conn, name):
    """
    Create a new office
    :param conn:
    :param name: office name
    :return:
    """
    if len(name[0]) < 2:
        display_message(
            "Record not added! Office name cannot be blank or less than 2 characters."
        )
        return False
    try:
        sql = """ INSERT INTO offices(name)
                VALUES(?) """
        cur = conn.cursor()
        cur.execute(sql, name)
        conn.commit()
        display_message("success_create")
    except Error as e:
        display_message(repr(e))
        return False
    return True


def update_employee(conn, employee):
    """
    update employee_code, surname, first_name, file_name, and email
    :param conn:
    :param employee:
    :return:
    """
    file_name = employee[3]
    if len(file_name) > 4 and file_name[len(file_name) - 4 :].lower() == ".pdf":
        for field in employee[: len(employee) - 1]:
            if len(field) < 2:
                display_message(
                    "Record not updated! No field should be blank or have less than 2 characters."
                )
                return False
        try:
            sql = """ UPDATE employees
                    SET employee_code = ? ,
                        surname = ? ,
                        first_name = ?,
                        file_name = ?,
                        email = ?
                    WHERE rowid = ?"""
            cur = conn.cursor()
            cur.execute(sql, employee)
            conn.commit()
            display_message("success_update")
        except Error as e:
            display_message(repr(e))
            return False
    else:
        display_message(
            "The file name must be more than 4 characters and end with '.pdf'."
        )
        return False
    return True


def update_account(conn, account):
    """
    update name, email, password, smtp, port, and secure
    :param conn:
    :param account:
    :return:
    """
    try:
        sql = """ UPDATE accounts
                SET name = ? ,
                    email = ? ,
                    password = ? ,
                    smtp = ?,
                    port = ?,
                    secure = ?
                WHERE rowid = ?"""
        cur = conn.cursor()
        cur.execute(sql, account)
        conn.commit()
        display_message("success_update")
    except Error as e:
        display_message(repr(e))
        return False
    return True


def update_message(conn, message):
    """
    update message
    :param conn:
    :param message:
    :return:
    """
    try:
        sql = """ UPDATE messages
                SET message = ? 
                WHERE rowid = ?"""
        cur = conn.cursor()
        cur.execute(sql, message)
        conn.commit()
        display_message("success_update")
    except Error as e:
        display_message(repr(e))
    return


def update_office(conn, office):
    """
    Create a new office
    :param conn:
    :param office: tuple of office name and rowid
    :return:
    """
    for field in office:
        if len(office[0]) < 2:
            display_message(
                "Record not added! Office name cannot be blank or less than 2 characters."
            )
            return False
    try:
        sql = """ UPDATE offices
                SET name = ? 
                WHERE rowid = ?"""
        cur = conn.cursor()
        cur.execute(sql, office)
        conn.commit()
        display_message("success_update")
    except Error as e:
        display_message(repr(e))
        return False
    return True


def delete_employee(conn, employee_code):
    """
    Delete an employee by employee rowid
    :param conn:  Connection to the SQLite database
    :param rowid: rowid of the employee
    :return:
    """
    try:
        sql = "DELETE FROM employees WHERE employee_code=?"
        cur = conn.cursor()
        cur.execute(sql, (employee_code,))
        conn.commit()
        display_message("success_delete")
    except Error as e:
        display_message(repr(e))
    return


def delete_account(conn, rowid):
    """
    Delete an account by account rowid
    :param conn:  Connection to the SQLite database
    :param rowid: rowid of the account
    :return:
    """
    try:
        sql = "DELETE FROM accounts WHERE rowid=?"
        cur = conn.cursor()
        cur.execute(sql, (rowid,))
        conn.commit()
        display_message("success_delete")
    except Error as e:
        display_message(repr(e))
    return


def delete_all_employees(conn):
    """
    Delete all rows in the employees table
    :param conn: Connection to the SQLite database
    :return:
    """
    try:
        sql = "DELETE FROM employees"
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except Error as e:
        display_message(repr(e))
    return


def delete_all_accounts(conn):
    """
    Delete all rows in the accounts table
    :param conn: Connection to the SQLite database
    :return:
    """
    try:
        sql = "DELETE FROM accounts"
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except Error as e:
        display_message(repr(e))
    return


def select_all_employees(conn):
    """
    Query all rows in the employees table
    :param conn: the Connection object
    :return rows:
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees ORDER BY surname")

        rows = cur.fetchall()
        return rows
    except Error as e:
        display_message(repr(e))
    return


def select_employee(conn, employee_code):
    """
    Query for one employee from the employees table
    :param conn: the Connection object
    :param emp_code: employee code
    :return rowid:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT rowid FROM employees WHERE employee_code=?", (employee_code,)
        )

        row = cur.fetchone()
        return row[0]
    except Error as e:
        display_message(repr(e))


def select_all_accounts(conn):
    """
    Query all rows in the accounts table
    :param conn: the Connection object
    :return:
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM accounts")

        rows = cur.fetchall()
        return rows
    except Error as e:
        display_message(repr(e))
    return


def select_account(conn, email):
    """
    Retrieve an account from the accounts table
    :param conn: the Connection object
    :return account:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT rowid, name, email, password, smtp, port, secure FROM accounts WHERE email=?",
            (email,),
        )

        row = cur.fetchone()
        return row
    except Error as e:
        display_message(repr(e))


def select_message(conn):
    """
    Query all rows in the messages table
    :param conn: the Connection object
    :return:
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT rowid, message FROM messages WHERE rowid=1;")

        message = cur.fetchone()
        return message
    except Error as e:
        display_message(repr(e))
    return


def select_all_offices(conn):
    """
    Query all rows in the offices table
    :param conn: the Connection object
    :return offices:
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM offices")

        offices = cur.fetchall()
        return offices
    except Error as e:
        display_message(repr(e))


def select_office(conn, name):
    """
    Retrieve an office from the offices table
    :param conn: the Connection object
    :param name: name of offices
    :return office:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT rowid, name FROM offices WHERE name=?",
            (name,),
        )

        row = cur.fetchone()
        return row
    except Error as e:
        display_message(repr(e))


def drop_table(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return


def setup_db():
    try:
        database = "mydb.db"

        sql_create_employees_table = """ CREATE TABLE IF NOT EXISTS employees (
                                            employee_code text NOT NULL UNIQUE,
                                            surname text NOT NULL,
                                            first_name text NOT NULL,
                                            file_name text NOT NULL UNIQUE,
                                            email text NOT NULL
                                        ); """

        sql_create_accounts_table = """CREATE TABLE IF NOT EXISTS accounts (
                                        name text NOT NULL,
                                        email text NOT NULL UNIQUE,
                                        password text NOT NULL,
                                        smtp text NOT NULL,
                                        port integer NOT NULL,
                                        secure integer NOT NULL
                                    );"""

        sql_create_messages_table = """CREATE TABLE IF NOT EXISTS messages (
                                        message text NOT NULL
                                    );"""

        sql_create_offices_table = """CREATE TABLE IF NOT EXISTS offices (
                                        name text NOT NULL
                                    );"""

        # create a database connection
        conn = create_connection(database)

        # create tables
        if conn is not None:
            with conn:
                # create employees table
                create_table(conn, sql_create_employees_table)

                # create accounts table
                create_table(conn, sql_create_accounts_table)

                # create messages table
                create_table(conn, sql_create_messages_table)

                # create offices table
                create_table(conn, sql_create_offices_table)

                # create a new employee
                employee = (
                    "A2609198700080",
                    "Abiatar",
                    "Festus Uugwanga",
                    "Abiatar.pdf",
                    "Festus.Abiatar@mha.gov.na",
                )
                # employees = emps
                # for employee in employees:
                #     create_employee(conn, employee)
                # update_employee(conn, employee)

                # create a new account
                account = (
                    "Abiatar",
                    "username@gmail.com",
                    "lgcbbvi^^jvsxdtlav",
                    "smtp.gmail.com",
                    "465",
                )
                # create_account(conn, account)

                # create a new message
                message = (
                    "Good day, {receiver}!\n\nAttached please find your payslip of {month} as received from Salary.\nNB: Please take note that the process to extract your payslip from others and email it to you was done with an automated program. Thus, if you received a wrong payslip, do let me know so I fix it, and I do apologise for that.\n\nRegards,\n\n{sender}",
                )
                # create_message(conn, message)
                # update_message(conn, message)
                #drop_table(conn, "DROP TABLE accounts")

        else:
            display_message("Error! cannot create the database connection.")
    except Error as e:
        display_message(repr(e))
    return


if __name__ == "__main__":
    setup_db()
