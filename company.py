import database
from typing import List, Optional

class CompanyToken:
    def __init__(self,
                 company_name:str='',
                 realm_id=None,
                 access_token=None,
                 refresh_token=None,):
        
        self.company_name = company_name
        self.realm_id = realm_id
        self.access_token = access_token
        self.refresh_token = refresh_token


class CompanyTokenFactory:
    def __init__(self) -> None:
        pass
    
    
    @staticmethod
    def get_one(company_name:str)->CompanyToken:
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM company_token WHERE company_name = ?", (company_name,))
        result = cursor.fetchone()
        conn.commit()
        conn.close()
        return CompanyToken(*result)


    @staticmethod
    def upsert(company_token:CompanyToken)->None:
        #Connects to database defined in Database.py

        conn = database.connect()
        cursor = conn.cursor()
        # Check if the customer already exists
        cursor.execute("SELECT * FROM company_token WHERE company_name = ?", (company_token.company_name,))
        result = cursor.fetchone()
        if result:
            # Update existing customer
            cursor.execute("UPDATE company_token SET access_token = ?, refresh_token = ? WHERE realm_id = ?",
                           (company_token.access_token, company_token.refresh_token, company_token.realm_id))
        else:
            # Insert new customer
            cursor.execute("INSERT INTO company_token (company_name, realm_id, access_token, refresh_token) VALUES (?, ?, ?, ?)",
                           (company_token.company_name, company_token.realm_id, company_token.access_token, company_token.refresh_token))
        conn.commit()
        conn.close()


    @staticmethod
    def get_all()->List[CompanyToken]:
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM company_token")
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        company_token_list = []
        for result in results:
            company_token = CompanyToken(company_name=result[0],
                                         realm_id=result[1],
                                         access_token=result[2],
                                         refresh_token=result[3]
                                         )
            company_token_list.append(company_token)
        return company_token_list