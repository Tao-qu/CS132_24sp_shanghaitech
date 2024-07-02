import sys
import os

# 添加 src 目录到 sys.path
current_dir = os.path.dirname(__file__)
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.append(src_dir)
import unittest
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from main import MainDialog, PatientDialog
import database

# Create test environment
app = QApplication([])

class TestMedicalApplication(unittest.TestCase):
    def setUp(self):
        # Setup executed before each test case
        self.dialog_physician = MainDialog()
        self.dialog_patient = PatientDialog()

    def test_adjust_baseline_amount(self):
        # T1.1: Corresponds to S1.1
        # Tests adjusting the baseline amount
        self.dialog_physician.ui.horizontalSlider.setValue(50)  # Set to 0.05 ml/min
        self.assertEqual(database.baseline_amount, 0.05)
        # Open switch to update UI
        QTest.mouseClick(self.dialog_physician.ui.StartBaselineBottom, Qt.LeftButton)
        self.assertIn("0.05", self.dialog_physician.ui.label_11.text())

    def test_set_bolus_amount(self):
        # T1.2: Corresponds to S1.2
        # Tests setting the bolus amount
        self.dialog_physician.ui.horizontalSlider_2.setValue(300)  # Set to 0.3 ml/shot
        self.assertEqual(database.bolus_amount, 0.3)
        self.assertIn("0.3", self.dialog_physician.ui.label_12.text())

    def test_baseline_switch(self):
        # T1.3: Corresponds to S1.3
        # Tests baseline switch
        initial_state = database.switch_on
        QTest.mouseClick(self.dialog_physician.ui.StartBaselineBottom, Qt.LeftButton)
        self.assertNotEqual(database.switch_on, initial_state)
        expected_text = "The switch is on." if database.switch_on == 1 else "The switch is off."
        self.assertIn(expected_text, self.dialog_physician.ui.switchlabel.text())

    def test_amount_calculation(self):
        # T1.4: Corresponds to S1.4
        # Tests amount calculation
        current_time = time.time()
        database.baseline_timeline_list.append([current_time - 3600, 0.01])
        database.bolus_timeline_list.append([current_time - 1800, 0.2])
        self.assertTrue(database.calculate_1_h(database.baseline_timeline_list, database.bolus_timeline_list, current_time) > 0)
        self.assertTrue(database.calculate_24_h(database.baseline_timeline_list, database.bolus_timeline_list, current_time) > 0)

    def test_decide_baseline_state(self):
        # T1.5: Corresponds to S1.5
        # Tests deciding baseline state
        if database.switch_on == 0:
            QTest.mouseClick(self.dialog_physician.ui.StartBaselineBottom, Qt.LeftButton)
        database.baseline_amount = 0.01
        self.dialog_physician.start_baseline()
        self.assertIn("Baseline: off", self.dialog_physician.ui.baselinelabel.text())

    def test_reset_injection_records(self):
        # T1.6: Corresponds to S1.6
        # Tests resetting injection records
        database.baseline_timeline_list.append([time.time(), 0.01])
        database.bolus_timeline_list.append([time.time(), 0.2])
        QTest.mouseClick(self.dialog_physician.ui.RstButton, Qt.LeftButton)
        self.assertEqual(len(database.baseline_timeline_list), 0)
        self.assertEqual(len(database.bolus_timeline_list), 0)

    def test_inject_bolus(self):
        # T2.1: Corresponds to S2.1
        # Tests bolus injection
        database.bolus_amount = 0.2
        QTest.mouseClick(self.dialog_patient.ui.InjectionButtom_2, Qt.LeftButton)
        self.assertTrue(len(database.bolus_timeline_list) > 0)

    def test_update(self):
        # T3.1: Corresponds to S3.1
        # Tests update functionality
        database.baseline_timeline_list.append([time.time() - 3600, 0.01])
        database.current_time = time.time()
        self.dialog_physician.update()
        current_amount = database.baseline_timeline_list[-1][1]
        if database.switch_on == 1 and current_amount != database.baseline_amount:
            self.assertEqual(current_amount, database.baseline_amount)
        elif database.switch_on == 0 and current_amount != 0:
            self.assertEqual(current_amount, 0)
            
    def tearDown(self):
        self.dialog_physician.close()
        self.dialog_patient.close()

if __name__ == "__main__":
    unittest.main()
