import DataBase
import init

from Auto import AutoCloseMessageBox
from Auto import AutoInputDialog
from Launch import current_datetime
from query import query

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox,QInputDialog,QDialog
from PyQt5.QtCore import *

from ui_to_py.ATMlog_UI import Ui_ATMlog
from ui_to_py.ATMmain_UI import Ui_ATMmain

zmqThread = init.zmqThread
timeStamp = init.timeStamp
serverMessage = init.serverMessage
messageUnprocessed = init.messageUnprocessed

ATM_current_window = None 

class ATMlog(QtWidgets.QMainWindow):
    def __init__(self, x, y, parent=None):
        super(ATMlog, self).__init__(parent)

        global ATM_current_window
        ATM_current_window=self

        self.x=x
        self.y=y
        self.move(x, y)  
        self.ui = Ui_ATMlog()
        self.ui.setupUi(self)
        self.ui.confirm.clicked.connect(self.confirm)
        self.ui.help.clicked.connect(self.help)
        self.show()

    def help(self, auto_password=None):
        if auto_password:
            # Automatic mode
            input_dialog = AutoInputDialog(self)
            input_dialog.setWindowTitle('创建账户')
            input_dialog.setLabelText('请输入你要创建的账户密码')
            input_dialog.set_auto_text(auto_password)  # Set the auto password and confirm
        else:
            # Manual mode
            input_dialog = QInputDialog(self)
            input_dialog.setWindowTitle('创建账户')
            input_dialog.setLabelText('请输入你要创建的账户密码')
        
        if input_dialog.exec_() == QDialog.Accepted:
            password = input_dialog.textValue()
            if (password.isdigit()==False) or len(password)<5 or len(password) > 12:
                msg_box = AutoCloseMessageBox(self)
                msg_box.setText('密码格式不正确，必须为5到12位的数字！')
                msg_box.exec_()
                return
            new_account = DataBase.generate_random_number()
            DataBase.account_balance[new_account] = 0
            DataBase.account_password[new_account] = password
            # Use auto-closing message box
            msg_box = AutoCloseMessageBox(self)
            msg_box.setText(f'创建账户成功！\n您的账户为{new_account}\n密码为: {password}')
            msg_box.exec_()
            DataBase.ATM_current_account=new_account
            self.deleteLater()
            self.cams = ATMmain(self.x,self.y)
            self.cams.show()

            global ATM_current_window
            ATM_current_window=self.cams

            zmqThread.sendMsg("account_created@"+ str(new_account))            

    def auto_login(self, account_id, password):
        self.ui.card_number.setText(account_id)  # 自动设置账号
        self.ui.card_password.setText(password)  # 自动设置密码
        QTimer.singleShot(1000, self.confirm)

    def confirm(self):
        card_number=self.ui.card_number.text()
        card_password=self.ui.card_password.text()
        if card_number in DataBase.account_password:
            if DataBase.account_password[card_number] == card_password:    
                msg_box = AutoCloseMessageBox(self)
                msg_box.setText("绑定成功！")
                msg_box.exec_()
                DataBase.ATM_current_account=card_number
                self.deleteLater()
                self.cams = ATMmain(self.x,self.y)
                self.cams.show()

                global ATM_current_window
                ATM_current_window=self.cams

                zmqThread.sendMsg("card_inserted@"+ str(card_number))

            else:
                msg_box = AutoCloseMessageBox(self)
                msg_box.setText("绑定失败，银行卡密码错误！")
                msg_box.exec_()
                zmqThread.sendMsg(f"failed@insert_card")
        else:
            msg_box = AutoCloseMessageBox(self)
            msg_box.setText("绑定失败，未查询到该银行账户！")
            msg_box.exec_()
            zmqThread.sendMsg(f"failed@insert_card")



