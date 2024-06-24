from pyautogui import mouseDown, mouseUp, leftClick, doubleClick, moveTo, size
import time


class MouseBehaviour:
    def __init__(self) -> None:
        self.time_start = None
        self.last_contact = None
        self.is_dragging = False
        self.distance_threshold = 0.045
        self.drag_time_threshold = 0.6
        self.double_click_time_threshold = 0.8
        
        self.cursor = None
        self.center = (.75, .75)
        
        self.swidth, self.sheight = size()
        
    def _euc(self, v1, v2):
        return pow(
            pow(v1[0] - v2[0], 2) + pow(v1[1] - v2[1], 2) + pow(v1[2] - v2[2], 2),
            0.5
        )
    
    def detect(self, cursor, index, thumb, mulx, muly):
        self.cursor = cursor
        distance = self._euc(index, thumb)
        
        if distance <= self.distance_threshold:
            if self.time_start is None:
                if self.last_contact is not None and time.time() - self.last_contact < self.double_click_time_threshold:
                    doubleClick(_pause=False)
                    self.time_start = None
                else:
                    self.time_start = time.time()
                    leftClick(_pause=False)
            elif time.time() - self.time_start >= self.drag_time_threshold:
                self.is_dragging = True
                mouseDown(_pause=False)
        else:
            if self.is_dragging:
                mouseUp(_pause=False)
                self.is_dragging = False
                self.last_contact = None
                self.time_start = None
            else:
                self.last_contact = self.time_start
                self.time_start = None                
            
        moveTo(
            self.swidth * (0.5 - ((self.center[0] - cursor[0]) * mulx)), 
            self.sheight * (0.5 - ((self.center[1] - cursor[1]) * muly)), 
            _pause=False
        )
        
