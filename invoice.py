class Invoice:
    def __init__(self,
                 DocNum:str,
                 terms:str,
                 due_date:str,
                 balance:str,
                 current_company:str,
                 invoice_Id:str,
                 customer_name='',
                 customer_refrence:str=''):
        
        self.DocNum = DocNum
        self.terms = terms
        self.due_date = due_date
        self.balance = balance
        self.current_company = current_company
        self.customer_refrence = customer_refrence
        self.invoice_Id = invoice_Id
        self.customer_name = customer_name