class ATMmain(QtWidgets.QMainWindow):
    def __init__(self, x, y, parent=None):
        super(ATMmain, self).__init__(parent)

        global ATM_current_window
        ATM_current_window=self

        self.x=x
        self.y=y
        self.move(x, y)     # 设置窗口位置

        self.ui = Ui_ATMmain()
        self.ui.setupUi(self)
        self.show()

        self.ui.current_account.setText(DataBase.ATM_current_account)
        # self.ui.balance.setText(str(DataBase.account_balance[DataBase.ATM_current_account]))
        self.ui.balance.setText(f"{float(DataBase.account_balance[DataBase.ATM_current_account]):.2f}")
        self.ui.view.clicked.connect(self.view)
        self.ui.change_password.clicked.connect(self.change_password)
        self.ui.transfer.clicked.connect(self.transfer)
        self.ui.recharge.clicked.connect(self.recharge)
        self.ui.withdraw.clicked.connect(self.withdraw)
        self.ui.flow.clicked.connect(self.query)
        self.ui.out.clicked.connect(self.out)
        self.ui.close.clicked.connect(self.close)

        # 创建定时器
        self.timer = QTimer()
        # 每隔0.1秒触发一次timeout信号
        self.timer.setInterval(100)
        # 连接timeout信号到updateText方法
        self.timer.timeout.connect(self.updateText)
        # 启动定时器
        self.timer.start()

    def updateText(self):
        current_account = DataBase.ATM_current_account
        if current_account in DataBase.account_balance:
            # self.ui.balance.setText(str(DataBase.account_balance[current_account]))
            self.ui.balance.setText(f"{float(DataBase.account_balance[DataBase.ATM_current_account]):.2f}")
        else:
            self.ui.balance.setText("账户不存在")

    def is_two_decimal(self, number_str):
        # 先尝试将字符串转换为浮点数
        try:
            float_number = float(number_str)
        except ValueError:
            return False  # 如果无法将字符串转换为浮点数，返回 False
        # 分割整数部分和小数部分
        integer_part, decimal_part = str(float_number).split('.')
        # 检查小数部分的长度是否为两位
        return len(decimal_part) <= 2

    def view(self):
        password =DataBase.account_password[DataBase.ATM_current_account]
        QMessageBox.information(self, "view",  f"您当前账户的密码为：{password}")

    def change_password(self):
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
                return  # 如果对话框没有被接受，直接返回
        # 验证新密码是否与原密码一致
        if new_password == DataBase.account_password[DataBase.ATM_current_account]:
            msg_box = AutoCloseMessageBox(self)
            msg_box.setText('修改密码失败，新密码不能与原密码一致😔')
            msg_box.exec_()
            if automated_test:
                zmqThread.sendMsg("failed@change_password")
            return
        
        if (new_password.isdigit()==False) or len(new_password)<5 or len(new_password) > 12:
            msg_box = AutoCloseMessageBox(self)
            msg_box.setText('密码格式不正确，必须为5到12位的数字！')
            msg_box.exec_()
            if automated_test:
                zmqThread.sendMsg(f"failed@change_password")
            return

        # 修改密码
        DataBase.account_password[DataBase.ATM_current_account] = new_password  # 更新当前的账户密码
        DataBase.account_password[DataBase.ATM_current_account] = new_password  # 更新数据库里的账户密码
        # 显示成功信息
        msg_box = AutoCloseMessageBox(self)
        msg_box.setText(f'修改密码成功，您的新密码为🙂: {new_password}')
        msg_box.exec_()

    def transfer(self):
        dest_num, ok1 = QInputDialog.getText(self, '转账', '请输入你要转账的目标账户:')
        if ok1:
            if dest_num not in DataBase.account_balance or dest_num == DataBase.ATM_current_account:
                QMessageBox.warning(self, '错误', '目标账户无效或不能转账给自己')
                return

            transfer_amount, ok2 = QInputDialog.getText(self, '转账', '请输入你要转账的金额:')
            if ok2:
                try:
                    transfer_amount = float(transfer_amount)
                    if float(transfer_amount) < 0.01 or not self.is_two_decimal(transfer_amount) or float(transfer_amount) > float(DataBase.account_balance[DataBase.ATM_current_account]):
                        msg_box = AutoCloseMessageBox(self)
                        msg_box.setText('错误: 交易金额无效或超出账户余额')
                        msg_box.exec_()
                        return
                    
                    password, ok3 = QInputDialog.getText(self, '转账', '请输入你当前的账户密码:')
                    if ok3:
                        if str(password)!=str(DataBase.account_password[DataBase.ATM_current_account]):
                            msg_box = AutoCloseMessageBox(self)
                            msg_box.setText('错误: 你当前的账户密码错误')
                            msg_box.exec_()
                            return                            
                        # Perform the transfer
                        DataBase.account_balance[DataBase.ATM_current_account] = float(DataBase.account_balance[DataBase.ATM_current_account])-float(transfer_amount)
                        DataBase.account_balance[dest_num] = float(DataBase.account_balance[dest_num])+float(transfer_amount)

                        # Update transaction history
                        if DataBase.ATM_current_account not in DataBase.detail:
                            DataBase.detail[DataBase.ATM_current_account] = []
                        DataBase.detail[DataBase.ATM_current_account].append([DataBase.account_balance[DataBase.ATM_current_account], f'向{dest_num}账户转出', transfer_amount, current_datetime])

                        if dest_num not in DataBase.detail:
                            DataBase.detail[dest_num] = []
                        DataBase.detail[dest_num].append([DataBase.account_balance[dest_num], f'由{DataBase.ATM_current_account}账户转入', transfer_amount, current_datetime])

                        # Success message
                        msg_box = AutoCloseMessageBox(self)
                        msg_box.setText(f'转账成功，您当前的账户余额为: {DataBase.account_balance[DataBase.ATM_current_account]}元')
                        msg_box.exec_()

                        self.ui.balance.setText(str(DataBase.account_balance[DataBase.ATM_current_account]))  # Update balance display
                except ValueError:
                    msg_box = AutoCloseMessageBox(self)
                    msg_box.setText('错误: 请输入有效的交易金额')
                    msg_box.exec_()
                    return

    def auto_transfer(self, dest_num, amount):
        # First, handle the destination number
        input_dialog = AutoInputDialog(self)
        input_dialog.setWindowTitle('转账')
        input_dialog.setLabelText('请输入你要转账的目标账户:')
        input_dialog.set_auto_text(dest_num, 1000)

        if input_dialog.exec_() == QDialog.Accepted:
            if dest_num not in DataBase.account_balance or dest_num == DataBase.ATM_current_account:
                msg_box = AutoCloseMessageBox(self)
                msg_box.setText('错误: 目标账户无效或不能转账给自己')
                msg_box.exec_()
                zmqThread.sendMsg("failed@transfer_money")
                return

            # Second, handle the transfer amount
            input_dialog = AutoInputDialog(self)
            input_dialog.setWindowTitle('转账')
            input_dialog.setLabelText('请输入你要转账的金额:')
            input_dialog.set_auto_text(amount, 1000)

            if input_dialog.exec_() == QDialog.Accepted:
                transfer_amount = float(amount)
                try:
                    transfer_amount = float(transfer_amount)
                    if float(transfer_amount) < 0.01 or not self.is_two_decimal(transfer_amount) or float(transfer_amount) > float(DataBase.account_balance[DataBase.ATM_current_account]):
                        msg_box = AutoCloseMessageBox(self)
                        msg_box.setText('错误: 交易金额无效或超出账户余额')
                        msg_box.exec_()
                        zmqThread.sendMsg("failed@transfer_money")
                        return

                    # Perform the transfer
                    DataBase.account_balance[DataBase.ATM_current_account] = float(DataBase.account_balance[DataBase.ATM_current_account])-float(transfer_amount)
                    DataBase.account_balance[dest_num] = float(DataBase.account_balance[dest_num])+float(transfer_amount)

                    # Update transaction history
                    if DataBase.ATM_current_account not in DataBase.detail:
                        DataBase.detail[DataBase.ATM_current_account] = []
                    DataBase.detail[DataBase.ATM_current_account].append([DataBase.account_balance[DataBase.ATM_current_account], f'向{dest_num}账户转出', transfer_amount, current_datetime])

                    if dest_num not in DataBase.detail:
                        DataBase.detail[dest_num] = []
                    DataBase.detail[dest_num].append([DataBase.account_balance[dest_num], f'由{DataBase.ATM_current_account}账户转入', transfer_amount, current_datetime])

                    # Success message
                    msg_box = AutoCloseMessageBox(self)
                    msg_box.setText(f'转账成功，您当前的账户余额为: {DataBase.account_balance[DataBase.ATM_current_account]}元')
                    msg_box.exec_()

                    self.ui.balance.setText(str(DataBase.account_balance[DataBase.ATM_current_account]))
                except ValueError:
                    msg_box = AutoCloseMessageBox(self)
                    msg_box.setText('错误: 请输入有效的交易金额')
                    msg_box.exec_()
                    zmqThread.sendMsg(f"failed@transfer_money")
                    return


    def recharge(self):
        def is_two_decimal(number):
            return round(number, 2) == number 
        recharge_amount, ok = QInputDialog.getText(self, '充值', '请输入你要充值的金额:')
        if ok:
            try:
                # 检查输入是否为纯数字
                recharge_amount = float(recharge_amount)
            except ValueError:
                QMessageBox.warning(self, '错误', '请输入有效的数字金额')
                return
            # 检查充值金额是否小于0.01￥
            if recharge_amount < 0.01:
                QMessageBox.warning(self, '错误', '充值金额必须大于等于0.01￥')
                return
            # 检查充值金额是否合理
            if not is_two_decimal(recharge_amount):
                QMessageBox.warning(self, '错误', '充值金额必须为0.01￥的整数倍')
                return
            if (float(recharge_amount))%100!=0:
                QMessageBox.warning(self, '错误', '充值金额必须为100￥的整数倍')
                return
            # 更新账户余额

            password, ok3 = QInputDialog.getText(self, '充值', '请输入你当前的账户密码:')
            if ok3:
                if str(password)!=str(DataBase.account_password[DataBase.ATM_current_account]):
                    msg_box = AutoCloseMessageBox(self)
                    msg_box.setText('错误: 你当前的账户密码错误')
                    msg_box.exec_()
                    return      

                DataBase.account_balance[DataBase.ATM_current_account] = float(DataBase.account_balance[DataBase.ATM_current_account])+float(recharge_amount)
                DataBase.account_balance[DataBase.ATM_current_account] = DataBase.account_balance[DataBase.ATM_current_account]
                # 更新交易流水
                if DataBase.ATM_current_account not in DataBase.detail:
                    DataBase.detail[DataBase.ATM_current_account] = []
                DataBase.detail[DataBase.ATM_current_account].append([DataBase.account_balance[DataBase.ATM_current_account], '充值', recharge_amount, current_datetime])
        self.ui.balance.setText(str(DataBase.account_balance[DataBase.ATM_current_account]))

    def auto_recharge(self, amount):
        # 使用 AutoInputDialog 进行自动输入和确认
        input_dialog = AutoInputDialog(self)
        input_dialog.setWindowTitle('充值')
        input_dialog.setLabelText('请输入你要充值的金额:')
        input_dialog.set_auto_text(amount, 2000)  # 设置自动填写的金额和延迟
        if input_dialog.exec_() == QDialog.Accepted:
            recharge_amount = float(input_dialog.textValue())  # 获取输入的金额
            # 检查充值金额是否小于0.01元
            if recharge_amount < 0.01:
                msg_box = AutoCloseMessageBox(self)
                msg_box.setText('充值金额必须大于等于0.01元')
                msg_box.exec_()
                zmqThread.sendMsg("failed@deposit_cash")
                return
            # 检查充值金额是否为两位小数
            if not self.is_two_decimal(recharge_amount):
                msg_box = AutoCloseMessageBox(self)
                msg_box.setText('充值金额必须为0.01元的整数倍')
                msg_box.exec_()
                zmqThread.sendMsg("failed@deposit_cash")
                return
            if (float(recharge_amount))%100!=0:
                msg_box = AutoCloseMessageBox(self)
                msg_box.setText('充值金额必须为100元的整数倍')
                msg_box.exec_()
                zmqThread.sendMsg("failed@deposit_cash")
                return
            # 更新账户余额
            DataBase.account_balance[DataBase.ATM_current_account] = float(DataBase.account_balance[DataBase.ATM_current_account])+float(recharge_amount)
            DataBase.account_balance[DataBase.ATM_current_account] = DataBase.account_balance[DataBase.ATM_current_account]
            # 更新交易流水
            if DataBase.ATM_current_account not in DataBase.detail:
                DataBase.detail[DataBase.ATM_current_account] = []
            DataBase.detail[DataBase.ATM_current_account].append([DataBase.account_balance[DataBase.ATM_current_account], '充值', recharge_amount, current_datetime])
            # 显示充值成功信息
            msg_box = AutoCloseMessageBox(self)
            msg_box.setText(f'充值成功，您当前的账户余额为: {DataBase.account_balance[DataBase.ATM_current_account]}元')
            msg_box.exec_()
            # 更新界面显示的余额
            self.ui.balance.setText(str(DataBase.account_balance[DataBase.ATM_current_account]))
            zmqThread.sendMsg("cash_deposited@"+ str(input_dialog.textValue()))

    def withdraw(self):
        def is_two_decimal(number):
            return round(number, 2) == number 
        withdraw_amount, ok = QInputDialog.getText(self, '提现', '请输入你要提现的金额:')
        if ok:
            try:
                # 检查输入是否为纯数字
                withdraw_amount = float(withdraw_amount)
            except ValueError:
                QMessageBox.warning(self, '错误', '请输入有效的数字金额')
                return
            # 检查充值金额是否小于0.01￥
            if withdraw_amount < 0.01:
                QMessageBox.warning(self, '错误', '取款金额必须大于等于0.01￥')
                return
            # 检查充值金额是否合理
            if not is_two_decimal(withdraw_amount):
                QMessageBox.warning(self, '错误', '取款金额必须为0.01￥的整数倍')
                return
            # 检查提现金额是否小于等于当前余额
            if float(withdraw_amount) > float(DataBase.account_balance[DataBase.ATM_current_account]):
                QMessageBox.warning(self, '错误', '取款金额不能大于当前账户余额')
                return

            password, ok3 = QInputDialog.getText(self, '取款', '请输入你当前的账户密码:')
            if ok3:
                if str(password)!=str(DataBase.account_password[DataBase.ATM_current_account]):
                    msg_box = AutoCloseMessageBox(self)
                    msg_box.setText('错误: 你当前的账户密码错误')
                    msg_box.exec_()
                    return                      
                # 更新账户余额
                DataBase.account_balance[DataBase.ATM_current_account] = float(DataBase.account_balance[DataBase.ATM_current_account])-float(withdraw_amount)
                DataBase.account_balance[DataBase.ATM_current_account] = DataBase.account_balance[DataBase.ATM_current_account]

                # 更新交易流水
                if DataBase.ATM_current_account not in DataBase.detail:
                    DataBase.detail[DataBase.ATM_current_account] = []
                DataBase.detail[DataBase.ATM_current_account].append([DataBase.account_balance[DataBase.ATM_current_account], '取款', withdraw_amount, current_datetime])

                # 显示取款成功信息
                msg_box = AutoCloseMessageBox(self)
                msg_box.setText(f'取款成功，您当前的账户余额为: {DataBase.account_balance[DataBase.ATM_current_account]}元')
                msg_box.exec_()
                self.ui.balance.setText(str(DataBase.account_balance[DataBase.ATM_current_account]))  # 更新界面显示的余额


    def auto_withdraw(self, amount, password):
        # 验证密码（假设密码验证是必要的）
        if password != DataBase.account_password[DataBase.ATM_current_account]:  # 假设这里已经有了正确的密码验证逻辑
            msg_box = AutoCloseMessageBox(self)
            msg_box.setText('密码错误')
            msg_box.exec_()
            zmqThread.sendMsg("failed@withdraw_cash")
            return

        # 输入金额
        input_dialog = AutoInputDialog(self)
        input_dialog.setWindowTitle('提现')
        input_dialog.setLabelText('请输入你要提现的金额:')
        input_dialog.set_auto_text(amount, 1000)  # 设置自动填写的金额和延迟

        if input_dialog.exec_() == QDialog.Accepted:
            withdraw_amount = float(input_dialog.textValue())  # 获取输入的金额

            # 执行金额检查和余额更新
            if withdraw_amount < 0.01 or not self.is_two_decimal(withdraw_amount) or withdraw_amount > DataBase.account_balance[DataBase.ATM_current_account]:
                msg_box = AutoCloseMessageBox(self)
                msg_box.setText('取款失败，金额无效或超出账户余额')
                msg_box.exec_()
                zmqThread.sendMsg("failed@withdraw_cash")
                return
            DataBase.account_balance[DataBase.ATM_current_account] = float(DataBase.account_balance[DataBase.ATM_current_account])-float(withdraw_amount)
            # 更新交易流水
            if DataBase.ATM_current_account not in DataBase.detail:
                DataBase.detail[DataBase.ATM_current_account] = []
            DataBase.detail[DataBase.ATM_current_account].append([DataBase.account_balance[DataBase.ATM_current_account], '取款', withdraw_amount, current_datetime])
            # 显示取款成功信息
            msg_box = AutoCloseMessageBox(self)
            msg_box.setText(f'取款成功，您当前的账户余额为: {DataBase.account_balance[DataBase.ATM_current_account]}元')
            msg_box.exec_()
            self.ui.balance.setText(str(DataBase.account_balance[DataBase.ATM_current_account]))  # 更新界面显示的余额
            zmqThread.sendMsg("cash_withdrawn@"+ str(input_dialog.textValue()))

    def query(self):
        # self.deleteLater()
        self.cams = query(self.x, self.y, DataBase.ATM_current_account)
        self.cams.show() 
        zmqThread.sendMsg("query_showed")
        # global ATM_current_window
        # ATM_current_window=self.cams

    def out(self):
        self.deleteLater()
        self.cams = ATMlog(self.x,self.y)
        self.cams.show()  
        global ATM_current_window
        ATM_current_window=self.cams
        zmqThread.sendMsg("card_returned@"+ str(DataBase.ATM_current_account))

    def close(self):
        # if self.isVisible():  # 检查窗口是否可见，从而判断其是否有效
            if float(DataBase.account_balance[DataBase.ATM_current_account]) > 0:
                msg_box = AutoCloseMessageBox(self)
                msg_box.setText(f'注销账户时应确保账户余额清零！\n您当前的账户余额为{DataBase.account_balance[DataBase.ATM_current_account]}￥')
                msg_box.exec_()
                zmqThread.sendMsg("failed@close_acount")
            else:
                if DataBase.ATM_current_account in DataBase.account_balance:
                    del DataBase.account_balance[DataBase.ATM_current_account]
                if DataBase.ATM_current_account in DataBase.account_password:
                    del DataBase.account_password[DataBase.ATM_current_account]

                msg_box = AutoCloseMessageBox(self)
                msg_box.setText(f'账户 {DataBase.ATM_current_account} 已成功删除🙂')
                msg_box.show()
                msg_box.exec_()
                self.deleteLater()
                self.cams = ATMlog(self.x,self.y)
                global ATM_current_window
                ATM_current_window=self.cams
                zmqThread.sendMsg("account_closed@"+ str(DataBase.ATM_current_account))