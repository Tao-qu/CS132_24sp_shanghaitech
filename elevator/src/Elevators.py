from PyQt5.QtCore import QRect, QPropertyAnimation


IDLE = 0
UP = 1
DOWN = 2
UP_DOWN = 3
DOWN_UP = 4
FAULT = -1
PAUSE = 0
CLOSE = 1
OPEN = 2
HOLD = 3

ELEVATOR_SPEED = 0.5


elevator_car_position = [(210,590), (800,590)]
elevator_outside_position = [[(380,840), (380,590), (380,340), (380,90)], 
                             [(630,840), (630,590), (630,340), (630,90)]]
label_floor_position = [(510,790), (510,540), (510,290), (510,40)]
lcd_outside_position = [[(400,780), (400,530), (400,280), (400,30)], 
                         [(650,780), (650,530), (650,280), (650,30)]]
state_outside_position = [[(445,770), (445,520), (445,270), (445,20)],
                           [(695,770), (695,520), (695,270), (695,20)]]
button_up_position = [(550,875), (550,625), (550,375)]
button_down_position = [(550,675), (550,425), (550,175)]
elevator_inside_position = [(1150,590), (1150,90)]
label_elevator_position = [(1520,590), (1520,90)]
lcd_inside_position = [(1520,635), (1520,135)]
state_inside_position = [(1590,620), (1590,120)]
button_emergency_position = [(1520,705), (1520,205)]
button_floor_position = [[(1520, 815), (1520, 760), (1575, 760), (1630, 760)],
                         [(1520, 315), (1520, 260), (1575, 260), (1630, 260)]]
button_open_position = [(1520, 870), (1520, 370)]
button_close_position = [(1575, 870), (1575, 370)]


