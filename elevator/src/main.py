import sys
from PyQt5.QtWidgets import QMainWindow, QApplication 
from PyQt5.QtGui import QIcon

from GUI import *
from Dispatcher import *
from Porter import *


class mywindow(QMainWindow, GUI):
    def __init__(self, elevators:Elevators):
        super().__init__(elevators)
        self.setup_ui(self)
        self.setWindowTitle('Elevator')
        self.setWindowIcon(QIcon('./res/elevator.ico'))
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    elevators = Elevators()
    porter = Porter(elevators)
    dispatcher = Dispatcher(porter)

    window = mywindow(elevators)
    window.show()
    
    sys.exit(app.exec())