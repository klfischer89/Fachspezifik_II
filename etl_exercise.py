import csv
import sqlite3
import logging
from datetime import datetime
import re
import matplotlib.pyplot as plt

debugString = "ERROR"

def extract_data():
    debugString = "---START EXTRACTING DATA---"
    print(debugString)

    # extract data from csv file
    with open("data/kunden.csv", newline="", encoding="utf-8") as file:
        kunden = list(csv.DictReader(file))
        debugString = "\033[32m---DATA EXTRACTION SUCCESSFUL---\033[0m"
        print(debugString)
        return kunden

def cleanup_data(kunden):
    debugString = "---START CLEANING UP THE DATA---"
    print(debugString)

    # define fields
    fields = define_fields()

    # check datatype for each field
    check_datatypes(fields)
        
    for kunde in kunden:
        # check for empty fields
        check_empty_fields(fields, kunde)
        # convert customer data, to fit datatypes, fill missing values and check for business rules
        convert_data(kunde)
        # save missing values in a separate list
        save_missing_values(kunde)
        # validate email of customers
        check_email(kunde)
        # check the status of customers
        check_status(kunde)
        # check for names and city containing not only letters
        check_letters(kunde.get("first_name"))
        check_letters(kunde.get("last_name"))
        check_letters(kunde.get("city"))
    # check datatype for each field, after conversion
    check_datatypes(fields)

    debugString = (
    f"\033[32m---CHECKED FOR EMPTY FIELDS---\033[0m\n"
    f"\033[32m---DATA CONVERTED---\033[0m\n"
    f"\033[32m---FILLED MISSING VALUES---\033[0m\n"
    f"\033[32m---REATIN BUSINESS RULES---\033[0m\n"
    f"\033[32m---VALIDATE E-MAIL ADDRESSES---\033[0m\n"
    f"\033[32m---CEHCEKD STATUS---\033[0m\n"
    f"\033[32m---CEHCEKD NAMES---\033[0m\n")

    print(debugString)

    return kunden

def save_missing_values(kunde):
    missingValues = []
    if kunde.get("email") == "None" | "":
        missingValues.append(kunde)
    elif kunde.get("age") == 0:
        missingValues.append(kunde)

def define_fields():
    # define fields
    fields = [
        "customer_id", "first_name", "last_name", "email",
        "city", "age", "registration_date", "status"
    ]
    debugString = f"\033[32m---FIELDS DEFINED---\033[0m"
    print(debugString)
    return fields

def check_email(kunde):
    # Regex-Pattern for Standard-E-Mail-Validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # re.match to check if email correspond to the pattern
    if not re.match(pattern, kunde.get("email")):
        kunde["email"] = "None"

def check_status(kunde):
    allowed_states = {"active", "deleted", "inactive"}
    if kunde.get("status") not in allowed_states:
        kunde["status"] = "inactive"

def check_datatypes(fields):
    for field in fields:
        debugString = f"\033[33m --> Field: {field}, has type: {type(kunden[0].get(field))}\033[0m"
        print(debugString)
    debugString = f"\033[32m---DATATYPES CHECKED---\033[0m"
    print(debugString)

def check_empty_fields(fields, data):
    emtpy_fields = [field for field in fields if not data.get(field, "").strip()]
    if emtpy_fields:
        debugString = f"\033[31m --> Missing Value for customer_id: {data.get("customer_id")}, in field: {emtpy_fields}\033[0m"
        print(debugString)

def check_letters(text):
    pattern = r"^[a-zA-ZäöüÄÖÜß]+$"
    
    if not re.match(pattern, text):
        value = "missing"
    else:
        value = text
    return value

def convert_data(data):
    # convert customer_id to int
        customer_id = int(data.get("customer_id"))
        data["customer_id"] = customer_id

        # fill missing email address with standard value "None"
        email = data.get("email", "") or "None"
        data["email"] = email

        # convert age to int and fill missing values with standard value 0
        age = int(data.get("age", 0) or 0)
        data["age"] = age

        # convert registration_date to date and fill values that are "None", "", "invalid-date" with "1900-01-01"
        date_str = data.get("registration_date")
        if date_str in (None, "", "invalid-date"):
            date_str = "1900-01-01"
        registration_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        data["registration_date"] = registration_date
                
        # check if customer of legal age, otherwise set the status to "inactive"
        if age < 18:
            data["status"] = "inactive"
            debugString = f"\033[31m --> Customer is under 18, customer_id: {data.get("customer_id")}, age: {age}. Status set to {data.get("status")}\033[0m"
            print(debugString)

