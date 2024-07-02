from PyQt5.QtCore import QTimer, QPropertyAnimation, QRect

from Elevators import *
from Porter import *


UPDATE_INTERVAL = 1000


class Dispatcher:
    def __init__(self, porter: Porter):
        self.porter = porter
        self.elevators = self.porter.elevators
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(UPDATE_INTERVAL)
        
    def dispatch(self):
        for i in range(2):
            if self.elevators.elevator_state[i] == FAULT:
                continue
            
            # if self.elevators.elevator_door[i] != PAUSE:
            #     if self.elevators.inside_queue[i].count(self.elevators.current_floor[i]):
            #         self.elevators.inside_queue[i].remove(self.elevators.current_floor[i])
            #         if not self.elevators.elevator_execute_queue[i].count(self.elevators.current_floor[i]):
            #             self.elevators.elevator_execute_queue[i].append(self.elevators.current_floor[i])
            #             self.elevators.elevator_execute_queue[i].sort()
            #         if not self.elevators.elevator_execute_trace_queue[i][0].count(self.elevators.current_floor[i]):
            #             self.elevators.elevator_execute_trace_queue[i][0].append(self.elevators.current_floor[i])
            #             self.elevators.elevator_execute_trace_queue[i][0].sort()
            #     continue

            choice = 0
            while choice < len(self.elevators.inside_queue[i]):
                if self.elevators.elevator_state[i] == IDLE:
                    if self.elevators.inside_queue[i][choice] > self.elevators.current_floor[i]:
                        self.elevators.elevator_state[i] = UP
                        if not self.elevators.elevator_execute_queue[i].count(self.elevators.inside_queue[i][choice]):
                            self.elevators.elevator_execute_queue[i].append(self.elevators.inside_queue[i][choice])
                            self.elevators.elevator_execute_queue[i].sort()
                        if not self.elevators.elevator_execute_trace_queue[i][0].count(self.elevators.inside_queue[i][choice]):
                            self.elevators.elevator_execute_trace_queue[i][0].append(self.elevators.inside_queue[i][choice])
                            self.elevators.elevator_execute_trace_queue[i][0].sort()
                        self.elevators.inside_queue[i].pop(choice)
                    elif self.elevators.inside_queue[i][choice] < self.elevators.current_floor[i]:
                        self.elevators.elevator_state[i] = DOWN
                        if not self.elevators.elevator_execute_queue[i].count(self.elevators.inside_queue[i][choice]):
                            self.elevators.elevator_execute_queue[i].append(self.elevators.inside_queue[i][choice])
                            self.elevators.elevator_execute_queue[i].sort()
                        if not self.elevators.elevator_execute_trace_queue[i][0].count(self.elevators.inside_queue[i][choice]):
                            self.elevators.elevator_execute_trace_queue[i][0].append(self.elevators.inside_queue[i][choice])
                            self.elevators.elevator_execute_trace_queue[i][0].sort()
                        self.elevators.inside_queue[i].pop(choice)
                    else:
                        if not self.elevators.elevator_execute_queue[i].count(self.elevators.inside_queue[i][choice]):
                            self.elevators.elevator_execute_queue[i].append(self.elevators.inside_queue[i][choice])
                            self.elevators.elevator_execute_queue[i].sort()
                        if not self.elevators.elevator_execute_trace_queue[i][0].count(self.elevators.inside_queue[i][choice]):
                            self.elevators.elevator_execute_trace_queue[i][0].append(self.elevators.inside_queue[i][choice])
                            self.elevators.elevator_execute_trace_queue[i][0].sort()
                        self.elevators.inside_queue[i].pop(choice)
                elif self.elevators.elevator_state[i] == UP:
                    if self.elevators.inside_queue[i][choice] > self.elevators.current_floor[i]:
                        if not self.elevators.elevator_execute_queue[i].count(self.elevators.inside_queue[i][choice]):
                            self.elevators.elevator_execute_queue[i].append(self.elevators.inside_queue[i][choice])
                            self.elevators.elevator_execute_queue[i].sort()
                        if not self.elevators.elevator_execute_trace_queue[i][0].count(self.elevators.inside_queue[i][choice]):
                            self.elevators.elevator_execute_trace_queue[i][0].append(self.elevators.inside_queue[i][choice])
                            self.elevators.elevator_execute_trace_queue[i][0].sort()
                        self.elevators.inside_queue[i].pop(choice)
                    else:
                        choice += 1
                elif self.elevators.elevator_state[i] == DOWN:
                    if self.elevators.inside_queue[i][choice] < self.elevators.current_floor[i]:
                        if not self.elevators.elevator_execute_queue[i].count(self.elevators.inside_queue[i][choice]):
                            self.elevators.elevator_execute_queue[i].append(self.elevators.inside_queue[i][choice])
                            self.elevators.elevator_execute_queue[i].sort()
                        if not self.elevators.elevator_execute_trace_queue[i][0].count(self.elevators.inside_queue[i][choice]):
                            self.elevators.elevator_execute_trace_queue[i][0].append(self.elevators.inside_queue[i][choice])
                            self.elevators.elevator_execute_trace_queue[i][0].sort()
                        self.elevators.inside_queue[i].pop(choice)
                    else:
                        choice += 1
                elif self.elevators.elevator_state[i] == UP_DOWN:
                    if self.elevators.inside_queue[i][choice] > self.elevators.current_floor[i] and self.elevators.inside_queue[i][choice] <= max(self.elevators.elevator_execute_queue[i]):
                        if not self.elevators.elevator_execute_queue[i].count(self.elevators.inside_queue[i][choice]):
                            self.elevators.elevator_execute_queue[i].append(self.elevators.inside_queue[i][choice])
                            self.elevators.elevator_execute_queue[i].sort()
                        if not self.elevators.elevator_execute_trace_queue[i][0].count(self.elevators.inside_queue[i][choice]):
                            self.elevators.elevator_execute_trace_queue[i][0].append(self.elevators.inside_queue[i][choice])
                            self.elevators.elevator_execute_trace_queue[i][0].sort()
                        self.elevators.inside_queue[i].pop(choice)
                    else:
                        choice += 1
                elif self.elevators.elevator_state[i] == DOWN_UP:
                    if self.elevators.inside_queue[i][choice] < self.elevators.current_floor[i] and self.elevators.inside_queue[i][choice] >= min(self.elevators.elevator_execute_queue[i]):
                        if not self.elevators.elevator_execute_queue[i].count(self.elevators.inside_queue[i][choice]):
                            self.elevators.elevator_execute_queue[i].append(self.elevators.inside_queue[i][choice])
                            self.elevators.elevator_execute_queue[i].sort()
                        if not self.elevators.elevator_execute_trace_queue[i][0].count(self.elevators.inside_queue[i][choice]):
                            self.elevators.elevator_execute_trace_queue[i][0].append(self.elevators.inside_queue[i][choice])
                            self.elevators.elevator_execute_trace_queue[i][0].sort()
                        self.elevators.inside_queue[i].pop(choice)
                    else:
                        choice += 1
                else:
                    print("Error: elevator state is not valid")
                    exit(1)
                    
        i = 0
        while i < len(self.elevators.outside_up_queue):
            if self.elevators.elevator_state[0] not in [IDLE, UP] and self.elevators.elevator_state[1] not in [IDLE, UP]:
                break
            elif self.elevators.elevator_state[0] not in [IDLE, UP] or self.elevators.elevator_state[1] not in [IDLE, UP]:
                choice = 0 if self.elevators.elevator_state[0] in [IDLE, UP] else 1
                if self.elevators.elevator_state[choice] == UP:
                    if self.elevators.outside_up_queue[i] > self.elevators.current_floor[choice]:
                        if not self.elevators.elevator_execute_queue[choice].count(self.elevators.outside_up_queue[i]):
                            self.elevators.elevator_execute_queue[choice].append(self.elevators.outside_up_queue[i])
                            self.elevators.elevator_execute_queue[choice].sort()
                        if not self.elevators.elevator_execute_trace_queue[choice][1].count(self.elevators.outside_up_queue[i]):
                            self.elevators.elevator_execute_trace_queue[choice][1].append(self.elevators.outside_up_queue[i])
                            self.elevators.elevator_execute_trace_queue[choice][1].sort()
                        self.elevators.outside_up_queue.pop(i)
                    else:
                        i += 1
                else:
                    if self.elevators.outside_up_queue[i] >= self.elevators.current_floor[choice]:
                        self.elevators.elevator_state[choice] = UP
                        if not self.elevators.elevator_execute_queue[choice].count(self.elevators.outside_up_queue[i]):
                            self.elevators.elevator_execute_queue[choice].append(self.elevators.outside_up_queue[i])
                            self.elevators.elevator_execute_queue[choice].sort()
                        if not self.elevators.elevator_execute_trace_queue[choice][1].count(self.elevators.outside_up_queue[i]):
                            self.elevators.elevator_execute_trace_queue[choice][1].append(self.elevators.outside_up_queue[i])
                            self.elevators.elevator_execute_trace_queue[choice][1].sort()
                        self.elevators.outside_up_queue.pop(i)
                    else:
                        self.elevators.elevator_state[choice] = DOWN_UP
                        if not self.elevators.elevator_execute_queue[choice].count(self.elevators.outside_up_queue[i]):
                            self.elevators.elevator_execute_queue[choice].append(self.elevators.outside_up_queue[i])
                            self.elevators.elevator_execute_queue[choice].sort()
                        if not self.elevators.elevator_execute_trace_queue[choice][1].count(self.elevators.outside_up_queue[i]):
                            self.elevators.elevator_execute_trace_queue[choice][1].append(self.elevators.outside_up_queue[i])
                            self.elevators.elevator_execute_trace_queue[choice][1].sort()
                        self.elevators.outside_up_queue.pop(i)
            else:
                choice = -1
                if self.elevators.elevator_state[0] == UP and self.elevators.elevator_state[1] == UP:
                    if self.elevators.current_floor[0] >= self.elevators.outside_up_queue[i] and self.elevators.current_floor[1] >= self.elevators.outside_up_queue[i]:
                        choice = -1
                    elif self.elevators.current_floor[0] < self.elevators.outside_up_queue[i] and self.elevators.current_floor[1] < self.elevators.outside_up_queue[i]:
                        choice = 0 if abs(self.elevators.current_floor[0] - self.elevators.outside_up_queue[i]) < abs(self.elevators.current_floor[1] - self.elevators.outside_up_queue[i]) else 1
                    else:
                        choice = 0 if self.elevators.current_floor[0] < self.elevators.outside_up_queue[i] else 1
                elif self.elevators.elevator_state[0] == UP:
                    if self.elevators.current_floor[0] >= self.elevators.outside_up_queue[i]:
                        choice = 1
                    else:
                        choice = 0 if abs(self.elevators.current_floor[0] - self.elevators.outside_up_queue[i]) < abs(self.elevators.current_floor[1] - self.elevators.outside_up_queue[i]) else 1
                elif self.elevators.elevator_state[1] == UP:
                    if self.elevators.current_floor[1] >= self.elevators.outside_up_queue[i]:
                        choice = 0
                    else:
                        choice = 0 if abs(self.elevators.current_floor[0] - self.elevators.outside_up_queue[i]) < abs(self.elevators.current_floor[1] - self.elevators.outside_up_queue[i]) else 1
                else:
                    choice = 0 if abs(self.elevators.current_floor[0] - self.elevators.outside_up_queue[i]) < abs(self.elevators.current_floor[1] - self.elevators.outside_up_queue[i]) else 1
                
                if choice == -1:
                    i += 1
                    continue
                else:
                    if self.elevators.elevator_state[choice] == IDLE:
                        self.elevators.elevator_state[choice] = UP if self.elevators.current_floor[choice] <= self.elevators.outside_up_queue[i] else DOWN_UP
                    if not self.elevators.elevator_execute_queue[choice].count(self.elevators.outside_up_queue[i]):
                        self.elevators.elevator_execute_queue[choice].append(self.elevators.outside_up_queue[i])
                        self.elevators.elevator_execute_queue[choice].sort()
                    if not self.elevators.elevator_execute_trace_queue[choice][1].count(self.elevators.outside_up_queue[i]):
                        self.elevators.elevator_execute_trace_queue[choice][1].append(self.elevators.outside_up_queue[i])
                        self.elevators.elevator_execute_trace_queue[choice][1].sort()
                    self.elevators.outside_up_queue.pop(i)
                    
        i = 0
        while i < len(self.elevators.outside_down_queue):
            if self.elevators.elevator_state[0] not in [IDLE, DOWN] and self.elevators.elevator_state[1] not in [IDLE, DOWN]:
                break
            elif self.elevators.elevator_state[0] not in [IDLE, DOWN] or self.elevators.elevator_state[1] not in [IDLE, DOWN]:
                choice = 0 if self.elevators.elevator_state[0] in [IDLE, DOWN] else 1
                if self.elevators.elevator_state[choice] == DOWN:
                    if self.elevators.outside_down_queue[i] < self.elevators.current_floor[choice]:
                        if not self.elevators.elevator_execute_queue[choice].count(self.elevators.outside_down_queue[i]):
                            self.elevators.elevator_execute_queue[choice].append(self.elevators.outside_down_queue[i])
                            self.elevators.elevator_execute_queue[choice].sort()
                        if not self.elevators.elevator_execute_trace_queue[choice][2].count(self.elevators.outside_down_queue[i]):
                            self.elevators.elevator_execute_trace_queue[choice][2].append(self.elevators.outside_down_queue[i])
                            self.elevators.elevator_execute_trace_queue[choice][2].sort()
                        self.elevators.outside_down_queue.pop(i)
                    else:
                        i += 1
                else:
                    if self.elevators.outside_down_queue[i] <= self.elevators.current_floor[choice]:
                        self.elevators.elevator_state[choice] = DOWN
                        if not self.elevators.elevator_execute_queue[choice].count(self.elevators.outside_down_queue[i]):
                            self.elevators.elevator_execute_queue[choice].append(self.elevators.outside_down_queue[i])
                            self.elevators.elevator_execute_queue[choice].sort()
                        if not self.elevators.elevator_execute_trace_queue[choice][2].count(self.elevators.outside_down_queue[i]):
                            self.elevators.elevator_execute_trace_queue[choice][2].append(self.elevators.outside_down_queue[i])
                            self.elevators.elevator_execute_trace_queue[choice][2].sort()
                        self.elevators.outside_down_queue.pop(i)
                    else:
                        self.elevators.elevator_state[choice] = UP_DOWN
                        if not self.elevators.elevator_execute_queue[choice].count(self.elevators.outside_down_queue[i]):
                            self.elevators.elevator_execute_queue[choice].append(self.elevators.outside_down_queue[i])
                            self.elevators.elevator_execute_queue[choice].sort()
                        if not self.elevators.elevator_execute_trace_queue[choice][2].count(self.elevators.outside_down_queue[i]):
                            self.elevators.elevator_execute_trace_queue[choice][2].append(self.elevators.outside_down_queue[i])
                            self.elevators.elevator_execute_trace_queue[choice][2].sort()
                        self.elevators.outside_down_queue.pop(i)
            else:
                choice = -1
                if self.elevators.elevator_state[0] == DOWN and self.elevators.elevator_state[1] == DOWN:
                    if self.elevators.current_floor[0] <= self.elevators.outside_down_queue[i] and self.elevators.current_floor[1] <= self.elevators.outside_down_queue[i]:
                        choice = -1
                    elif self.elevators.current_floor[0] > self.elevators.outside_down_queue[i] and self.elevators.current_floor[1] > self.elevators.outside_down_queue[i]:
                        choice = 0 if abs(self.elevators.current_floor[0] - self.elevators.outside_down_queue[i]) < abs(self.elevators.current_floor[1] - self.elevators.outside_down_queue[i]) else 1
                    else:
                        choice = 0 if self.elevators.current_floor[0] > self.elevators.outside_down_queue[i] else 1
                elif self.elevators.elevator_state[0] == DOWN:
                    if self.elevators.current_floor[0] <= self.elevators.outside_down_queue[i]:
                        choice = 1
                    else:
                        choice = 0 if abs(self.elevators.current_floor[0] - self.elevators.outside_down_queue[i]) < abs(self.elevators.current_floor[1] - self.elevators.outside_down_queue[i]) else 1
                elif self.elevators.elevator_state[1] == DOWN:
                    if self.elevators.current_floor[1] <= self.elevators.outside_down_queue[i]:
                        choice = 0
                    else:
                        choice = 0 if abs(self.elevators.current_floor[0] - self.elevators.outside_down_queue[i]) < abs(self.elevators.current_floor[1] - self.elevators.outside_down_queue[i]) else 1
                else:
                    choice = 0 if abs(self.elevators.current_floor[0] - self.elevators.outside_down_queue[i]) < abs(self.elevators.current_floor[1] - self.elevators.outside_down_queue[i]) else 1
                    
                if choice == -1:
                    i += 1
                    continue
                else:
                    if self.elevators.elevator_state[choice] == IDLE:
                        self.elevators.elevator_state[choice] = DOWN if self.elevators.current_floor[choice] >= self.elevators.outside_down_queue[i] else UP_DOWN
                    if not self.elevators.elevator_execute_queue[choice].count(self.elevators.outside_down_queue[i]):
                        self.elevators.elevator_execute_queue[choice].append(self.elevators.outside_down_queue[i])
                        self.elevators.elevator_execute_queue[choice].sort()
                    if not self.elevators.elevator_execute_trace_queue[choice][2].count(self.elevators.outside_down_queue[i]):
                        self.elevators.elevator_execute_trace_queue[choice][2].append(self.elevators.outside_down_queue[i])
                        self.elevators.elevator_execute_trace_queue[choice][2].sort()
                    self.elevators.outside_down_queue.pop(i)
                    
    def log(self):
        print("--------------------")
        print("Outside up queue: " + str(self.elevators.outside_up_queue))
        print("Outside down queue: " + str(self.elevators.outside_down_queue))
        print()
        for i in range(2):
            print("Elevator " + str(i+1) + ":")
            print("State: " + str(self.elevators.elevator_state[i]))
            print("Current floor: " + str(self.elevators.current_floor[i]))
            print("Door state: " + str(self.elevators.elevator_door[i]))
            print("Execute queue: " + str(self.elevators.elevator_execute_queue[i]))
            print("Execute trace queue: " + str(self.elevators.elevator_execute_trace_queue[i]))
            print("Inside queue: " + str(self.elevators.inside_queue[i]))
            print()    
    
    def update(self):
        # self.log()
        
        self.dispatch()
        
        for i in range(2):
            
            if self.elevators.elevator_state[i] == FAULT:
                continue
                    
            if self.elevators.elevator_state[i] == IDLE:
                for j in range(4):
                    self.elevators.state_outside[i][j].setStyleSheet("QGraphicsView{border-image: url(./res/state.png)}")
                self.elevators.state_inside[i].setStyleSheet("QGraphicsView{border-image: url(./res/state.png)}")
            elif self.elevators.elevator_state[i] in [UP, UP_DOWN]:
                for j in range(4):
                    self.elevators.state_outside[i][j].setStyleSheet("QGraphicsView{border-image: url(./res/state_up.png)}")
                self.elevators.state_inside[i].setStyleSheet("QGraphicsView{border-image: url(./res/state_up.png)}")
            elif self.elevators.elevator_state[i] in [DOWN, DOWN_UP]:
                for j in range(4):
                    self.elevators.state_outside[i][j].setStyleSheet("QGraphicsView{border-image: url(./res/state_down.png)}")
                self.elevators.state_inside[i].setStyleSheet("QGraphicsView{border-image: url(./res/state_down.png)}")

            if self.elevators.current_floor[i] % 1 == 0:    
                for j in range(4):
                    self.elevators.lcd_outside[i][j].setProperty("value", int(self.elevators.current_floor[i]) if self.elevators.current_floor[i] > 0 else -1)
                self.elevators.lcd_inside[i].setProperty("value", int(self.elevators.current_floor[i]) if self.elevators.current_floor[i] > 0 else -1)
                    
            if self.elevators.elevator_execute_queue[i].count(self.elevators.current_floor[i]) and self.elevators.elevator_door[i] not in [OPEN, HOLD]:
                self.elevators.animation_open(i, int(self.elevators.current_floor[i]))
                self.porter.zmqThread.sendMsg(("up" if self.elevators.elevator_state[i] in [UP, DOWN_UP] else "down") + "_floor_arrived@" 
                                                + str(int(self.elevators.current_floor[i]) if self.elevators.current_floor[i] > 0 else -1) 
                                                + "#" + str(1+i))
            elif self.elevators.elevator_door[i] == OPEN:
                self.elevators.button_open[i].setStyleSheet("QPushButton{border-image: url(./res/open.png);}"
                                                    "QPushButton:hover{border-image: url(./res/open_hover.png);}"
                                                    "QPushButton:pressed{border-image: url(./res/open_pressed.png);}")
                self.elevators.button_open[i].setEnabled(True)
                if self.elevators.elevator_execute_queue[i].count(int(self.elevators.current_floor[i])):
                    self.elevators.button_floor[i][int(self.elevators.current_floor[i])].setStyleSheet("QPushButton{border-image: url(./res/" + str(int(self.elevators.current_floor[i])) + "F.png);}"
                                                                                               "QPushButton:hover{border-image: url(./res/" + str(int(self.elevators.current_floor[i])) + "F_hover.png);}"
                                                                                               "QPushButton:pressed{border-image: url(./res/" + str(int(self.elevators.current_floor[i])) + "F_pressed.png);}")
                    self.elevators.button_floor[i][int(self.elevators.current_floor[i])].setObjectName("button_floor_#" + str(1+i) + "_" + str(int(self.elevators.current_floor[i])) + "F")
                    if self.elevators.elevator_state[i] in [UP, DOWN_UP] and self.elevators.current_floor[i] < 3:
                        self.elevators.button_up[int(self.elevators.current_floor[i])].setStyleSheet("QPushButton{border-image: url(./res/up.png);}"
                                                                                                "QPushButton:hover{border-image: url(./res/up_hover.png);}"
                                                                                                "QPushButton:pressed{border-image: url(./res/up_pressed.png);}")
                        self.elevators.button_up[int(self.elevators.current_floor[i])].setEnabled(True)
                    elif self.elevators.elevator_state[i] in [DOWN, UP_DOWN] and self.elevators.current_floor[i] > 0:
                        self.elevators.button_down[int(self.elevators.current_floor[i] - 1)].setStyleSheet("QPushButton{border-image: url(./res/down.png);}"
                                                                                                    "QPushButton:hover{border-image: url(./res/down_hover.png);}"
                                                                                                    "QPushButton:pressed{border-image: url(./res/down_pressed.png);}")
                        self.elevators.button_down[int(self.elevators.current_floor[i] - 1)].setEnabled(True)
                if self.elevators.elevator_execute_queue[i].count(int(self.elevators.current_floor[i])):
                    self.elevators.elevator_execute_queue[i].remove(int(self.elevators.current_floor[i]))
                for j in range(3):
                    if self.elevators.elevator_execute_trace_queue[i][j].count(int(self.elevators.current_floor[i])):
                        self.elevators.elevator_execute_trace_queue[i][j].remove(int(self.elevators.current_floor[i]))
                self.elevators.elevator_door[i] = HOLD
                self.porter.zmqThread.sendMsg("door_opened#" + str(1+i))
            elif self.elevators.elevator_door[i] == HOLD:
                self.elevators.animation_close(i, int(self.elevators.current_floor[i]))
            elif self.elevators.elevator_door[i] == CLOSE:
                self.elevators.button_close[i].setStyleSheet("QPushButton{border-image: url(./res/close.png);}"
                                                  "QPushButton:hover{border-image: url(./res/close_hover.png);}"
                                                  "QPushButton:pressed{border-image: url(./res/close_pressed.png);}")
                self.elevators.button_close[i].setEnabled(True)
                self.porter.zmqThread.sendMsg("door_closed#" + str(1+i))
                self.elevators.elevator_door[i] = PAUSE
            elif self.elevators.elevator_door[i] == PAUSE:
                if self.elevators.elevator_state[i] == UP or self.elevators.elevator_state[i] == UP_DOWN:
                    if self.elevators.current_floor[i] % 1 == 0:
                        self.elevators.animation_up(i)
                    self.elevators.current_floor[i] += ELEVATOR_SPEED
                elif self.elevators.elevator_state[i] == DOWN or self.elevators.elevator_state[i] == DOWN_UP:
                    if self.elevators.current_floor[i] % 1 == 0:
                        self.elevators.animation_down(i)
                    self.elevators.current_floor[i] -= ELEVATOR_SPEED
                    
            if not self.elevators.elevator_execute_queue[i] and self.elevators.current_floor[i] % 1 == 0:
                if self.elevators.elevator_state[i] in [UP, DOWN]:
                    self.elevators.elevator_state[i] = IDLE
                elif self.elevators.elevator_state[i] == UP_DOWN:
                    self.elevators.elevator_state[i] = DOWN
                elif self.elevators.elevator_state[i] == DOWN_UP:
                    self.elevators.elevator_state[i] = UP
                for floor in self.elevators.inside_queue[i]:
                    button = self.elevators.button_floor[i][floor]
                    button.setStyleSheet("QPushButton{border-image: url(./res/" + str(floor) + "F.png);}"
                                 "QPushButton:hover{border-image: url(./res/" + str(floor) + "F_hover.png);}"
                                 "QPushButton:pressed{border-image: url(./res/" + str(floor) + "F_pressed.png);}")
                    button.setObjectName("button_floor_#" + str(i+1) + "_" + str(floor) + "F")
                self.elevators.inside_queue[i].clear()