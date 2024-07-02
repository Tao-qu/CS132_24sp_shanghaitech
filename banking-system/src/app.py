import DataBase
import init

from Auto import AutoCloseMessageBox
from Auto import AutoInputDialog
from Launch import current_datetime
from query import query

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import  QMessageBox,QInputDialog,QDialog
from PyQt5.QtCore import *

from ui_to_py.applog_UI import Ui_applog
from ui_to_py.appmain_UI import Ui_appmain

app_current_account=0
app_current_account_password=0
app_current_account_balance=0

zmqThread = init.zmqThread
timeStamp = init.timeStamp
serverMessage = init.serverMessage
messageUnprocessed = init.messageUnprocessed

class applog(QtWidgets.QMainWindow):
    def __init__(self, x, y, parent=None):
        super(applog, self).__init__(parent)

        global app_current_account
        global app_current_account_password
        global app_current_account_balance
        self.app_current_account=app_current_account
        self.app_current_account_password=app_current_account_password
        self.app_current_account_balance=app_current_account_balance

        #self.account=None
        self.x=x
        self.y=y
        self.move(x, y)
        self.ui = Ui_applog()
        self.ui.setupUi(self)
        self.ui.close.clicked.connect(self.close)
        self.ui.confirm.clicked.connect(self.confirm)
        self.ui.help.clicked.connect(self.help)
        self.show()

    def auto_login(self, account_id, password):
        self.ui.card_number.setText(account_id)  # 自动设置账号
        self.ui.card_password.setText(password)  # 自动设置密码
        QTimer.singleShot(1000, self.confirm)

    def help(self):
        QMessageBox.information(self, "view", "Banking system initial assumption\n\nAssume that there is 2 accounts in the initial database,  and the accounts id are 11111/22222, with 10000 Yuan deposit in it.😊\n\n( The password is 11111/22222 respectively.)")

    def confirm(self):
        global app_current_account
        global app_current_account_password
        global app_current_account_balance
        card_number=self.ui.card_number.text()
        card_password=self.ui.card_password.text()
        if card_number in DataBase.account_password:
            if DataBase.account_password[card_number] == card_password:    
                msg_box = AutoCloseMessageBox(self)
                msg_box.setText("绑定成功！")
                msg_box.exec_()
                # 关闭当前窗口，并打开主窗口
                if (DataBase.auto==0):
                    for i in range(len(DataBase.manual_instances)):
                        if DataBase.manual_instances[i].account==card_number:
                            DataBase.manual_instances[i].out()
                            #del DataBase.manual_instances[i]
                else:
                    for name, instance in DataBase.app_instances.items():
                        if(hasattr(instance,'account')):
                            if instance.account==card_number and (instance.is_active==False):
                                DataBase.app_instances[name].out()
                              #  zmqThread.sendMsg(f"logged_in@{card_number}#{name[3:]}") 
                self.account=card_number
                app_current_account=card_number
                app_current_account_password=DataBase.account_password[app_current_account]
                app_current_account_balance=DataBase.account_balance[app_current_account]
                self.deleteLater()
                self.cams = appmain(self.x,self.y)
                self.cams.show()
                if(DataBase.auto==0):
                    self.cams.account=card_number
                    DataBase.manual_instances.append(self.cams)
                else:
                    for name, instance in DataBase.app_instances.items():
                        if(hasattr(instance,'is_active')):
                            if instance.is_active:
                                DataBase.app_instances[name] = self.cams
                                setattr(self.cams, 'account', card_number)
                                zmqThread.sendMsg(f"logged_in@{card_number}#{name[3:]}")
            else:
                msg_box = AutoCloseMessageBox(self)
                msg_box.setText("绑定失败，银行卡密码错误！")
                msg_box.exec_()
                if (DataBase.auto==1):
                    for name, instance in DataBase.app_instances.items():
                        if instance.is_active:
                            zmqThread.sendMsg(f"failed@log_in#{name[3:]}")
        else:
            msg_box = AutoCloseMessageBox(self)
            msg_box.setText("绑定失败，未查询到该银行账户！")
            msg_box.exec_()
            if (DataBase.auto==1):
                for name, instance in DataBase.app_instances.items():
                    if instance.is_active:
                        zmqThread.sendMsg(f"failed@log_in#{name[3:]}")

    def close(self):
        self.deleteLater()

