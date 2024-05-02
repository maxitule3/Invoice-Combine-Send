import database

class UserSettings:

    def __init__(self, tag_number_value=1, cc_email='', invoice_length=5, combiner_input='', combiner_output='', sender_input='', use_custom_body:int=0, custom_body:str=''):
        
        self.tag_number_value = tag_number_value
        self.cc_email = cc_email
        self.invoice_length = invoice_length
        self.combiner_input = combiner_input
        self.combiner_output = combiner_output
        self.sender_input = sender_input
        self.tag_number_value = tag_number_value
        self.use_custom_body = use_custom_body
        self.custom_body = custom_body

    def save_settings(self):
        #Connects to database defined in Database.py
        conn = database.connect()
        cursor = conn.cursor()

        # Check if the customer already exists
        cursor.execute("SELECT * FROM user_settings")
        result = cursor.fetchone()
        if result:
            # Update existing customer
            cursor.execute("UPDATE user_settings SET tag_number_value = ?, cc_email = ?, invoice_length = ?, combiner_input = ?, combiner_output = ?, sender_input = ?, use_custom_body = ?, custom_body = ? ",
                           (self.tag_number_value, self.cc_email, self.invoice_length, self.combiner_input, self.combiner_output, self.sender_input, self.use_custom_body, self.custom_body))
        else:
            # Insert new customer
            cursor.execute("INSERT INTO user_settings (tag_number_value, cc_email, invoice_length, combiner_input, combiner_output, sender_input, use_custom_body, custom_body) VALUES (?,?,?,?,?,?,?,?) ",
                           (self.tag_number_value, self.cc_email, self.invoice_length, self.combiner_input, self.combiner_output, self.sender_input, self.use_custom_body, self.custom_body))
        conn.commit()
        conn.close()

    
        


class UserSettingsFactory:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_user_settings()->UserSettings:
        conn = database.connect()
        cursor = conn.cursor()

        # Check if the settings already exists then close DB Connection
        cursor.execute("SELECT * FROM user_settings")
        result = cursor.fetchone()
        conn.commit()
        conn.close()

        if result:
            # Update existing customer
            return UserSettings(*result)
        else:
            print('didint find user settings')
            user_settings = UserSettings()

            return user_settings
        