def create_database(kunden):

    # establish connection to database customers
    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()

    # create table customers
    cursor.execute("""CREATE TABLE IF NOT EXISTS customers(
                    customer_id INTEGER Primary Key,
                    firstname TEXT NOT NULL,
                    lastname TEXT NOT NULL,
                    email TEXT NOT NULL,
                    city TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    registration_date DATE NOT NULL,
                    status TEXT NOT NULL)
                    """)
    conn.commit()

    debugString = "\033[32m---TABLE CREATED IN DATABASE---\033[0m"
    print(debugString)

    conn.close()

def fill_database():

    # establish connection to database customers
    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()

    # insert data into database
    for kunde in kunden:
        cursor.execute("""INSERT INTO customers (customer_id,firstname,lastname,email,city,age,registration_date,status)
                        VALUES (?,?,?,?,?,?,?,?)""",
                        (kunde['customer_id'], kunde['first_name'], kunde['last_name'], kunde['email'], kunde['city'], kunde['age'], kunde['registration_date'], kunde['status']))
        conn.commit()
        debugString = "\033[32m---DATA SAFED IN DATBASE---\033[0m"
        print(debugString)

    # close connection
    conn.close()

def load_data():

    # establish connection to database customers
    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()

    cursor.execute("""SELECT customer_id, age FROM customers""")

    all_customers = cursor.fetchall()

    for kunde in all_customers:
        print(f"ID: {kunde[0]}, Age: {kunde[1]}")

    conn.close()
    return all_customers

def visualize_data(data):

    # extract relevant data
    relevant_data = [kunde[1] for kunde in data]

    # define borders
    category_borders = [0, 20, 40, 60, 80, 100]

    # create histogram
    plt.figure(figsize=(8, 5))
    plt.hist(relevant_data, bins=category_borders, edgecolor="black", color="skyblue", rwidth=0.85)

    # lettering and Design
    plt.title("Age distribution", fontsize=14, fontweight="bold")
    plt.xlabel("Age Categories (Years)", fontsize=12)
    plt.ylabel("Number of Customers", fontsize=12)

    # lettering for borders
    plt.xticks(category_borders)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.show()

def log_etl_conf():
    # monitoring the ETL process on level INFO and log in file etl.log
    logging.basicConfig(filename="etl.log", level=logging.INFO, format="%(asctime) s - %(message) s")

def write_log(e):
    logging.error("Fehler aufgetreten: %s", e)

# main line
if __name__ == "__main__":
    try:
        # load logging configuration
        log_etl_conf()
        # extract data
        kunden = extract_data()
        # clean up data
        kunden = cleanup_data(kunden)
        # create database with table (if not existing) 
        create_database(kunden)
        #insert data into the table
        fill_database(kunden)
        data = load_data()
        visualize_data(data)


    except FileNotFoundError as f:
        debugString = f"\033[31m---FILE NOT FOUND. CHECK PATH OR FILENAME--- {f}\033[0m"
        print(debugString)
        write_log(f)
    except TypeError as t:
        debugString = f"\033[31m---INAPPROPRIATE DATATYPE--- {t}\033[0m"
        print(debugString)
        write_log(t)
    except ValueError as v:
        debugString = f"\033[31m---MISSMATCH FOR DATATYPE--- {v}\033[0m"
        print(debugString)
        write_log(v)
    except KeyError as k:
        debugString = f"\033[31m---KEY DOES NOT EXIST IN DATA--- {k}\033[0m"
        print(debugString)
        write_log(k)
    except OverflowError as o:
        debugString = f"\033[31m---VALUE OUT OF RANGE--- {o}\033[0m"
        print(debugString)
        write_log(o)
    except sqlite3.Error as d:
        debugString = f"\033[31m---DATABASE ERROR--- {d}\033[0m"
        print(debugString)
        write_log(d)
    except sqlite3.OperationalError as oe:
        debugString = f"\033[31m---ERROR READING THE DATABASE--- {oe}\033[0m"
        print(debugString)
        write_log(oe)