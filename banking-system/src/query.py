import DataBase

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import *

from ui_to_py.query_UI import Ui_query

class query(QtWidgets.QMainWindow):
    def __init__(self, x, y, account, parent=None):
        super(query, self).__init__(parent)
        self.account = account

        self.x = x
        self.y = y
        self.move(x, y)
        self.ui = Ui_query()
        self.ui.setupUi(self)
        self.ui.return_to_main.clicked.connect(self.RETURN)
        self.show()

        # 设置定时器更新账户信息和详情
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_info)
        self.update_timer.start(100)  # 设置定时器每100毫秒（0.1秒）触发一次

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.RETURN)
        self.timer.start(5000)

    def update_info(self):
        # 更新账户信息显示
        self.ui.current_account.setText(str(self.account))
        # 更新交易详情
        self.print_detail()

    def RETURN(self):
        self.update_timer.stop()  # 停止更新定时器
        self.timer.stop()  # 停止自动返回定时器
        self.deleteLater()

    def print_detail(self):
    # 先清空现有的表格内容
        self.ui.tableWidget.setRowCount(0)
        # 获取当前账户的所有交易详情
        current_account_details = DataBase.detail.get(self.account, [])
        # 打印当前账户的详情，检查是否为预期的列表结构
        # print("当前账户详情：", DataBase.detail.get(self.account, []))
        # 检查每条记录是否长度足够
        for record in DataBase.detail.get(self.account, []):
            if not isinstance(record, list) or len(record) < 4:
                print("记录不符合预期：", record)
        # 确保每个记录都是列表并且长度至少为4
        valid_details = [detail for detail in current_account_details if isinstance(detail, list) and len(detail) >= 4]
        # 按交易时间对详情进行排序
        sorted_details = sorted(valid_details, key=lambda x: x[3])
        # 遍历每一条交易记录
        for detail in sorted_details:
            # if detail[0] in DataBase.added_account.keys():
            row_position = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_position)
            # 遍历每一个交易详情的字段，并添加到表格中
            for column, item in enumerate(detail):
                table_item = QTableWidgetItem(str(item))
                table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)  # 设置为不可编辑
                self.ui.tableWidget.setItem(row_position, column, table_item)
        # 在所有数据填充完毕后，调整每列的宽度以适应内容
        self.ui.tableWidget.resizeColumnsToContents()

