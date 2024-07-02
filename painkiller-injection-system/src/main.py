import sys
import database

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import *

from ui_painkiller import Ui_Dialog
from ui_painkiller_patient import Ui_Dialog_Patient

from PyQt5.QtWidgets import QApplication, QDialog

import time


class MainDialog(QDialog):
    def __init__(self):
        super(MainDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_connections()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update)
        self.timer.start()
        self.ui.progress_1h.setValue(0)
        self.ui.progress_24h.setValue(0)
        database.bolus_amount = 0.2
        database.baseline_amount = 0.01
        database.baseline_timeline_list = []
        database.bolus_timeline_list = []
        database.cur_time = 0
        database.time_speed = 0
        self.ui.timeadjustdial.setValue(0)
        self.changeTimeSpeed(0)

        # database.injection_enable = 1

        database.initial_time = 0

        database.switch_on = 0

        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QPushButton {
                font-family: Cambria;
                background-color: #0078d7;
                border: none;
                color: white;
                text-align: center;
                text-decoration: none;
                font-size: 14px;
                border-radius: 12px;
            }
            QPushButton:checked {
                background-color: #0053a0;
            }
        """)

    def update(self):
        if database.time_speed != 0:
            database.current_time += 60/150

        if database.switch_on == 1:
            self.ui.horizontalSlider.setEnabled(False)
        else:
            self.ui.horizontalSlider.setEnabled(True)

        len_baseline = len(database.baseline_timeline_list)
        if len_baseline == 0 and database.switch_on == 0:
            database.baseline_timeline_list.append([database.current_time, 0])
            self.ui.baselinelabel.setText("Baseline: off")
        elif len_baseline == 0 and database.switch_on == 1:
            database.baseline_timeline_list.append(
                [database.current_time, database.baseline_amount])
            self.ui.baselinelabel.setText("Baseline: on")
        elif database.switch_on == 0:
            if database.baseline_timeline_list[-1][1] > 0.0000001:
                database.baseline_timeline_list.append(
                    [database.current_time, 0])
            self.ui.baselinelabel.setText("Baseline: off")
        else:
            if (database.calculate_1_h(database.baseline_timeline_list, database.bolus_timeline_list, database.current_time)+database.baseline_amount*(database.time_speed/2.5)/1000 <= 1 and database.calculate_24_h(database.baseline_timeline_list, database.bolus_timeline_list, database.current_time)+database.baseline_amount*(database.time_speed/2.5)/1000 <= 3):
                if database.baseline_timeline_list[-1][1] != database.baseline_amount:
                    database.baseline_timeline_list.append(
                        [database.current_time, database.baseline_amount])
                self.ui.baselinelabel.setText("Baseline: on")
            else:
                if database.baseline_timeline_list[-1][1] > 0.0000001:
                    database.baseline_timeline_list.append(
                        [database.current_time, 0])
                self.ui.baselinelabel.setText("Baseline: off")

        self.ui.lcdNumber.display(
            (database.current_time-database.initial_time)*150//(3600*24))
        self.ui.lcdNumber_2.display(
            ((database.current_time-database.initial_time)*150 % (3600*24))//3600)
        self.ui.lcdNumber_3.display(
            ((database.current_time-database.initial_time)*150 % 3600)//60)
        ex_time = database.current_time-24*24*3

        i = 0
        if (len(database.baseline_timeline_list) >= 3):
            while i < len(database.baseline_timeline_list)-1:
                if (database.baseline_timeline_list[i+1][0] < ex_time):
                    database.baseline_timeline_list.pop(0)
                else:
                    i += 1
                if (len(database.baseline_timeline_list) <= 3):
                    break

        i = 0
        if (len(database.baseline_timeline_list) >= 3):
            while i < len(database.baseline_timeline_list):
                if (database.baseline_timeline_list[i][0] < ex_time):
                    database.baseline_timeline_list.pop(0)
                else:
                    i += 1
                if (len(database.baseline_timeline_list) <= 3):
                    break

        # if (database.calculate_1_h(database.baseline_timeline_list, database.bolus_timeline_list, database.current_time) >= 1 or database.calculate_24_h(database.baseline_timeline_list, database.bolus_timeline_list, database.current_time) >= 3):
        #    # database.injection_enable = 0
        #    database.baseline_timeline_list.append([database.current_time, 0])

        self.ui.progress_24h.setValue(int(min(database.calculate_24_h(
            database.baseline_timeline_list, database.bolus_timeline_list, database.current_time)*100/3, 100)))
        self.ui.progress_1h.setValue(int(min(database.calculate_1_h
                                         (database.baseline_timeline_list, database.bolus_timeline_list, database.current_time)*100, 100)//1))
        # print(database.injection_enable)

    def setup_connections(self):
        # self.ui.SetBolusButton.clicked.connect(self.set_bolus)
        # self.ui.CancelBolusButtom.clicked.connect(self.cancel_bolus)
        # self.ui.SetBaselineBottom.clicked.connect(self.set_baseline)
        # self.ui.CancelBaselineBottom.clicked.connect(self.cancel_baseline)
        # self.ui.InjectionButtom.clicked.connect(self.inject_bolus)
        self.ui.StartBaselineBottom.clicked.connect(self.start_baseline)
        # self.ui.EndBaselineBottom.clicked.connect(self.end_baseline)
        self.ui.RstButton.clicked.connect(self.reset_everything)
        self.ui.horizontalSlider_2.valueChanged.connect(self.changeBolus)
        self.ui.horizontalSlider.valueChanged.connect(self.changeBaseline)
        self.ui.timeadjustdial.valueChanged.connect(self.changeTimeSpeed)

    def changeBolus(self, value):
        database.bolus_amount = value/1000
        self.ui.label_12.setText("Current Bolus: "+str(value/1000))

    def changeBaseline(self, value):
        database.baseline_amount = value/1000
        self.ui.label_11.setText("Current Bolus: "+str(value/1000))

    def changeTimeSpeed(self, value):
        time_speed_ = value/2
        database.time_speed = time_speed_
        if database.time_speed == 0:
            self.timer.setInterval(1000)
        else:
            self.timer.setInterval(int(1000/database.time_speed))
        self.ui.timeadjustlabel.setText(
            "Current time speed: "+str(time_speed_)+"min/s.")

    # def set_bolus(self):
    #    database.bolus_amount = float(self.ui.BolusEdit.text())
    #    self.ui.BolusEdit.clear()

    # def cancel_bolus(self):
    #    self.ui.BolusEdit.clear()

    # def set_baseline(self):
    #    database.baseline_amount = float(self.ui.BaselineEdit.text())
    #    self.ui.BaselineEdit.clear()

    # def cancel_baseline(self):
    #    self.ui.BaselineEdit.clear()

    # def inject_bolus(self):
    #    if (database.injection_enable):
    #        database.bolus_timeline_list.append(
    #            [time.time(), database.bolus_amount])

    def start_baseline(self):
        # if (database.injection_enable == 1 and database.calculate_1_h(database.baseline_timeline_list, database.bolus_timeline_list)+database.baseline_amount/1000 <= 1 and database.calculate_24_h(database.baseline_timeline_list, database.bolus_timeline_list)+database.baseline_amount/1000 <= 3):
        #    database.baseline_timeline_list.append(
        #        [time.time(), database.baseline_amount])
        database.switch_on = 1-database.switch_on

        if database.switch_on == 1:
            self.ui.switchlabel.setText("The switch is on.")
        else:
            self.ui.switchlabel.setText("The switch is off.")
        if database.switch_on == 0:
            self.ui.baselinelabel.setText("Baseline: off")

    # def end_baseline(self):
    #    database.baseline_timeline_list.append([time.time(), 0])

    def reset_everything(self):
        # database.bolus_amount = 0.2
        # database.baseline_amount = 0.01
        database.baseline_timeline_list = []
        database.bolus_timeline_list = []

        # database.injection_enable = 1

        database.switch_on = 0
        self.ui.switchlabel.setText("The switch is off.")


class PatientDialog(QDialog):
    def __init__(self):
        super(PatientDialog, self).__init__()
        self.ui = Ui_Dialog_Patient()
        self.ui.setupUi(self)
        self.setup_connections_patient()

        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QPushButton {
                font-family: Cambria;
                background-color: #0078d7;
                border: none;
                color: white;
                text-align: center;
                text-decoration: none;
                font-size: 14px;
                border-radius: 12px;
            }
            QPushButton:checked {
                background-color: #0053a0;
            }
        """)

    def setup_connections_patient(self):
        self.ui.InjectionButtom_2.clicked.connect(self.inject_bolus)

    def inject_bolus(self):
        if (database.calculate_1_h(database.baseline_timeline_list, database.bolus_timeline_list, database.current_time)+database.bolus_amount <= 1 and database.calculate_24_h(database.baseline_timeline_list, database.bolus_timeline_list, database.current_time)+database.bolus_amount <= 3):
            database.bolus_timeline_list.append(
                [database.current_time, database.bolus_amount])
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Successful Bolus Injection!")
            msg.setInformativeText(
                "The injected amount is "+str(database.bolus_amount)+".")
            msg.setWindowTitle("Success")
            msg.setStandardButtons(QMessageBox.Ok)
            # palette = msg.palette()
            # palette.setColor(QPalette.Base, QColor("#ffffff"))
            # msg.setPalette(palette)
            msg.setStyleSheet("""
            QMessageBox {
                background-color: #2d2d2d;
                color: #ffffff;
                font: Cambria 14px;
            }
            QPushButton {
                font-family: Cambria;
                background-color: #0078d7;
                color: white;
                text-align: center;
                text-decoration: none;
                font-size: 14px;
            }
            QLabel {
                color: #ffffff;
                font: Cambria 14px;
            }
        """)
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Failed Bolus Injection!")
            msg.setInformativeText("Amount exceeds the restriction.")
            msg.setWindowTitle("Failure")
            msg.setStandardButtons(QMessageBox.Ok)
            # palette = msg.palette()
            # palette.setColor(QPalette.Base, QColor("#ffffff"))
            # msg.setPalette(palette)
            msg.setStyleSheet("""
            QMessageBox {
                background-color: #2d2d2d;
                color: #ffffff;
                font: Cambria 14px;
            }
            QPushButton {
                font-family: Cambria;
                background-color: #0078d7;
                color: white;
                text-align: center;
                text-decoration: none;
                font-size: 14px;
            }
            QLabel {
                color: #ffffff;
                font: Cambria 14px;
            }
        """)
            msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog_physician = MainDialog()
    dialog_physician.show()
    dialog_patient = PatientDialog()
    dialog_patient.show()
    sys.exit(app.exec_())
