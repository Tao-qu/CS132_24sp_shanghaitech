from PyQt5 import QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QRect, Qt
from PyQt5.QtWidgets import QWidget

from Elevators import *


class GUI(QWidget):
    def __init__(self, elevators:Elevators):
        super().__init__()
        
        self.elevators = elevators
    
    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        MainWindow.setObjectName("MainWindow")
        
        for i in range(len(elevator_car_position)):
            elevator_car = QtWidgets.QGraphicsView(self)
            elevator_car.setGeometry(QRect(elevator_car_position[i][0], elevator_car_position[i][1], 130, 160))
            elevator_car.setStyleSheet("background-color: rgb(100, 100, 100);")
            elevator_car.setObjectName("elevator_car_#"+str(1+i))
            self.elevators.elevator_car.append(elevator_car)
            
            animation_elevator_car = QPropertyAnimation(elevator_car, b"geometry")
            animation_elevator_car.setDuration(1000)
            animation_elevator_car.setStartValue(QRect(elevator_car_position[i][0], elevator_car_position[i][1], 130, 160))
            animation_elevator_car.setEndValue(QRect(elevator_car_position[i][0], elevator_car_position[i][1], 130, 160))
            self.elevators.animation_elevator_car.append(animation_elevator_car)
            
        for i in range(len(elevator_outside_position)):
            for j in range(len(elevator_outside_position[i])):
                elevator_outside_background = QtWidgets.QGraphicsView(self)
                elevator_outside_background.setGeometry(QRect(elevator_outside_position[i][j][0], elevator_outside_position[i][j][1], 130, 160))
                elevator_outside_background.setStyleSheet("background-color: rgb(100, 100, 100);")
                elevator_outside_background.setObjectName("elevator_outside_background_#"+str(1+i)+"_"+str(j)+"F")
                self.elevators.elevator_outside_background[i].append(elevator_outside_background)
                
                elevator_outside_door_left = QtWidgets.QGraphicsView(self)
                elevator_outside_door_left.setGeometry(QRect(elevator_outside_position[i][j][0], elevator_outside_position[i][j][1], 64, 160))
                elevator_outside_door_left.setStyleSheet("background-color: rgb(160, 160, 160);")
                elevator_outside_door_left.setObjectName("elevator_outside_door_left_#"+str(1+i)+"_"+str(j)+"F")
                self.elevators.elevator_outside_door_left[i].append(elevator_outside_door_left)
                
                elevator_outside_door_right = QtWidgets.QGraphicsView(self)
                elevator_outside_door_right.setGeometry(QRect(elevator_outside_position[i][j][0]+66, elevator_outside_position[i][j][1], 64, 160))
                elevator_outside_door_right.setStyleSheet("background-color: rgb(160, 160, 160);")
                elevator_outside_door_right.setObjectName("elevator_outside_door_right_#"+str(1+i)+"_"+str(j)+"F")
                self.elevators.elevator_outside_door_right[i].append(elevator_outside_door_right)
                
                animation_outside_door_left = QPropertyAnimation(elevator_outside_door_left, b"geometry")
                animation_outside_door_left.setDuration(1000)
                animation_outside_door_left.setStartValue(QRect(elevator_outside_position[i][j][0], elevator_outside_position[i][j][1], 64, 160))
                animation_outside_door_left.setEndValue(QRect(elevator_outside_position[i][j][0], elevator_outside_position[i][j][1], 0, 160))
                self.elevators.animation_outside_door_left[i].append(animation_outside_door_left)
                
                animation_outside_door_right = QPropertyAnimation(elevator_outside_door_right, b"geometry")
                animation_outside_door_right.setDuration(1000)
                animation_outside_door_right.setStartValue(QRect(elevator_outside_position[i][j][0]+66, elevator_outside_position[i][j][1], 64, 160))
                animation_outside_door_right.setEndValue(QRect(elevator_outside_position[i][j][0]+130, elevator_outside_position[i][j][1], 0, 160))
                self.elevators.animation_outside_door_right[i].append(animation_outside_door_right)
                
        for i in range(len(label_floor_position)):
            label_floor = QtWidgets.QLabel(self)
            label_floor.setGeometry(QRect(label_floor_position[i][0], label_floor_position[i][1], 120, 20))
            label_floor.setAlignment(Qt.AlignCenter)
            if i == 0:
                label_floor.setText("-1F")
            else:
                label_floor.setText(str(i) + "F")
            label_floor.setObjectName("label_floor_" + str(i) + "F")
            self.elevators.label_floor.append(label_floor)
            
        for i in range(len(lcd_outside_position)):
            for j in range(len(lcd_outside_position[i])):
                lcd_outside = QtWidgets.QLCDNumber(self)
                lcd_outside.setGeometry(QRect(lcd_outside_position[i][j][0], lcd_outside_position[i][j][1], 50, 40))
                lcd_outside.setDigitCount(2)
                lcd_outside.setProperty("value", self.elevators.current_floor[i] if self.elevators.current_floor[i] > 0 else -1)
                lcd_outside.setStyleSheet("color: orange;")
                lcd_outside.setObjectName("lcd_outside_#"+str(1+i)+"_"+str(j)+"F")
                self.elevators.lcd_outside[i].append(lcd_outside)
                
        for i in range(len(state_outside_position)):
            for j in range(len(state_outside_position[i])):
                state_outside = QtWidgets.QGraphicsView(self)
                state_outside.setGeometry(QRect(state_outside_position[i][j][0], state_outside_position[i][j][1], 70, 60))
                state_outside.setStyleSheet("QGraphicsView{border-image: url(./res/state.png);}")
                state_outside.setObjectName("state_#"+str(1+i)+"_"+str(j)+"F")
                self.elevators.state_outside[i].append(state_outside)
                
        for i in range(len(button_up_position)):
            button_up = QtWidgets.QPushButton(self)
            button_up.setGeometry(QRect(button_up_position[i][0], button_up_position[i][1], 40, 40))
            button_up.setStyleSheet("QPushButton{border-image: url(./res/up.png);}"
                                    "QPushButton:hover{border-image: url(./res/up_hover.png);}"
                                    "QPushButton:pressed{border-image: url(./res/up_pressed.png);}")
            button_up.setObjectName("button_up_" + str(i) + "F")
            button_up.clicked.connect(self.button_outside_clicked)
            self.elevators.button_up.append(button_up)
            
        for i in range(len(button_down_position)):
            button_down = QtWidgets.QPushButton(self)
            button_down.setGeometry(QRect(button_down_position[i][0], button_down_position[i][1], 40, 40))
            button_down.setStyleSheet("QPushButton{border-image: url(./res/down.png);}"
                                      "QPushButton:hover{border-image: url(./res/down_hover.png);}"
                                      "QPushButton:pressed{border-image: url(./res/down_pressed.png);}")
            button_down.setObjectName("button_down_" + str(1+i) + "F")
            button_down.clicked.connect(self.button_outside_clicked)
            self.elevators.button_down.append(button_down)
        
        for i in range(len(elevator_inside_position)):
            elevator_inside_background = QtWidgets.QGraphicsView(self)
            elevator_inside_background.setGeometry(QRect(elevator_inside_position[i][0], elevator_inside_position[i][1], 260, 320))
            elevator_inside_background.setStyleSheet("background-color: rgb(100, 100, 100);")
            elevator_inside_background.setObjectName("elevator_inside_background_#" + str(1+i))
            self.elevators.elevator_inside_background.append(elevator_inside_background)
            
            elevator_inside_door_left = QtWidgets.QGraphicsView(self)
            elevator_inside_door_left.setGeometry(QRect(elevator_inside_position[i][0], elevator_inside_position[i][1], 128, 320))
            elevator_inside_door_left.setStyleSheet("background-color: rgb(160, 160, 160);")
            elevator_inside_door_left.setObjectName("elevator_inside_door_left_#" + str(1+i))
            self.elevators.elevator_inside_door_left.append(elevator_inside_door_left)
            
            elevator_inside_door_right = QtWidgets.QGraphicsView(self)
            elevator_inside_door_right.setGeometry(QRect(elevator_inside_position[i][0]+132, elevator_inside_position[i][1], 128, 320))
            elevator_inside_door_right.setStyleSheet("background-color: rgb(160, 160, 160);")
            elevator_inside_door_right.setObjectName("elevator_inside_door_right_#" + str(1+i))
            self.elevators.elevator_inside_door_right.append(elevator_inside_door_right)
            
            animation_inside_door_left = QPropertyAnimation(elevator_inside_door_left, b"geometry")
            animation_inside_door_left.setDuration(1000)
            animation_inside_door_left.setStartValue(QRect(elevator_inside_position[i][0], elevator_inside_position[i][1], 128, 320))
            animation_inside_door_left.setEndValue(QRect(elevator_inside_position[i][0], elevator_inside_position[i][1], 0, 320))
            self.elevators.animation_inside_door_left.append(animation_inside_door_left)
            
            animation_inside_door_right = QPropertyAnimation(elevator_inside_door_right, b"geometry")
            animation_inside_door_right.setDuration(1000)
            animation_inside_door_right.setStartValue(QRect(elevator_inside_position[i][0]+132, elevator_inside_position[i][1], 128, 320))
            animation_inside_door_right.setEndValue(QRect(elevator_inside_position[i][0]+260, elevator_inside_position[i][1], 0, 320))
            self.elevators.animation_inside_door_right.append(animation_inside_door_right)
            
        for i in range(len(label_elevator_position)):
            label_elevator = QtWidgets.QLabel(self)
            label_elevator.setGeometry(QRect(label_elevator_position[i][0], label_elevator_position[i][1], 160, 20))
            label_elevator.setAlignment(Qt.AlignCenter)
            label_elevator.setText("Elevator #" + str(1+i))
            label_elevator.setObjectName("label_elevator_#" + str(1+i))
            self.elevators.label_elevator.append(label_elevator)
        
        for i in range(len(lcd_inside_position)):
            lcd_inside = QtWidgets.QLCDNumber(self)
            lcd_inside.setGeometry(QRect(lcd_inside_position[i][0], lcd_inside_position[i][1], 75, 60))
            lcd_inside.setDigitCount(2)
            lcd_inside.setProperty("value", self.elevators.current_floor[i] if self.elevators.current_floor[i] > 0 else -1)
            lcd_inside.setStyleSheet("color: orange;")
            lcd_inside.setObjectName("lcd_inside_#" + str(1+i))
            self.elevators.lcd_inside.append(lcd_inside)
            
        for i in range(len(state_inside_position)):
            state_inside = QtWidgets.QGraphicsView(self)
            state_inside.setGeometry(QRect(state_inside_position[i][0], state_inside_position[i][1], 105, 90))
            state_inside.setStyleSheet("QGraphicsView{border-image: url(./res/state.png);}")
            state_inside.setObjectName("state_inside_#" + str(1+i))
            self.elevators.state_inside.append(state_inside)
            
        for i in range(len(button_emergency_position)):
            button_emergency = QtWidgets.QPushButton(self)
            button_emergency.setGeometry(QRect(button_emergency_position[i][0], button_emergency_position[i][1], 45, 45))
            button_emergency.setStyleSheet("QPushButton{border-image: url(./res/emergency.png);}"
                                           "QPushButton:hover{border-image: url(./res/emergency_hover.png);}"
                                           "QPushButton:pressed{border-image: url(./res/emergency_pressed.png);}")
            button_emergency.setObjectName("button_emergency_#" + str(1+i))
            button_emergency.clicked.connect(self.button_emergency_clicked)
            self.elevators.button_emergency.append(button_emergency)
            
        for i in range(len(button_floor_position)):
            for j in range(len(button_floor_position[i])):
                button_floor = QtWidgets.QPushButton(self)
                button_floor.setGeometry(QRect(button_floor_position[i][j][0], button_floor_position[i][j][1], 45, 45))
                button_floor.setStyleSheet("QPushButton{border-image: url(./res/" + str(j) + "F.png);}"
                                            "QPushButton:hover{border-image: url(./res/" + str(j) + "F_hover.png);}"
                                            "QPushButton:pressed{border-image: url(./res/" + str(j) + "F_pressed.png);}")
                button_floor.setObjectName("button_floor_#" + str(1+i) + "_" + str(j) + "F")
                button_floor.clicked.connect(self.button_floor_clicked)
                self.elevators.button_floor[i].append(button_floor)
                
        for i in range(len(button_open_position)):
            button_open = QtWidgets.QPushButton(self)
            button_open.setGeometry(QRect(button_open_position[i][0], button_open_position[i][1], 45, 45))
            button_open.setStyleSheet("QPushButton{border-image: url(./res/open.png);}"
                                      "QPushButton:hover{border-image: url(./res/open_hover.png);}"
                                      "QPushButton:pressed{border-image: url(./res/open_pressed.png);}")
            button_open.setObjectName("button_open_#" + str(1+i))
            button_open.clicked.connect(self.button_open_clicked)
            self.elevators.button_open.append(button_open)
            
        for i in range(len(button_close_position)):
            button_close = QtWidgets.QPushButton(self)
            button_close.setGeometry(QRect(button_close_position[i][0], button_close_position[i][1], 45, 45))
            button_close.setStyleSheet("QPushButton{border-image: url(./res/close.png);}"
                                       "QPushButton:hover{border-image: url(./res/close_hover.png);}"
                                       "QPushButton:pressed{border-image: url(./res/close_pressed.png);}")
            button_close.setObjectName("button_close_#" + str(1+i))
            button_close.clicked.connect(self.button_close_clicked)
            self.elevators.button_close.append(button_close)
            
    def button_outside_clicked(self):
        floor = int(self.sender().objectName().split('_')[-1][:-1])
        if self.sender().objectName().split('_')[1] == 'up':
                button = self.elevators.button_up[floor if floor > 0 else 0]
                self.elevators.outside_up_queue.append(floor)
                self.elevators.outside_up_queue.sort()
                button.setStyleSheet("QPushButton{border-image: url(./res/up_pressed.png);}")
                button.setEnabled(False)
        else:
            button = self.elevators.button_down[floor-1]
            self.elevators.outside_down_queue.append(floor)
            self.elevators.outside_down_queue.sort()
            button.setStyleSheet("QPushButton{border-image: url(./res/down_pressed.png);}")
            button.setEnabled(False)
            
    def button_floor_clicked(self):
        if self.sender().objectName().split('_')[-1] != "clciked":
            elevator = int(self.sender().objectName().split('_')[-2][1])
            floor = int(self.sender().objectName().split('_')[-1][:-1])
            button = self.elevators.button_floor[elevator-1][floor]
            self.elevators.inside_queue[elevator - 1].append(floor)
            self.elevators.inside_queue[elevator - 1].sort()
            button.setStyleSheet("QPushButton{border-image: url(./res/" + str(floor) + "F_pressed.png);}")
            button.setObjectName("button_floor_#" + str(elevator) + "_" + str(floor) + "F_clciked")
        elif self.sender().objectName().split('_')[-1] == "clciked":
            elevator = int(self.sender().objectName().split('_')[-3][1])
            floor = int(self.sender().objectName().split('_')[-2][:-1])
            button = self.elevators.button_floor[elevator-1][floor]
            if self.elevators.inside_queue[elevator - 1].count(floor):
                self.elevators.inside_queue[elevator - 1].remove(floor)
            if self.elevators.elevator_execute_trace_queue[elevator - 1][0].count(floor):
                self.elevators.elevator_execute_trace_queue[elevator - 1][0].remove(floor)
                if not self.elevators.elevator_execute_trace_queue[elevator - 1][1].count(floor) and not self.elevators.elevator_execute_trace_queue[elevator - 1][2].count(floor):
                    self.elevators.elevator_execute_queue[elevator - 1].remove(floor)
            button.setStyleSheet("QPushButton{border-image: url(./res/" + str(floor) + "F.png);}"
                                 "QPushButton:hover{border-image: url(./res/" + str(floor) + "F_hover.png);}"
                                 "QPushButton:pressed{border-image: url(./res/" + str(floor) + "F_pressed.png);}")
            button.setObjectName("button_floor_#" + str(elevator) + "_" + str(floor) + "F")
            
    # def button_floor_clicked(self):
    #     elevator = int(self.sender().objectName().split('_')[-2][1])
    #     floor = int(self.sender().objectName().split('_')[-1][:-1])
    #     button = self.elevators.button_floor[elevator-1][floor]
    #     self.elevators.inside_queue[elevator - 1].append(floor)
    #     self.elevators.inside_queue[elevator - 1].sort()
    #     button.setStyleSheet("QPushButton{border-image: url(./res/" + str(floor) + "F_pressed.png);}")
    #     # button.clicked.disconnect(self.button_floor_clciked)
    #     # button.clicked.connect(self.button_floor_clicked_cancel)
        
    # def button_floor_clicked_cancel(self):
    #     elevator = int(self.sender().objectName().split('_')[-2][1])
    #     floor = int(self.sender().objectName().split('_')[-1][:-1])
    #     button = self.elevators.button_floor[elevator-1][floor]
    #     if self.elevators.inside_queue[elevator - 1].count(floor):
    #         self.elevators.inside_queue[elevator - 1].remove(floor)
    #     if self.elevators.elevator_execute_trace_queue[elevator - 1][0].count(floor):
    #         self.elevators.elevator_execute_trace_queue[elevator - 1][0].remove(floor)
    #         if not self.elevators.elevator_execute_trace_queue[elevator - 1][1].count(floor) and not self.elevators.elevator_execute_trace_queue[elevator - 1][2].count(floor):
    #             self.elevators.elevator_execute_queue[elevator - 1].remove(floor)
    #     button.setStyleSheet("QPushButton{border-image: url(./res/" + str(floor) + "F.png);}"
    #                          "QPushButton:hover{border-image: url(./res/" + str(floor) + "F_hover.png);}"
    #                             "QPushButton:pressed{border-image: url(./res/" + str(floor) + "F_pressed.png);}")
    #     button.clicked.disconnect(self.button_floor_clicked_cancel)
    #     button.clicked.connect(self.button_floor_clicked)
                
    def button_open_clicked(self):
        elevator = int(self.sender().objectName().split('_')[-1][1])
        if (self.elevators.elevator_state[elevator - 1] == IDLE and self.elevators.elevator_door[elevator - 1] == PAUSE) or (self.elevators.elevator_door[elevator - 1] == CLOSE):
            self.elevators.animation_open(elevator - 1, int(self.elevators.current_floor[elevator - 1]))
            
    def button_close_clicked(self):
        elevator = int(self.sender().objectName().split('_')[-1][1])
        if (self.elevators.elevator_door[elevator - 1] == OPEN) or (self.elevators.elevator_door[elevator - 1] == HOLD):
            self.elevators.animation_close(elevator - 1, int(self.elevators.current_floor[elevator - 1]))
            
    def button_emergency_clicked(self):
        pass