class Elevators:
    def __init__(self):
        self.elevator_car = []
        self.elevator_outside_background = [[],[]]
        self.elevator_outside_door_left = [[],[]]
        self.elevator_outside_door_right = [[],[]]
        self.label_floor = []
        self.lcd_outside = [[],[]]
        self.state_outside = [[],[]]
        self.button_up = []
        self.button_down = []
        self.elevator_inside_background = []
        self.elevator_inside_door_left = []
        self.elevator_inside_door_right = []
        self.label_elevator = []
        self.lcd_inside = []
        self.state_inside = []
        self.button_emergency = []
        self.button_floor = [[],[]]
        self.button_open = []
        self.button_close = []
        
        self.animation_elevator_car = []
        self.animation_outside_door_left = [[],[]]
        self.animation_outside_door_right = [[],[]]
        self.animation_inside_door_left = []
        self.animation_inside_door_right = []
        
        self.elevator_state = [IDLE, IDLE]
        self.current_floor = [1, 1]
        self.elevator_door = [PAUSE, PAUSE]
        self.elevator_execute_queue = [[], []]
        self.elevator_execute_trace_queue = [[[],[],[]], [[],[],[]]]
        self.inside_queue = [[], []]
        self.outside_up_queue = []
        self.outside_down_queue = []
        
    def animation_move_door(self, object, start, end, speed):
        distance = abs(start.width() - end.width())
        duration = int(distance / speed)

        animation = QPropertyAnimation(object, b"geometry")
        animation.setDuration(duration)
        animation.setStartValue(start)
        animation.setEndValue(end)
        animation.start()
        return animation
    
    def animation_move_car(self, object, start, end, speed):
        distance = abs(start.y() - end.y())
        duration = int(distance / speed)

        animation = QPropertyAnimation(object, b"geometry")
        animation.setDuration(duration)
        animation.setStartValue(start)
        animation.setEndValue(end)
        animation.start()
        return animation
    
    def animation_open(self, elevator, floor):
        self.button_close[elevator].setStyleSheet("QPushButton{border-image: url(./res/close.png);}"
                                                  "QPushButton:hover{border-image: url(./res/close_hover.png);}"
                                                  "QPushButton:pressed{border-image: url(./res/close_pressed.png);}")
        self.button_close[elevator].setEnabled(True)
        self.elevator_door[elevator] = OPEN
        self.button_open[elevator].setStyleSheet("QPushButton{border-image: url(./res/open_pressed.png);}")
        self.button_open[elevator].setEnabled(False)
        self.animation_outside_door_left[elevator][floor] = self.animation_move_door(self.elevator_outside_door_left[elevator][floor], 
                                                                                          self.elevator_outside_door_left[elevator][floor].geometry(), 
                                                                                          QRect(elevator_outside_position[elevator][floor][0], elevator_outside_position[elevator][floor][1], 0, 160), 0.064)
        self.animation_outside_door_right[elevator][floor] = self.animation_move_door(self.elevator_outside_door_right[elevator][floor], 
                                                                                           self.elevator_outside_door_right[elevator][floor].geometry(), 
                                                                                           QRect(elevator_outside_position[elevator][floor][0]+130, elevator_outside_position[elevator][floor][1], 0, 160), 0.064)
        self.animation_inside_door_left[elevator] = self.animation_move_door(self.elevator_inside_door_left[elevator],
                                                                                  self.elevator_inside_door_left[elevator].geometry(),
                                                                                  QRect(elevator_inside_position[elevator][0], elevator_inside_position[elevator][1], 0, 320), 0.128)
        self.animation_inside_door_right[elevator] = self.animation_move_door(self.elevator_inside_door_right[elevator],
                                                                                   self.elevator_inside_door_right[elevator].geometry(),
                                                                                   QRect(elevator_inside_position[elevator][0]+260, elevator_inside_position[elevator][1], 0, 320), 0.128)
        
    def animation_close(self, elevator, floor):
        self.button_open[elevator].setStyleSheet("QPushButton{border-image: url(./res/open.png);}"
                                                    "QPushButton:hover{border-image: url(./res/open_hover.png);}"
                                                    "QPushButton:pressed{border-image: url(./res/open_pressed.png);}")
        self.button_open[elevator].setEnabled(True)
        self.elevator_door[elevator] = CLOSE
        self.button_close[elevator].setStyleSheet("QPushButton{border-image: url(./res/close_pressed.png);}")
        self.button_close[elevator].setEnabled(False)
        self.animation_outside_door_left[elevator][floor] = self.animation_move_door(self.elevator_outside_door_left[elevator][floor], 
                                                                                          self.elevator_outside_door_left[elevator][floor].geometry(), 
                                                                                          QRect(elevator_outside_position[elevator][floor][0], elevator_outside_position[elevator][floor][1], 64, 160), 0.064)
        self.animation_outside_door_right[elevator][floor] = self.animation_move_door(self.elevator_outside_door_right[elevator][floor], 
                                                                                           self.elevator_outside_door_right[elevator][floor].geometry(), 
                                                                                           QRect(elevator_outside_position[elevator][floor][0]+66, elevator_outside_position[elevator][floor][1], 64, 160), 0.064)
        self.animation_inside_door_left[elevator] = self.animation_move_door(self.elevator_inside_door_left[elevator],
                                                                                  self.elevator_inside_door_left[elevator].geometry(),
                                                                                  QRect(elevator_inside_position[elevator][0], elevator_inside_position[elevator][1], 128, 320), 0.128)
        self.animation_inside_door_right[elevator] = self.animation_move_door(self.elevator_inside_door_right[elevator],
                                                                                   self.elevator_inside_door_right[elevator].geometry(),
                                                                                   QRect(elevator_inside_position[elevator][0]+132, elevator_inside_position[elevator][1], 128, 320), 0.128)
    
    def animation_up(self, elevator):
        self.animation_elevator_car[elevator] = self.animation_move_car(self.elevator_car[elevator], 
                                                                             self.elevator_car[elevator].geometry(), 
                                                                             QRect(self.elevator_car[elevator].geometry().x(), elevator_outside_position[elevator][int(self.current_floor[elevator])+1][1], 130, 160), 250*ELEVATOR_SPEED/1000)
        
    def animation_down(self, elevator):
        self.animation_elevator_car[elevator] = self.animation_move_car(self.elevator_car[elevator], 
                                                                             self.elevator_car[elevator].geometry(), 
                                                                             QRect(self.elevator_car[elevator].geometry().x(), elevator_outside_position[elevator][int(self.current_floor[elevator])-1][1], 130, 160), 250*ELEVATOR_SPEED/1000)
                