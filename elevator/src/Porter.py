from PyQt5.QtCore import QTimer

from NetClient import *
from Elevators import *

CHECK_INTERVAL = 100


class Porter:
    def __init__(self, elevators:Elevators):
        self.elevators = elevators
        
        self.identity = "TeamX"
        self.zmqThread = ZmqClientThread(identity=self.identity)
        self.timeStamp = -1 
        self.serverMessage = "" 
        self.messageUnprocessed = False
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_message)
        self.timer.start(CHECK_INTERVAL)
    
    def is_received_new_message(self, oldTimeStamp:int, oldServerMessage:str, Msgunprocessed:bool = False)->bool:
        if(Msgunprocessed):
            return True
        else:
            if(oldTimeStamp == self.zmqThread.messageTimeStamp and 
            oldServerMessage == self.zmqThread.receivedMessage):
                return False
            else:
                return True
            
    def check_message(self):
        if self.is_received_new_message(self.timeStamp, self.serverMessage, self.messageUnprocessed):
            if not self.messageUnprocessed:
                self.timeStamp = self.zmqThread.messageTimeStamp
                self.serverMessage = self.zmqThread.receivedMessage
            self.messageUnprocessed = False
            
            if "call_up" in self.serverMessage:
                floor = int(self.serverMessage.split("@")[1])
                floor = floor if floor > 0 else 0
                if not self.elevators.outside_up_queue.count(floor) and not self.elevators.elevator_execute_trace_queue[0][1].count(floor) and not self.elevators.elevator_execute_trace_queue[1][1].count(floor):
                    button = self.elevators.button_up[floor]
                    self.elevators.outside_up_queue.append(floor)
                    self.elevators.outside_up_queue.sort()
                    button.setStyleSheet("QPushButton{border-image: url(./res/up_pressed.png);}")
                    button.setEnabled(False)  
            elif "call_down" in self.serverMessage:
                floor = int(self.serverMessage.split("@")[1])
                if not self.elevators.outside_down_queue.count(floor) and not self.elevators.elevator_execute_trace_queue[0][2].count(floor) and not self.elevators.elevator_execute_trace_queue[1][2].count(floor):
                    button = self.elevators.button_down[floor - 1]
                    self.elevators.outside_down_queue.append(floor)
                    self.elevators.outside_down_queue.sort()
                    button.setStyleSheet("QPushButton{border-image: url(./res/down_pressed.png);}")
                    button.setEnabled(False)
            elif "select_floor" in self.serverMessage:
                elevator = int(self.serverMessage.split("#")[1])
                floor = int(self.serverMessage.split("@")[1].split("#")[0])
                floor = floor if floor > 0 else 0
                button = self.elevators.button_floor[elevator - 1][floor]
                if self.elevators.button_floor[elevator - 1][floor].objectName().split('_')[-1][:-1] != "clciked":
                    self.elevators.inside_queue[elevator - 1].append(floor)
                    self.elevators.inside_queue[elevator - 1].sort()
                    button.setStyleSheet("QPushButton{border-image: url(./res/" + str(floor) + "F_pressed.png);}")
                    button.setObjectName("button_floor_#" + str(1+elevator) + "_" + str(floor) + "F_clciked")
            elif "open_door" in self.serverMessage:
                elevator = int(self.serverMessage.split("#")[1])
                if (self.elevators.elevator_state[elevator - 1] == IDLE and self.elevators.elevator_door[elevator - 1] == PAUSE) or (self.elevators.elevator_door[elevator - 1] == CLOSE):
                    self.elevators.animation_open(elevator - 1, int(self.elevators.current_floor[elevator - 1]))
                self.messageUnprocessed = True
            elif "close_door" in self.serverMessage:
                elevator = int(self.serverMessage.split("#")[1])
                if (self.elevators.elevator_door[elevator - 1] == OPEN) or (self.elevators.elevator_door[elevator - 1] == HOLD):
                    self.elevators.animation_close(elevator - 1, int(self.elevators.current_floor[elevator - 1]))
                self.messageUnprocessed = True
            elif "reset" in self.serverMessage:
                self.elevators.elevator_state = [IDLE, IDLE]
                self.elevators.current_floor = [1, 1]
                self.elevators.elevator_door = [PAUSE, PAUSE]
                self.elevators.elevator_execute_queue = [[], []]
                self.elevators.elevator_execute_trace_queue = [[[],[],[]], [[],[],[]]]
                self.elevators.inside_queue = [[], []]
                self.elevators.outside_up_queue = []
                self.elevators.outside_down_queue = []
                
                for i in range(len(self.elevators.elevator_car)):
                    self.elevators.elevator_car[i].setGeometry(QRect(elevator_car_position[i][0], elevator_car_position[i][1], 130, 160))
                
                for i in range(len(self.elevators.elevator_outside_door_left)):
                    for j in range(len(self.elevators.elevator_outside_door_left[i])):
                        self.elevators.elevator_outside_door_left[i][j].setGeometry(QRect(elevator_outside_position[i][j][0], elevator_outside_position[i][j][1], 64, 160))
                        self.elevators.elevator_outside_door_right[i][j].setGeometry(QRect(elevator_outside_position[i][j][0]+66, elevator_outside_position[i][j][1], 64, 160))
                        
                for i in range(len(self.elevators.lcd_outside)):
                    for j in range(len(self.elevators.lcd_outside[i])):
                        self.elevators.lcd_outside[i][j].setProperty("value", self.elevators.current_floor[i] if self.elevators.current_floor[i] > 0 else -1)
                    
                for i in range(len(self.elevators.state_outside)):
                    for j in range(len(self.elevators.state_outside[i])):
                        self.elevators.state_outside[i][j].setStyleSheet("QGraphicsView{border-image: url(./res/state.png);}")
                
                for i in range(len(self.elevators.button_up)):
                    self.elevators.button_up[i].setStyleSheet("QPushButton{border-image: url(./res/up.png);}"
                                                            "QPushButton:hover{border-image: url(./res/up_hover.png);}"
                                                            "QPushButton:pressed{border-image: url(./res/up_pressed.png);}")
                    self.elevators.button_up[i].setEnabled(True)
                    
                for i in range(len(self.elevators.button_down)):
                    self.elevators.button_down[i].setStyleSheet("QPushButton{border-image: url(./res/down.png);}"
                                                            "QPushButton:hover{border-image: url(./res/down_hover.png);}"
                                                            "QPushButton:pressed{border-image: url(./res/down_pressed.png);}")
                    self.elevators.button_down[i].setEnabled(True)
                    
                for i in range(len(self.elevators.elevator_inside_door_left)):
                    self.elevators.elevator_inside_door_left[i].setGeometry(QRect(elevator_inside_position[i][0], elevator_inside_position[i][1], 128, 320))
                    self.elevators.elevator_inside_door_right[i].setGeometry(QRect(elevator_inside_position[i][0]+132, elevator_inside_position[i][1], 128, 320))
                    
                for i in range(len(self.elevators.lcd_inside)):
                    self.elevators.lcd_inside[i].setProperty("value", self.elevators.current_floor[i] if self.elevators.current_floor[i] > 0 else -1)
                    
                for i in range(len(self.elevators.state_inside)):
                    self.elevators.state_inside[i].setStyleSheet("QGraphicsView{border-image: url(./res/state.png);}")
                    
                for i in range(len(self.elevators.button_emergency)):
                    self.elevators.button_emergency[i].setStyleSheet("QPushButton{border-image: url(./res/emergency.png);}"
                                                            "QPushButton:hover{border-image: url(./res/emergency_hover.png);}"
                                                            "QPushButton:pressed{border-image: url(./res/emergency_pressed.png);}")
                    self.elevators.button_emergency[i].setEnabled(True)
                    
                for i in range(len(self.elevators.button_floor)):
                    for j in range(len(self.elevators.button_floor[i])):
                        self.elevators.button_floor[i][j].setStyleSheet("QPushButton{border-image: url(./res/" + str(j) + "F.png);}"
                                                            "QPushButton:hover{border-image: url(./res/" + str(j) + "F_hover.png);}"
                                                            "QPushButton:pressed{border-image: url(./res/" + str(j) + "F_pressed.png);}")
                        self.elevators.button_floor[i][j].setEnabled(True)
                    
                for i in range(len(self.elevators.button_open)):
                    self.elevators.button_open[i].setStyleSheet("QPushButton{border-image: url(./res/open.png);}"
                                                            "QPushButton:hover{border-image: url(./res/open_hover.png);}"
                                                            "QPushButton:pressed{border-image: url(./res/open_pressed.png);}")
                    self.elevators.button_open[i].setEnabled(True)
                    
                for i in range(len(self.elevators.button_close)):
                    self.elevators.button_close[i].setStyleSheet("QPushButton{border-image: url(./res/close.png);}"
                                                            "QPushButton:hover{border-image: url(./res/close_hover.png);}"
                                                            "QPushButton:pressed{border-image: url(./res/close_pressed.png);}")
                    self.elevators.button_close[i].setEnabled(True)