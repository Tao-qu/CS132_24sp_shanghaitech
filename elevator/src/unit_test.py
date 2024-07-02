import unittest
import time
from PyQt5 import QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QRect, Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
# import Dispatcher
from main import mywindow
from GUI import *
from Dispatcher import *
from Porter import *

# Create test environment
app = QApplication([])


class TestElevatorFunc(unittest.TestCase):
    def setUp(self):
        self.elevators = Elevators()
        self.porter = Porter(self.elevators)
        self.dispatcher = Dispatcher(self.porter)
        self.window = mywindow(self.elevators)

    def testAutoDoorOpen(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [1, 1]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[2], []]
        self.elevators.inside_queue = [[2], []]
        while (self.elevators.current_floor[0] != 2):
            self.dispatcher.update()

        self.dispatcher.update()
        self.assertEqual(self.elevators.elevator_door[0], OPEN)
        self.dispatcher.update()
        self.assertEqual(self.elevators.elevator_door[0], HOLD)
        self.dispatcher.update()
        self.assertEqual(self.elevators.elevator_door[0], CLOSE)
        self.assertEqual(len(self.elevators.elevator_execute_queue[0]), 0)

    def testValidDoorOpen(self):
        def ClickOpen_(self, elevator):
            if (self.elevators.elevator_state[elevator - 1] == IDLE and self.elevators.elevator_door[elevator - 1] == PAUSE) or (self.elevators.elevator_door[elevator - 1] == CLOSE):
                self.elevators.animation_open(
                    elevator - 1, int(self.elevators.current_floor[elevator - 1]))
        ClickOpen_(self, 1)
        self.assertEqual(self.elevators.elevator_door[0], OPEN)
        self.dispatcher.update()
        self.assertEqual(self.elevators.elevator_door[0], HOLD)
        self.dispatcher.update()
        self.assertEqual(self.elevators.elevator_door[0], CLOSE)
        self.dispatcher.update()
        ClickOpen_(self, 1)
        self.assertEqual(self.elevators.elevator_door[0], OPEN)

    def testInvalidDoorOpen(self):
        def ClickOpen_(self, elevator):
            if (self.elevators.elevator_state[elevator - 1] == IDLE and self.elevators.elevator_door[elevator - 1] == PAUSE) or (self.elevators.elevator_door[elevator - 1] == CLOSE):
                self.elevators.animation_open(
                    elevator - 1, int(self.elevators.current_floor[elevator - 1]))
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [1, 1]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[2], []]
        self.elevators.inside_queue = [[2], []]
        self.dispatcher.update()
        ClickOpen_(self, 1)
        self.assertEqual(self.elevators.elevator_door[0], PAUSE)

    def testDoorClose(self):
        def ClickOpen_(self, elevator):
            if (self.elevators.elevator_state[elevator - 1] == IDLE and self.elevators.elevator_door[elevator - 1] == PAUSE) or (self.elevators.elevator_door[elevator - 1] == CLOSE):
                self.elevators.animation_open(
                    elevator - 1, int(self.elevators.current_floor[elevator - 1]))

        def ClickClose_(self, elevator):
            if (self.elevators.elevator_door[elevator - 1] == OPEN) or (self.elevators.elevator_door[elevator - 1] == HOLD):
                self.elevators.animation_close(
                    elevator - 1, int(self.elevators.current_floor[elevator - 1]))
        ClickOpen_(self, 1)
        self.assertEqual(self.elevators.elevator_door[0], OPEN)
        self.dispatcher.update()
        ClickClose_(self, 1)
        self.assertEqual(self.elevators.elevator_door[0], CLOSE)
        self.dispatcher.update()
        self.assertEqual(self.elevators.elevator_door[0], PAUSE)

    def testInsideButton_other(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [1, 1]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[], []]
        self.elevators.inside_queue = [[], []]

        def button_floor_clicked_(self, elevator, floor):
            button = self.elevators.button_floor[elevator-1][floor]
            self.elevators.inside_queue[elevator - 1].append(floor)
            self.elevators.inside_queue[elevator - 1].sort()
            button.setStyleSheet(
                "QPushButton{border-image: url(./res/" + str(floor) + "F_pressed.png);}")
            button.setEnabled(False)

        button_floor_clicked_(self, 1, 0)
        floor_list = []
        elevator_state_list = []
        door_state_list = []
        cnt = 0
        while (cnt <= 20):
            floor_list.append(self.elevators.current_floor[1])
            elevator_state_list.append(self.elevators.elevator_state[1])
            door_state_list.append(self.elevators.elevator_door[1])
            self.dispatcher.update()
            cnt += 1

        def removerepeat(list_):
            new_list = list(set(list_))
            new_list.sort(key=list_.index)
            return new_list
        self.assertEqual(removerepeat(floor_list), [1])
        self.assertEqual(removerepeat(elevator_state_list), [IDLE])
        self.assertEqual(removerepeat(door_state_list), [
                         PAUSE])

    def testInsideBotton_1_b(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [1, 1]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[], []]
        self.elevators.inside_queue = [[], []]

        def button_floor_clicked_(self, elevator, floor):
            button = self.elevators.button_floor[elevator-1][floor]
            self.elevators.inside_queue[elevator - 1].append(floor)
            self.elevators.inside_queue[elevator - 1].sort()
            button.setStyleSheet(
                "QPushButton{border-image: url(./res/" + str(floor) + "F_pressed.png);}")
            button.setEnabled(False)

        button_floor_clicked_(self, 1, 0)
        floor_list = []
        elevator_state_list = []
        cnt = 0
        while (cnt <= 20):
            floor_list.append(self.elevators.current_floor[0])
            elevator_state_list.append(self.elevators.elevator_state[0])
            self.dispatcher.update()
            cnt += 1

        def removerepeat(list_):
            new_list = list(set(list_))
            new_list.sort(key=list_.index)
            return new_list
        self.assertEqual(removerepeat(floor_list), [1, 0.5, 0])
        self.assertEqual(removerepeat(elevator_state_list), [IDLE, DOWN])

    def testInsideBotton_1_1(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [2, 2]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[], []]
        self.elevators.inside_queue = [[], []]

        def button_floor_clicked_(self, elevator, floor):
            button = self.elevators.button_floor[elevator-1][floor]
            self.elevators.inside_queue[elevator - 1].append(floor)
            self.elevators.inside_queue[elevator - 1].sort()
            button.setStyleSheet(
                "QPushButton{border-image: url(./res/" + str(floor) + "F_pressed.png);}")
            button.setEnabled(False)

        button_floor_clicked_(self, 1, 1)
        floor_list = []
        elevator_state_list = []
        cnt = 0
        while (cnt <= 20):
            floor_list.append(self.elevators.current_floor[0])
            elevator_state_list.append(self.elevators.elevator_state[0])
            self.dispatcher.update()
            cnt += 1

        def removerepeat(list_):
            new_list = list(set(list_))
            new_list.sort(key=list_.index)
            return new_list
        self.assertEqual(removerepeat(floor_list), [2, 1.5, 1])
        self.assertEqual(removerepeat(elevator_state_list), [IDLE, DOWN])

    def testInsideBotton_1_1_opposite(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [0, 0]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[], []]
        self.elevators.inside_queue = [[], []]

        def button_floor_clicked_(self, elevator, floor):
            button = self.elevators.button_floor[elevator-1][floor]
            self.elevators.inside_queue[elevator - 1].append(floor)
            self.elevators.inside_queue[elevator - 1].sort()
            button.setStyleSheet(
                "QPushButton{border-image: url(./res/" + str(floor) + "F_pressed.png);}")
            button.setEnabled(False)

        button_floor_clicked_(self, 1, 1)
        floor_list = []
        elevator_state_list = []
        cnt = 0
        while (cnt <= 20):
            floor_list.append(self.elevators.current_floor[0])
            elevator_state_list.append(self.elevators.elevator_state[0])
            self.dispatcher.update()
            cnt += 1

        def removerepeat(list_):
            new_list = list(set(list_))
            new_list.sort(key=list_.index)
            return new_list
        self.assertEqual(removerepeat(floor_list), [0, 0.5, 1])
        self.assertEqual(removerepeat(elevator_state_list), [IDLE, UP])

    def testInsideBotton_1_2(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [0, 0]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[], []]
        self.elevators.inside_queue = [[], []]

        def button_floor_clicked_(self, elevator, floor):
            button = self.elevators.button_floor[elevator-1][floor]
            self.elevators.inside_queue[elevator - 1].append(floor)
            self.elevators.inside_queue[elevator - 1].sort()
            button.setStyleSheet(
                "QPushButton{border-image: url(./res/" + str(floor) + "F_pressed.png);}")
            button.setEnabled(False)

        button_floor_clicked_(self, 1, 2)
        floor_list = []
        elevator_state_list = []
        cnt = 0
        while (cnt <= 40):
            floor_list.append(self.elevators.current_floor[0])
            elevator_state_list.append(self.elevators.elevator_state[0])
            self.dispatcher.update()
            cnt += 1

        def removerepeat(list_):
            new_list = list(set(list_))
            new_list.sort(key=list_.index)
            return new_list
        self.assertEqual(removerepeat(floor_list), [0, 0.5, 1, 1.5, 2])
        self.assertEqual(removerepeat(elevator_state_list), [IDLE, UP])

    def testInsideBotton_1_3(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [0, 0]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[], []]
        self.elevators.inside_queue = [[], []]

        def button_floor_clicked_(self, elevator, floor):
            button = self.elevators.button_floor[elevator-1][floor]
            self.elevators.inside_queue[elevator - 1].append(floor)
            self.elevators.inside_queue[elevator - 1].sort()
            button.setStyleSheet(
                "QPushButton{border-image: url(./res/" + str(floor) + "F_pressed.png);}")
            button.setEnabled(False)

        button_floor_clicked_(self, 1, 3)
        floor_list = []
        elevator_state_list = []
        cnt = 0
        while (cnt <= 60):
            floor_list.append(self.elevators.current_floor[0])
            elevator_state_list.append(self.elevators.elevator_state[0])
            self.dispatcher.update()
            cnt += 1

        def removerepeat(list_):
            new_list = list(set(list_))
            new_list.sort(key=list_.index)
            return new_list
        self.assertEqual(removerepeat(floor_list), [0, 0.5, 1, 1.5, 2, 2.5, 3])
        self.assertEqual(removerepeat(elevator_state_list), [IDLE, UP])

    def testInsideBotton_2_1(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [0, 0]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[], []]
        self.elevators.inside_queue = [[], []]

        def button_floor_clicked_(self, elevator, floor):
            button = self.elevators.button_floor[elevator-1][floor]
            self.elevators.inside_queue[elevator - 1].append(floor)
            self.elevators.inside_queue[elevator - 1].sort()
            button.setStyleSheet(
                "QPushButton{border-image: url(./res/" + str(floor) + "F_pressed.png);}")
            button.setEnabled(False)

        button_floor_clicked_(self, 2, 1)
        floor_list = []
        elevator_state_list = []
        cnt = 0
        while (cnt <= 20):
            floor_list.append(self.elevators.current_floor[1])
            elevator_state_list.append(self.elevators.elevator_state[1])
            self.dispatcher.update()
            cnt += 1

        def removerepeat(list_):
            new_list = list(set(list_))
            new_list.sort(key=list_.index)
            return new_list
        self.assertEqual(removerepeat(floor_list), [0, 0.5, 1])
        self.assertEqual(removerepeat(elevator_state_list), [IDLE, UP])

    def testOutsideButton_b_1(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [0, 1]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[], []]
        self.elevators.inside_queue = [[], []]

        def button_outside_clicked_(self, floor, direction):
            if direction == 'up':
                button = self.elevators.button_up[floor if floor > 0 else 0]
                self.elevators.outside_up_queue.append(floor)
                self.elevators.outside_up_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/up_pressed.png);}")
                button.setEnabled(False)
            else:
                button = self.elevators.button_down[floor-1]
                self.elevators.outside_down_queue.append(floor)
                self.elevators.outside_down_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/down_pressed.png);}")
                button.setEnabled(False)
        button_outside_clicked_(self, 0, 'up')
        floor_list_1 = []
        elevator_state_list_1 = []
        floor_list_2 = []
        elevator_state_list_2 = []
        cnt = 0
        while (cnt <= 60):
            floor_list_1.append(self.elevators.current_floor[0])
            elevator_state_list_1.append(self.elevators.elevator_state[0])
            floor_list_2.append(self.elevators.current_floor[1])
            elevator_state_list_2.append(self.elevators.elevator_state[1])
            self.dispatcher.update()
            cnt += 1

        def removerepeat(list_):
            new_list = list(set(list_))
            new_list.sort(key=list_.index)
            return new_list
        self.assertEqual(removerepeat(floor_list_1), [0])
        self.assertEqual(removerepeat(elevator_state_list_1), [IDLE, UP])
        self.assertEqual(removerepeat(floor_list_2), [1])
        self.assertEqual(removerepeat(elevator_state_list_2), [IDLE])

    def testOutsideButton_b_2(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [2, 1]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[], []]
        self.elevators.inside_queue = [[], []]

        def button_outside_clicked_(self, floor, direction):
            if direction == 'up':
                button = self.elevators.button_up[floor if floor > 0 else 0]
                self.elevators.outside_up_queue.append(floor)
                self.elevators.outside_up_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/up_pressed.png);}")
                button.setEnabled(False)
            else:
                button = self.elevators.button_down[floor-1]
                self.elevators.outside_down_queue.append(floor)
                self.elevators.outside_down_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/down_pressed.png);}")
                button.setEnabled(False)
        button_outside_clicked_(self, 0, 'up')
        floor_list_1 = []
        elevator_state_list_1 = []
        floor_list_2 = []
        elevator_state_list_2 = []
        cnt = 0
        while (cnt <= 60):
            floor_list_1.append(self.elevators.current_floor[0])
            elevator_state_list_1.append(self.elevators.elevator_state[0])
            floor_list_2.append(self.elevators.current_floor[1])
            elevator_state_list_2.append(self.elevators.elevator_state[1])
            self.dispatcher.update()
            cnt += 1

        def removerepeat(list_):
            new_list = list(set(list_))
            new_list.sort(key=list_.index)
            return new_list
        self.assertEqual(removerepeat(floor_list_1), [2])
        self.assertEqual(removerepeat(elevator_state_list_1), [IDLE])
        self.assertEqual(removerepeat(floor_list_2), [1, 0.5, 0])
        self.assertEqual(removerepeat(elevator_state_list_2),
                         [IDLE, DOWN_UP, UP])

    def testOutsideButton_1_up(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [0, 3]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[], []]
        self.elevators.inside_queue = [[], []]

        def button_outside_clicked_(self, floor, direction):
            if direction == 'up':
                button = self.elevators.button_up[floor if floor > 0 else 0]
                self.elevators.outside_up_queue.append(floor)
                self.elevators.outside_up_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/up_pressed.png);}")
                button.setEnabled(False)
            else:
                button = self.elevators.button_down[floor-1]
                self.elevators.outside_down_queue.append(floor)
                self.elevators.outside_down_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/down_pressed.png);}")
                button.setEnabled(False)
        button_outside_clicked_(self, 1, 'up')
        floor_list_1 = []
        elevator_state_list_1 = []
        floor_list_2 = []
        elevator_state_list_2 = []
        cnt = 0
        while (cnt <= 60):
            floor_list_1.append(self.elevators.current_floor[0])
            elevator_state_list_1.append(self.elevators.elevator_state[0])
            floor_list_2.append(self.elevators.current_floor[1])
            elevator_state_list_2.append(self.elevators.elevator_state[1])
            self.dispatcher.update()
            cnt += 1

        def removerepeat(list_):
            new_list = list(set(list_))
            new_list.sort(key=list_.index)
            return new_list
        self.assertEqual(removerepeat(floor_list_1), [0, 0.5, 1])
        self.assertEqual(removerepeat(elevator_state_list_1), [IDLE, UP])
        self.assertEqual(removerepeat(floor_list_2), [3])
        self.assertEqual(removerepeat(elevator_state_list_2),
                         [IDLE])

    def testOutsideButton_1_down(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [0, 3]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[], []]
        self.elevators.inside_queue = [[], []]

        def button_outside_clicked_(self, floor, direction):
            if direction == 'up':
                button = self.elevators.button_up[floor if floor > 0 else 0]
                self.elevators.outside_up_queue.append(floor)
                self.elevators.outside_up_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/up_pressed.png);}")
                button.setEnabled(False)
            else:
                button = self.elevators.button_down[floor-1]
                self.elevators.outside_down_queue.append(floor)
                self.elevators.outside_down_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/down_pressed.png);}")
                button.setEnabled(False)
        button_outside_clicked_(self, 1, 'down')
        floor_list_1 = []
        elevator_state_list_1 = []
        floor_list_2 = []
        elevator_state_list_2 = []
        cnt = 0
        while (cnt <= 60):
            floor_list_1.append(self.elevators.current_floor[0])
            elevator_state_list_1.append(self.elevators.elevator_state[0])
            floor_list_2.append(self.elevators.current_floor[1])
            elevator_state_list_2.append(self.elevators.elevator_state[1])
            self.dispatcher.update()
            cnt += 1

        def removerepeat(list_):
            new_list = list(set(list_))
            new_list.sort(key=list_.index)
            return new_list
        self.assertEqual(removerepeat(floor_list_1), [0, 0.5, 1])
        self.assertEqual(removerepeat(elevator_state_list_1),
                         [IDLE, UP_DOWN, DOWN])
        self.assertEqual(removerepeat(floor_list_2), [3])
        self.assertEqual(removerepeat(elevator_state_list_2),
                         [IDLE])

    def testOutsideButton_2_up(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [0, 3]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[], []]
        self.elevators.inside_queue = [[], []]

        def button_outside_clicked_(self, floor, direction):
            if direction == 'up':
                button = self.elevators.button_up[floor if floor > 0 else 0]
                self.elevators.outside_up_queue.append(floor)
                self.elevators.outside_up_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/up_pressed.png);}")
                button.setEnabled(False)
            else:
                button = self.elevators.button_down[floor-1]
                self.elevators.outside_down_queue.append(floor)
                self.elevators.outside_down_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/down_pressed.png);}")
                button.setEnabled(False)
        button_outside_clicked_(self, 2, 'up')
        floor_list_1 = []
        elevator_state_list_1 = []
        floor_list_2 = []
        elevator_state_list_2 = []
        cnt = 0
        while (cnt <= 60):
            floor_list_1.append(self.elevators.current_floor[0])
            elevator_state_list_1.append(self.elevators.elevator_state[0])
            floor_list_2.append(self.elevators.current_floor[1])
            elevator_state_list_2.append(self.elevators.elevator_state[1])
            self.dispatcher.update()
            cnt += 1

        def removerepeat(list_):
            new_list = list(set(list_))
            new_list.sort(key=list_.index)
            return new_list
        self.assertEqual(removerepeat(floor_list_1), [0])
        self.assertEqual(removerepeat(elevator_state_list_1),
                         [IDLE])
        self.assertEqual(removerepeat(floor_list_2), [3, 2.5, 2])
        self.assertEqual(removerepeat(elevator_state_list_2),
                         [IDLE, DOWN_UP, UP])

    def testOutsideButton_2_down(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [0, 3]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[], []]
        self.elevators.inside_queue = [[], []]

        def button_outside_clicked_(self, floor, direction):
            if direction == 'up':
                button = self.elevators.button_up[floor if floor > 0 else 0]
                self.elevators.outside_up_queue.append(floor)
                self.elevators.outside_up_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/up_pressed.png);}")
                button.setEnabled(False)
            else:
                button = self.elevators.button_down[floor-1]
                self.elevators.outside_down_queue.append(floor)
                self.elevators.outside_down_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/down_pressed.png);}")
                button.setEnabled(False)
        button_outside_clicked_(self, 2, 'down')
        floor_list_1 = []
        elevator_state_list_1 = []
        floor_list_2 = []
        elevator_state_list_2 = []
        cnt = 0
        while (cnt <= 60):
            floor_list_1.append(self.elevators.current_floor[0])
            elevator_state_list_1.append(self.elevators.elevator_state[0])
            floor_list_2.append(self.elevators.current_floor[1])
            elevator_state_list_2.append(self.elevators.elevator_state[1])
            self.dispatcher.update()
            cnt += 1

        def removerepeat(list_):
            new_list = list(set(list_))
            new_list.sort(key=list_.index)
            return new_list
        self.assertEqual(removerepeat(floor_list_1), [0])
        self.assertEqual(removerepeat(elevator_state_list_1),
                         [IDLE])
        self.assertEqual(removerepeat(floor_list_2), [3, 2.5, 2])
        self.assertEqual(removerepeat(elevator_state_list_2),
                         [IDLE, DOWN])

    def testOutsideButton_3_1(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [3, 2]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[], []]
        self.elevators.inside_queue = [[], []]

        def button_outside_clicked_(self, floor, direction):
            if direction == 'up':
                button = self.elevators.button_up[floor if floor > 0 else 0]
                self.elevators.outside_up_queue.append(floor)
                self.elevators.outside_up_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/up_pressed.png);}")
                button.setEnabled(False)
            else:
                button = self.elevators.button_down[floor-1]
                self.elevators.outside_down_queue.append(floor)
                self.elevators.outside_down_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/down_pressed.png);}")
                button.setEnabled(False)
        button_outside_clicked_(self, 3, 'down')
        floor_list_1 = []
        elevator_state_list_1 = []
        floor_list_2 = []
        elevator_state_list_2 = []
        cnt = 0
        while (cnt <= 60):
            floor_list_1.append(self.elevators.current_floor[0])
            elevator_state_list_1.append(self.elevators.elevator_state[0])
            floor_list_2.append(self.elevators.current_floor[1])
            elevator_state_list_2.append(self.elevators.elevator_state[1])
            self.dispatcher.update()
            cnt += 1

        def removerepeat(list_):
            new_list = list(set(list_))
            new_list.sort(key=list_.index)
            return new_list
        self.assertEqual(removerepeat(floor_list_1), [3])
        self.assertEqual(removerepeat(elevator_state_list_1), [IDLE, DOWN])
        self.assertEqual(removerepeat(floor_list_2), [2])
        self.assertEqual(removerepeat(elevator_state_list_2), [IDLE])

    def testOutsideButton_3_2(self):
        self.elevators.elevator_state = [IDLE, IDLE]
        self.elevators.current_floor = [1, 2]
        self.elevators.elevator_door = [PAUSE, PAUSE]
        self.elevators.elevator_execute_queue = [[], []]
        self.elevators.inside_queue = [[], []]

        def button_outside_clicked_(self, floor, direction):
            if direction == 'up':
                button = self.elevators.button_up[floor if floor > 0 else 0]
                self.elevators.outside_up_queue.append(floor)
                self.elevators.outside_up_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/up_pressed.png);}")
                button.setEnabled(False)
            else:
                button = self.elevators.button_down[floor-1]
                self.elevators.outside_down_queue.append(floor)
                self.elevators.outside_down_queue.sort()
                button.setStyleSheet(
                    "QPushButton{border-image: url(./res/down_pressed.png);}")
                button.setEnabled(False)
        button_outside_clicked_(self, 3, 'down')
        floor_list_1 = []
        elevator_state_list_1 = []
        floor_list_2 = []
        elevator_state_list_2 = []
        cnt = 0
        while (cnt <= 60):
            floor_list_1.append(self.elevators.current_floor[0])
            elevator_state_list_1.append(self.elevators.elevator_state[0])
            floor_list_2.append(self.elevators.current_floor[1])
            elevator_state_list_2.append(self.elevators.elevator_state[1])
            self.dispatcher.update()
            cnt += 1

        def removerepeat(list_):
            new_list = list(set(list_))
            new_list.sort(key=list_.index)
            return new_list
        self.assertEqual(removerepeat(floor_list_1), [1])
        self.assertEqual(removerepeat(elevator_state_list_1), [IDLE])
        self.assertEqual(removerepeat(floor_list_2), [2, 2.5, 3])
        self.assertEqual(removerepeat(elevator_state_list_2),
                         [IDLE, UP_DOWN, DOWN])


if __name__ == "__main__":
    unittest.main()
