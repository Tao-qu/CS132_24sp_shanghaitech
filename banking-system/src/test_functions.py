import DataBase

def get_key (dict, value):
    for k, v in dict.items():
        if v == value:
            return k

def create_account(password):
    if DataBase.ATM_current_account != 0:
        return
    if (password.isdigit()==False) or len(password) < 5 or len(password) > 12:
        return
    new_account = DataBase.generate_random_number()
    DataBase.account_balance[new_account] = '0'
    DataBase.account_password[new_account] = password
    DataBase.ATM_current_account = int(new_account)
    
def close_account():
    if DataBase.ATM_current_account == 0:
        return
    if int(DataBase.account_balance[str(DataBase.ATM_current_account)]) != 0:
        return
    del DataBase.account_balance[str(DataBase.ATM_current_account)]
    del DataBase.account_password[str(DataBase.ATM_current_account)]
    DataBase.ATM_current_account = 0
    
def insert_card(id, password):
    if DataBase.ATM_current_account != 0:
        return
    if id not in DataBase.account_password.keys():
        return
    if DataBase.account_password[id] != password:
        return
    DataBase.ATM_current_account = int(id)
    
def return_card():
    DataBase.ATM_current_account = 0
    
def deposit(num):
    if DataBase.ATM_current_account == 0:
        return
    if num.isdigit()==False:
        return
    if int(num) < 0:
        return
    DataBase.account_balance[str(DataBase.ATM_current_account)] = str(int(DataBase.account_balance[str(DataBase.ATM_current_account)])+int(num))
    
def withdraw(num):
    if DataBase.ATM_current_account == 0:
        return
    if num.isdigit()==False:
        return
    if int(num) < 0:
        return
    if int(DataBase.account_balance[str(DataBase.ATM_current_account)]) < int(num):
        return
    DataBase.account_balance[str(DataBase.ATM_current_account)] = str(int(DataBase.account_balance[str(DataBase.ATM_current_account)])-int(num))
    
def log_in(id, password):
    if id not in DataBase.account_password.keys():
        return
    if DataBase.account_password[id] != password:
        return
    if id in DataBase.app_instances.values():
        return
    DataBase.app_count += 1
    DataBase.app_instances[len(DataBase.app_instances)] = id
    
def log_out(app_id):
    if app_id not in DataBase.app_instances.keys():
        return
    for i in range(app_id, len(DataBase.app_instances)-1):
        DataBase.app_instances[i] = DataBase.app_instances[i+1]
    del DataBase.app_instances[len(DataBase.app_instances)-1]
    DataBase.app_count -= 1
    
def close_app(app_id):
    if app_id not in DataBase.app_instances.keys():
        return
    for i in range(app_id, len(DataBase.app_instances)-1):
        DataBase.app_instances[i] = DataBase.app_instances[i+1]
    del DataBase.app_instances[len(DataBase.app_instances)-1]
    DataBase.app_count -= 1
    
def change_password(new_password,app_id=None):
    if app_id == None:
        if DataBase.ATM_current_account == 0:
            return
        if (new_password.isdigit()==False) or len(new_password) < 5 or len(new_password) > 12:
            return
        DataBase.account_password[str(DataBase.ATM_current_account)] = new_password
    else:
        if app_id not in DataBase.app_instances.keys():
            return
        if (new_password.isdigit()==False) or len(new_password) < 5 or len(new_password) > 12:
            return
        DataBase.account_password[DataBase.app_instances[app_id]] = new_password
        
def transfer_money(receiver_id, num, app_id=None):
    if app_id == None:
        if DataBase.ATM_current_account == 0:
            return
        if receiver_id not in DataBase.account_password.keys():
            return
        if num.isdigit()==False:
            return
        if int(num) < 0:
            return
        if int(DataBase.account_balance[str(DataBase.ATM_current_account)]) < int(num):
            return
        DataBase.account_balance[str(DataBase.ATM_current_account)] = str(int(DataBase.account_balance[str(DataBase.ATM_current_account)])-int(num))
        DataBase.account_balance[receiver_id] = str(int(DataBase.account_balance[receiver_id])+int(num))
    else:
        if app_id not in DataBase.app_instances.keys():
            return
        if receiver_id not in DataBase.account_password.keys():
            return
        if num.isdigit()==False:
            return
        if int(num) < 0:
            return
        if int(DataBase.account_balance[DataBase.app_instances[app_id]]) < int(num):
            return
        DataBase.account_balance[DataBase.app_instances[app_id]] = str(int(DataBase.account_balance[DataBase.app_instances[app_id]])-int(num))
        DataBase.account_balance[receiver_id] = str(int(DataBase.account_balance[receiver_id])+int(num))