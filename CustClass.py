

class customer():

    customers = []

    def __init__(self, name, email, prt):
        self.name = name
        self.email = email
        self.prt = prt


    def new(name, email, prt):
        cust = customer(name, email, prt)
        customer.customers.append(cust)

    def update_prt(name, prt):

        for i in customer.customers:
            if i.name == name:
                i.prt = prt
