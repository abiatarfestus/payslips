import sqlite3
from sqlite3 import Error


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
        print(e)

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
        print(e)


def create_employee(conn, employee):
    """
    Create a new employee into the employees table
    :param conn:
    :param employee:
    :return:
    """
    try:
        sql = """ INSERT INTO employees(employee_code,surname,first_name, file_name, email)
                VALUES(?,?,?,?,?) """
        cur = conn.cursor()
        cur.execute(sql, employee)
        conn.commit()
    except Error as e:
        print(e)
    return


def create_account(conn, account):
    """
    Create a new account
    :param conn:
    :param account:
    :return:
    """
    try:
        sql = """ INSERT INTO accounts(name,email,password,smtp,port)
                VALUES(?,?,?,?,?) """
        cur = conn.cursor()
        cur.execute(sql, account)
        conn.commit()
    except Error as e:
        print(e)
    return


def create_message(conn, message):
    """
    Create a new message
    :param conn:
    :param message:
    :return:
    """
    try:
        sql = """ INSERT INTO messages(subject,message)
                VALUES(?,?) """
        cur = conn.cursor()
        cur.execute(sql, message)
        conn.commit()
    except Error as e:
        print(e)
    return


def update_employee(conn, employee):
    """
    update employee_code, surname, first_name, file_name, and email
    :param conn:
    :param employee:
    :return:
    """
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
    except Error as e:
        print(e)
    return


def update_account(conn, account):
    """
    update email, password, smtp,  and port
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
                WHERE rowid = ?"""
        cur = conn.cursor()
        cur.execute(sql, account)
        conn.commit()
    except Error as e:
        print(e)
    return


def update_message(conn, message):
    """
    update subect, and message
    :param conn:
    :param message:
    :return:
    """
    try:
        sql = """ UPDATE messages
                SET subject = ? ,
                    message = ? 
                WHERE rowid = ?"""
        cur = conn.cursor()
        cur.execute(sql, message)
        conn.commit()
    except Error as e:
        print(e)
    return


def delete_employee(conn, rowid):
    """
    Delete an employee by employee rowid
    :param conn:  Connection to the SQLite database
    :param rowid: rowid of the employee
    :return:
    """
    try:
        sql = "DELETE FROM employees WHERE rowid=?"
        cur = conn.cursor()
        cur.execute(sql, (rowid,))
        conn.commit()
    except Error as e:
        print(e)
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
    except Error as e:
        print(e)
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
        print(e)
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
        print(e)
    return


def select_all_employees(conn):
    """
    Query all rows in the employees table
    :param conn: the Connection object
    :return:
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees")

        rows = cur.fetchall()

        for row in rows:
            pass
    except Error as e:
        print(e)
    return


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

        for row in rows:
            pass
    except Error as e:
        print(e)
    return


def select_all_messages(conn):
    """
    Query all rows in the messages table
    :param conn: the Connection object
    :return:
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM messages WHERE rowid=1;")

        rows = cur.fetchall()

        for row in rows:
            pass
    except Error as e:
        print(e)
    return


def main():
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
                                        port integer NOT NULL
                                    );"""

        sql_create_messages_table = """CREATE TABLE IF NOT EXISTS messages (
                                        subject text NOT NULL,
                                        message text NOT NULL
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

                # create a new employee
                employee = (
                    "A2609198700080",
                    "Abiatar",
                    "Festus Uugwanga",
                    "AbiatarFU.pdf",
                    "Festus.Abiatar@mha.gov.na",
                )
                # create_employee(conn, employee)

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
                    "{month} Payslip",
                    "Good day, {receiver}!\n\nAttached please find your payslip of {month} as received from Salary.\nNB: Please take note that the process to extract your payslip from others and email it to you was done with an automated program. Thus, if you received a wrong payslip, do let me know so I fix it, and I do apologise for that.\n\n Regards,\n\n {sender}",
                    1,
                )
                # create_message(conn, message)
                update_message(conn, message)

        else:
            print("Error! cannot create the database connection.")
    except Error as e:
        print(e)
    return


if __name__ == "__main__":
    main()