class appmain(QtWidgets.QMainWindow):
    def __init__(self, x, y, parent=None):
        super(appmain, self).__init__(parent)

        global app_current_account
        global app_current_account_password
        global app_current_account_balance
        self.app_current_account=app_current_account
        self.app_current_account_password=app_current_account_password
        self.app_current_account_balance=app_current_account_balance

        self.account=None
        self.x=x
        self.y=y
        self.move(x, y)   
        self.ui = Ui_appmain()
        self.ui.setupUi(self)
        self.show()
        self.ui.current_account.setText(str(self.app_current_account))
        # self.ui.balance.setText(str(DataBase.account_balance[self.app_current_account]))
        self.ui.balance.setText(f"{float(DataBase.account_balance[self.app_current_account]):.2f}")
        self.ui.view.clicked.connect(self.view)
        self.ui.change_password.clicked.connect(self.change_password)
        self.ui.transfer.clicked.connect(self.transfer)
        self.ui.out.clicked.connect(self.out)
        self.ui.query.clicked.connect(self.query)

        # 创建定时器
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.updateText)
        self.timer.start()

    def updateText(self):
        # self.ui.balance.setText(str(DataBase.account_balance[self.app_current_account]))
        try:
            self.ui.balance.setText(f"{float(DataBase.account_balance[self.app_current_account]):.2f}")
        except:
            self.out()

    def view(self):
        global app_current_account
        global app_current_account_password
        global app_current_account_balance
        password = DataBase.account_password[self.app_current_account]
        QMessageBox.information(self, "view",  f"您当前账户的密码为：{password}")

    def is_two_decimal(self, number_str):
        try:
            float_number = float(number_str)
        except ValueError:
            return False  
        integer_part, decimal_part = str(float_number).split('.')
        return len(decimal_part) <= 2

    def change_password(self):
        global app_current_account
        global app_current_account_password
        global app_current_account_balance
        input_dialog = AutoInputDialog(self)
        input_dialog.setWindowTitle('修改密码')
        input_dialog.setLabelText('请输入你要修改的密码:')
        input_dialog.show()  # 显示输入对话框以允许用户手动输入
        if input_dialog.exec_() == QDialog.Accepted:
            new_password = input_dialog.textValue()
            self.auto_change_password(new_password, automated_test=False)

    def auto_change_password(self, new_password, automated_test=False):
        if automated_test:
            # 在自动化测试中自动填充并接受密码
            input_dialog = AutoInputDialog(self)
            input_dialog.setWindowTitle('修改密码')
            input_dialog.setLabelText('请输入你要修改的密码:')
            input_dialog.set_auto_text(new_password, 500)  # 延迟0.5秒自动填充
            if input_dialog.exec_() == QDialog.Accepted:
                new_password = input_dialog.textValue()
            else:
                return  
        if new_password == self.app_current_account_password:
            msg_box = AutoCloseMessageBox(self)
            msg_box.setText('修改密码失败，新密码不能与原密码一致😔')
            msg_box.exec_()
            if automated_test:
                for name, instance in DataBase.app_instances.items():
                    print(name)
                    print(instance.is_active)
                    if instance.is_active:
                        zmqThread.sendMsg(f"failed@change_password#{name[3:]}")
            return
        if (new_password.isdigit()==False) or len(new_password)<5 or len(new_password) > 12:
            msg_box = AutoCloseMessageBox(self)
            msg_box.setText('密码格式不正确，必须为5到12位的数字！')
            msg_box.exec_()
            if automated_test:
                for name, instance in DataBase.app_instances.items():
                    if instance.is_active:
                        zmqThread.sendMsg(f"failed@change_password#{name[3:]}")
            return

        # 修改密码
        self.app_current_account_password = new_password  # 更新当前的账户密码
        DataBase.account_password[self.app_current_account] = new_password  # 更新数据库里的账户密码
        # 显示成功信息
        msg_box = AutoCloseMessageBox(self)
        msg_box.setText(f'修改密码成功，您的新密码为🙂: {new_password}')
        msg_box.exec_()

        if automated_test:
            for name, instance in DataBase.app_instances.items():
                if instance.is_active:
                    zmqThread.sendMsg(f"password_changed#{name[3:]}")
            

    def transfer(self):

        global app_current_account
        global app_current_account_password
        global app_current_account_balance

        dest_num, ok1 = QInputDialog.getText(self, '转账', '请输入你要转账的目标账户:')
        if ok1:
            if dest_num not in DataBase.account_balance or dest_num == self.app_current_account:
                QMessageBox.warning(self, '错误', '目标账户无效或不能转账给自己')
                return

            transfer_amount, ok2 = QInputDialog.getText(self, '转账', '请输入你要转账的金额:')
            if ok2:
                try:
                    transfer_amount = float(transfer_amount)
                    if float(transfer_amount) < 0.01 or not self.is_two_decimal(transfer_amount) or float(transfer_amount) > float(self.app_current_account):
                        msg_box = AutoCloseMessageBox(self)
                        msg_box.setText('错误: 交易金额无效或超出账户余额')
                        msg_box.exec_()
                        return

                    # Perform the transfer
                    self.app_current_account_balance=float(self.app_current_account_balance)-float(transfer_amount) # 更新当前余额
                    DataBase.account_balance[self.app_current_account] = float(DataBase.account_balance[self.app_current_account])-float(transfer_amount) # 更新当前余额
                    DataBase.account_balance[dest_num]=float(DataBase.account_balance[dest_num])+float(transfer_amount) # 更新总的余额
                    # 更新交易流水
                    if self.app_current_account not in DataBase.detail:
                        DataBase.detail[self.app_current_account] = []
                    DataBase.detail[self.app_current_account].append([DataBase.account_balance[self.app_current_account], f'向{dest_num}账户转出', transfer_amount, current_datetime])
                    if dest_num not in DataBase.detail:
                        DataBase.detail[dest_num] = []
                    DataBase.detail[dest_num].append([DataBase.account_balance[dest_num], f'由{self.app_current_account}账户转入', transfer_amount, current_datetime])
                    # Success message
                    msg_box = AutoCloseMessageBox(self)
                    msg_box.setText(f'转账成功，您当前的账户余额为: {float(DataBase.account_balance[self.app_current_account])}元')
                    msg_box.exec_()
                    #self.ui.balance.setText(str(DataBase.account_balance[self.app_current_account]))  # Update balance display
                    # self.ui.balance.setText("{:.2f}".format(DataBase.account_balance[self.app_current_account]))
                except ValueError:
                    msg_box = AutoCloseMessageBox(self)
                    msg_box.setText('错误: 请输入有效的交易金额')
                    msg_box.exec_()

    def auto_transfer(self, dest_num, amount):

        global app_current_account
        global app_current_account_password
        global app_current_account_balance

        # First, handle the destination number
        input_dialog = AutoInputDialog(self)
        input_dialog.setWindowTitle('转账')
        input_dialog.setLabelText('请输入你要转账的目标账户:')
        input_dialog.set_auto_text(dest_num, 1000)

        if input_dialog.exec_() == QDialog.Accepted:
            if dest_num not in DataBase.account_balance or dest_num == self.app_current_account:
                msg_box = AutoCloseMessageBox(self)
                msg_box.setText('错误: 目标账户无效或不能转账给自己')
                msg_box.exec_()
                for name, instance in DataBase.app_instances.items():
                    if instance.is_active:
                        zmqThread.sendMsg(f"failed@transfer_money#{name[3:]}")
                return

            # Second, handle the transfer amount
            input_dialog = AutoInputDialog(self)
            input_dialog.setWindowTitle('转账')
            input_dialog.setLabelText('请输入你要转账的金额:')
            input_dialog.set_auto_text(amount, 1000)

            if input_dialog.exec_() == QDialog.Accepted:
                try:
                    transfer_amount = float(amount)
                    if float(transfer_amount) < 0.01 or not self.is_two_decimal(transfer_amount) or float(transfer_amount) > float(self.app_current_account):
                        msg_box = AutoCloseMessageBox(self)
                        msg_box.setText('错误: 交易金额无效或超出账户余额')
                        msg_box.exec_()
                        for name, instance in DataBase.app_instances.items():
                            if instance.is_active:
                                zmqThread.sendMsg(f"failed@transfer_money#{name[3:]}")
                        return
                    # Perform the transfer
                    self.app_current_account_balance=float(self.app_current_account_balance)-float(transfer_amount) # 更新当前余额
                    DataBase.account_balance[self.app_current_account] = float(DataBase.account_balance[self.app_current_account])-float(transfer_amount) # 更新当前余额
                    DataBase.account_balance[dest_num]=float(DataBase.account_balance[dest_num])+float(transfer_amount) # 更新对方账户余额
                    # 更新交易流水
                    if self.app_current_account not in DataBase.detail:
                        DataBase.detail[self.app_current_account] = []
                    DataBase.detail[self.app_current_account].append([DataBase.account_balance[self.app_current_account], f'向{dest_num}账户转出', transfer_amount, current_datetime])
                    if dest_num not in DataBase.detail:
                        DataBase.detail[dest_num] = []
                    DataBase.detail[dest_num].append([DataBase.account_balance[dest_num], f'由{self.app_current_account}账户转入', transfer_amount, current_datetime])
                    # Success message
                    msg_box = AutoCloseMessageBox(self)
                    msg_box.setText(f'转账成功，您当前的账户余额为: {float(DataBase.account_balance[self.app_current_account])}元')
                    msg_box.exec_()
                    self.ui.balance.setText(str(DataBase.account_balance[self.app_current_account]))  # Update balance display
                    for name, instance in DataBase.app_instances.items():
                        if instance.is_active:
                            zmqThread.sendMsg(f"money_transfered@{amount}"+"#"+f"{name[3:]}")
                except ValueError:
                    msg_box = AutoCloseMessageBox(self)
                    msg_box.setText('错误: 请输入有效的交易金额')
                    msg_box.exec_()
                    for name, instance in DataBase.app_instances.items():
                        if instance.is_active:
                            zmqThread.sendMsg(f"failed@transfer_money#{name[3:]}")
                    return

    def query(self):
        global app_current_account
        global app_current_account_password
        global app_current_account_balance
        self.cam = query(self.x, self.y, self.app_current_account)
        self.cam.show() 

    def out(self):
        global app_current_account
        if (DataBase.auto==0):
            for i in range(len(DataBase.manual_instances)):
                try:
                    if DataBase.manual_instances[i].account==self.app_current_account:
                        del DataBase.manual_instances[i]
                except:
                    break
            self.deleteLater()
            self.cams = applog(self.x,self.y)
            self.cams.show()  
        else:
            for name, instance in DataBase.app_instances.items():
                if(hasattr(instance,'account')):
                    if instance.account==self.app_current_account and (instance.is_active==False):
                        instance.account=0
                        self.deleteLater()
                        self.cams = applog(self.x,self.y)
                        self.cams.show()  
                        DataBase.app_instances[name]=self.cams
                        return
                    
            for name, instance in DataBase.app_instances.items():
                if instance.is_active==True:
                    self.deleteLater()
                    self.cams = applog(self.x,self.y)
                    self.cams.show()  
                    DataBase.app_instances[name]=self.cams