import sys
import DataBase
import init

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import *

from datetime import datetime
current_datetime = datetime.now()
current_datetime = current_datetime.replace(microsecond=0)

# This function determines whether a new message has been received
def is_received_new_message(oldTimeStamp:int, oldServerMessage:str, Msgunprocessed:bool = False)->bool:
    zmqThread = init.zmqThread
    if(Msgunprocessed):
        return True
    else:
        if(oldTimeStamp == zmqThread.messageTimeStamp and 
           oldServerMessage == zmqThread.receivedMessage):
            return False
        else:
            return True

def check_messages():
    from app import applog
    from ATM import ATM_current_window
    zmqThread = init.zmqThread
    
    global timeStamp, serverMessage, messageUnprocessed
    timeStamp = init.timeStamp
    serverMessage = init.serverMessage
    messageUnprocessed = init.messageUnprocessed
    if is_received_new_message(timeStamp, serverMessage, messageUnprocessed):
        if not messageUnprocessed:
            timeStamp = zmqThread.messageTimeStamp
            serverMessage = zmqThread.receivedMessage
        messageUnprocessed = False

        # On ATM
        if "create_account@" in serverMessage:
            password = serverMessage.split("@")[1]  # 从消息中提取密码
            ATM_current_window.help(auto_password=password)  # 使用自动密码

        if serverMessage == "close_account":
            ATM_current_window.close()  
        
        if "insert_card@" in serverMessage:
            parts = serverMessage.split("@")
            account_id = parts[1]
            ATM_current_window.auto_login(account_id, DataBase.account_password[account_id])

        if serverMessage == "return_card":
            ATM_current_window.out()  

        if "deposit_cash@" in serverMessage:
            # amount = float(serverMessage.split("@")[1])
            amount = serverMessage.split("@")[1]
            ATM_current_window.auto_recharge(amount) 

        if "withdraw_cash@" in serverMessage:
            parts = serverMessage.split("@")
            amount = parts[1]
            password = parts[2]
            ATM_current_window.auto_withdraw(amount, password)

        # app
        if(serverMessage == "open_app"):
            DataBase.app_count += 1
            new_x = DataBase.initial_x + (DataBase.app_count - 1) * DataBase.increment_x
            app_instance = applog(new_x, DataBase.initial_y)
            app_instance.show()
            app_name = f"app{DataBase.app_count}"
            DataBase.app_instances[app_name] = app_instance
            for name, instance in DataBase.app_instances.items():
                setattr(instance, 'is_active', False)
            zmqThread.sendMsg(f"app_opened#{DataBase.app_count}")

        if "log_in@" in serverMessage:
            parts = serverMessage.split("@")
            account_id = parts[1]
            password = parts[2].split("#")[0]
            app_id = int(parts[2].split("#")[1])

            for name, instance in DataBase.app_instances.items():
                setattr(instance, 'is_active', False)
            app_name = f"app{app_id}"
            if app_name in DataBase.app_instances:
                print(app_name)
                instance = DataBase.app_instances[app_name]
                setattr(instance, 'is_active', True)
                try:
                    instance.auto_login(account_id, password)
                except:
                    zmqThread.sendMsg(f"failed@log_in#{app_id}")
            else:
                zmqThread.sendMsg(f"failed@log_in#{app_id}") # failed cases where the app to log in does not exist

        if "log_out#" in serverMessage:
            parts = serverMessage.split("#")
            app_id = parts[1]
            for name, instance in DataBase.app_instances.items():
                setattr(instance, 'is_active', False)
            app_name = f"app{app_id}"
            if app_name in DataBase.app_instances:
                instance = DataBase.app_instances[app_name]
                setattr(instance, 'is_active', True)
                try:
                    instance.out()
                    zmqThread.sendMsg(f"logged_out"+"#"+f"{app_id}") 
                except:
                    zmqThread.sendMsg(f"failed@log_out#{app_id}")
            else:
                zmqThread.sendMsg(f"failed@log_out#{app_id}") # failed cases where the app to log out does not exist

        if "close_app#" in serverMessage:
            parts = serverMessage.split("#")
            app_id = parts[1]
            for name, instance in dict(DataBase.app_instances).items():
                if name == f"app{app_id}":
                    try:
                        instance.close()
                        del DataBase.app_instances[name]
                        zmqThread.sendMsg(f"app_closed#{app_id}")
                    except:
                        zmqThread.sendMsg(f"failed@close_app#{app_id}") 
            if f"app{app_id}" not in DataBase.app_instances.items():
                zmqThread.sendMsg(f"failed@close_app#{app_id}") # failed cases when try to close an app that does not actually exist

        # both ATM and app
        if "transfer_money@" in serverMessage :
            parts = serverMessage.split("#")
            basic_info = parts[0]
            info_parts = basic_info.split("@")
            receiver_id = info_parts[1]
            amount = info_parts[2]
            if len(parts) == 1:  
                ATM_current_window.auto_transfer(receiver_id, amount)
                zmqThread.sendMsg("money_transfered@"+ str(amount))
            elif len(parts) > 1 :
                for name, instance in DataBase.app_instances.items():
                    setattr(instance, 'is_active', False)
                app_name = f"app{parts[1]}" 
                if app_name in DataBase.app_instances:
                    instance = DataBase.app_instances[app_name]
                    setattr(instance, 'is_active', True)
                    try:
                        instance.auto_transfer(receiver_id, amount)
                    except:
                        zmqThread.sendMsg(f"failed@transfer_money#{app_id}")
                else:
                    zmqThread.sendMsg(f"failed@transfer_money#{app_id}") # failed cases where the app to transfer does not exist

        if "change_password@" in serverMessage and "#" not in serverMessage:
            new_password = serverMessage.split("@")[1]
            try:
                ATM_current_window.auto_change_password(new_password,True) 
                zmqThread.sendMsg(f"password_changed") 
            except:
                zmqThread.sendMsg(f"failed@change_password")
        elif "change_password@" in serverMessage and "#" in serverMessage:
            parts = serverMessage.split("@")
            new_password = parts[1].split("#")[0]  
            additional_info = parts[1].split("#")[1]  
            app_name = f"app{additional_info}"  
            for name, instance in DataBase.app_instances.items():
                setattr(instance, 'is_active', False)
            if app_name in DataBase.app_instances:
                print(app_name)
                instance = DataBase.app_instances[app_name]
                setattr(instance, 'is_active', True)
                try:
                    instance.auto_change_password(new_password, True)
                except:
                    zmqThread.sendMsg(f"failed@change_password#{app_id}")
            else:
                zmqThread.sendMsg(f"failed@change_password#{app_id}") # failed cases where the app to change password does not exist

        if "query" in serverMessage:
            parts = serverMessage.split("#")
            if len(parts) == 1:  
                ATM_current_window.query()
            elif len(parts) > 1 :
                app_id = parts[1]
                for name, instance in DataBase.app_instances.items():
                    setattr(instance, 'is_active', False)
                app_name = f"app{app_id}"
                if app_name in DataBase.app_instances:
                    instance = DataBase.app_instances[app_name]
                    setattr(instance, 'is_active', True)
                    try:
                        instance.query()
                        zmqThread.sendMsg(f"query_showed#{app_id}")
                    except:
                        zmqThread.sendMsg(f"failed@query#{app_id}")
                else:
                    zmqThread.sendMsg(f"failed@query#{app_id}") # failed cases where the app to query does not exist

    init.timeStamp = timeStamp
    init.serverMessage = serverMessage
    init.messageUnprocessed = messageUnprocessed

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # DataBase.auto=0
    # from app import applog
    # app1 = applog(100,700)
    # app1.show()

    # app2 = applog(700,700)
    # app2.show()

    from ATM import ATMlog, ATM_current_window
    ATM = ATMlog(700, 100)
    ATM.show()

    timer = QTimer()
    timer.timeout.connect(check_messages)
    timer.start(100)  # Check every second (100 milliseconds)

    sys.exit(app.exec_())
   