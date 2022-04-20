class func:

    def doSend():
        if (customer.prt) == True:
            print(f'Print {customer.name}\'s invoice')
        elif (customer.prt) == False:
            print(f'Send {customer.name}\'s email to {customer.email}')
        else:
            print('Invalid argument given')

    def doEmail():
        print(f'Send email to {customer.email}')

    def doPrint():
        print(f'Print {customer.name}\'s invoice')


class customer:
    def __init__(self, name, email, prt):
        self.name = name
        self.email = email
        self.prt = prt

data = []

data.append(customer('brendan', 'breh@bren.com', False))
data.append(customer('max', 'max@gmail.com', True))
data.append(customer('brian', 'brianitule@gmail.com', False))

for customer in data:
    func.doPrint()





exit()