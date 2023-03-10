### Imports ###
import os
os.environ['KIVY_NO_CONSOLELOG'] = '1'

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, ReferenceListProperty
from kivy.core.window import Window
from kivy.clock import Clock

from grid_analyzer import GridAnalyzer

from networktables import NetworkTables
### Imports ###



### Constants ###
NODE_X_OFFSET = 0.275
NODE_Y_OFFSET = 0.10125

LOCALHOST = True

IP = '127.0.0.1' if LOCALHOST else '10.87.36.2'
### Constants ###

# 
# 
### Globals ###
cur_row = 0
cur_col = 0

selected = [0, 0]
best = [0, 0]

smart_dashboard = None
grid_analyzer = GridAnalyzer()
### Globals ###



### Field ###
class Field(FloatLayout):
    pass

class Background(Image):
    offset = ListProperty()
    magnification = NumericProperty(0)

class Bounds(RelativeLayout):
    grid = ObjectProperty(None)
### Field ###



### Grid ###
class Grid(RelativeLayout):
    def update_hat(self, _a, _b, _c, value):
        global selected

        desired = selected

        if value == (-1, 0):
            desired[0] = desired[0] + 1
        elif value == (1, 0):
            desired[0] = desired[0] - 1

        if value == (0, -1):
            desired[1] = desired[1] - 1
        elif value == (0, 1):
            desired[1] = desired[1] + 1

        selected[0] = 0 if desired[0] < 0 else (2 if desired[0] > 2 else desired[0])
        selected[1] = 0 if desired[1] < 0 else (8 if desired[1] > 8 else desired[1])

    def update_button(self, _a, _b, value):
        global grid_analyzer

        if value == 0:
            for child in self.children:
                if [child.row, child.col] == selected:
                    child.set_element(True)

        if value == 1:
            for child in self.children:
                if [child.row, child.col] == selected:
                    child.set_element(None)

        state = [
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False]
        ]

        for child in self.children:
            state[child.row][child.col] = child.has_element

        grid_analyzer.update_state(state)

    def update_selected(self, *largs):
        global selected
        global best
        global grid_analyzer
        global smart_dashboard

        for child in self.children:
            if [child.row, child.col] != selected:
                child.unselect()
            else:
                child.select()

        best = grid_analyzer.get_best_node()

        if smart_dashboard:
            smart_dashboard.putNumber("TargetRow", best[0])
            smart_dashboard.putNumber("TargetCol", best[1])

### Grid ###



### Node ###
class Node(Widget):
    row = NumericProperty(0)
    col = NumericProperty(0)

    offset_x = NumericProperty(0)
    offset_y = NumericProperty(0)

    r = NumericProperty(0)
    g = NumericProperty(0)
    b = NumericProperty(0)
    a = NumericProperty(0)

    selected = False
    has_element = False

    def __init__(self, **kwargs):
        global cur_row
        global cur_col

        super(Node, self).__init__(**kwargs)

        self.row = cur_row
        self.col = cur_col

        self.offset_x = NODE_X_OFFSET * self.row
        self.offset_y = NODE_Y_OFFSET * self.col

        cur_col += 1

        if cur_col == 9:
            cur_row += 1
            cur_col = 0

        self.r = 1
        self.g = 0
        self.b = 0
        self.a = 0.25

    def select(self):
        self.selected = True

        self.update_color()
        
    def unselect(self):
        self.selected = False

        self.update_color()

    def set_element(self, has_element):
        self.has_element = has_element

        self.update_color()

    def update_color(self):
        if self.selected:
            self.r, self.g, self.b, self.a = (0, 1, 0, 0.5)
            return
        elif not self.has_element:
            self.r, self.g, self.b, self.a = (1, 0, 0, 0.5)
            return

        if self.has_element:
            if self.col == 1 or self.col == 4 or self.col == 7:
                self.r, self.g, self.b, self.a = (
                    156 / 255,
                    69 / 255,
                    255 / 255,
                    1.0
                )
                return
            else:
                self.r, self.g, self.b, self.a = (
                    255 / 255,
                    168 / 255,
                    82 / 255,
                    1.0
                )
                return

### Node ### 



### App ###
class Field4d(App):
    def build(self):
        global smart_dashboard

        field = Field()

        field.grid.update_selected()
        
        Window.bind(on_joy_hat=field.grid.update_hat)
        Window.bind(on_joy_button_down=field.grid.update_button)

        Clock.schedule_interval(field.grid.update_selected, 0.25)
        Clock.schedule_interval(self.connect, 1.0)

        return field

    def connect(self, *largs):
        global smart_dashboard

        if smart_dashboard:
            return

        NetworkTables.initialize(server=IP)
        smart_dashboard = NetworkTables.getTable('SmartDashboard')

        print('[SmartDashboard] Connected!')
### App ###



### Main ###
if __name__ == '__main__':
    Field4d().run()
### Main ###