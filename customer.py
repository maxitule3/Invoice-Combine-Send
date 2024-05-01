import database
from typing import List

class Customer:
    def __init__(self, name:str, email:str='', wants_invoice_printed:int=0) -> None:
        self.name = name
        self.email = email
        self.wants_invoice_printed = wants_invoice_printed


class CustomerFactory:
    def __init__(self)-> None:
        pass

    @staticmethod
    def get_all()->List[Customer]:
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers")
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        customer_list = []

        for result in results:
            customer = Customer(name=result[0], email=result[1], wants_invoice_printed=result[2])
            customer_list.append(customer)

        return customer_list

    @staticmethod
    def create_customer(customer_name:str, customer_email:str='', wants_invoice_printed:int= 0)->Customer:
        customer = Customer(customer_name, customer_email, wants_invoice_printed)

        return customer

    @staticmethod
    def get_customer_by_name(customer_name:str)-> Customer:
        #Connects to database defined in Database.py
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT customer_name, customer_email, wants_invoice_printed FROM customers WHERE customer_name = ?", (customer_name,))
        result = cursor.fetchone()
        conn.close()


        return Customer(*result)
        

    @staticmethod
    def upsert_customer(customer:Customer)->None:
        #Connect to database defined in Database.py
        conn = database.connect()
        cursor = conn.cursor()
        # Check if the customer already exists
        cursor.execute("SELECT * FROM customers WHERE customer_name = ?", (customer.name,))
        result = cursor.fetchone()
        if result:
            # Update existing customer
            cursor.execute("UPDATE customers SET customer_name=?, customer_email=? WHERE customer_name =?",
                           (customer.name, customer.email, customer.name))
        else:
            # Insert new customer
            cursor.execute("INSERT INTO customers (customer_name, customer_email, wants_invoice_printed) VALUES (?, ?, ?)",
                           (customer.name, customer.email, customer.wants_invoice_printed))
        conn.commit()
        conn.close()

    @staticmethod
    def bulk_upsert_print_status(customers_list:List[Customer])->None:
        conn = database.connect()
        cursor = conn.cursor()

        try:
            for customer in customers_list:
                cursor.execute("UPDATE customers SET wants_invoice_printed=? WHERE customer_name =?",
                            (customer.wants_invoice_printed, customer.name))
                conn.commit()
        except:
            conn.close()
  
        conn.close()

    @staticmethod
    def get_empty_cutomer()->Customer:
        empty_customer_object = Customer(name='')

        return empty_customer_object

