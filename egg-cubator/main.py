from kivy.config import Config

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy_garden.graph import Graph, MeshLinePlot
from random import randint
from kivymd.toast import toast

KV = '''
MDScreen:
    md_bg_color: app.theme_cls.bg_normal

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Egg-cubator Monitor"
            elevation: 4
            pos_hint: {"top": 1}

        # SINGLE BOTTOM NAVIGATION BAR
        MDBottomNavigation:
            panel_color: "#f3f3f3"
            selected_color_background: "orange"
            text_color_active: "black"

            MDBottomNavigationItem:
                name: "nav_home"
                icon: "home"
                text: "Home"
                on_tab_press: app.switch_screen("nav_home")

                ScrollView:

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(8)
                        padding: dp(8)
                        adaptive_height: True
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}

                        # STATUS CARDS
                        MDBoxLayout:
                            orientation: "vertical"
                            adaptive_height: True
                            spacing: dp(8)
                            MDBoxLayout:
                                size_hint_y: None
                                height: dp(90)
                                spacing: dp(8)
                                MDCard:
                                    orientation: "vertical"
                                    md_bg_color: app.theme_cls.primary_color
                                    radius: [12]
                                    MDLabel:
                                        text: "Days"
                                        halign: "center"
                                        theme_text_color: "Custom"
                                        text_color: 1,1,1,0.9
                                    MDLabel:
                                        id: days_label
                                        text: "10"
                                        halign: "center"
                                        font_style: "H4"
                                        text_color: 1,1,1,1
                                        
                                MDCard:
                                    orientation: "vertical"
                                    md_bg_color: [0.5, 1, 0.3, 1]
                                    radius: [12]
                                    MDLabel:
                                        text: "No. of egg turns"
                                        halign: "center"
                                        theme_text_color: "Custom"
                                        text_color: 1,1,1,0.9
                                    MDLabel:
                                        id: turn_label
                                        text: "8"
                                        halign: "center"
                                        font_style: "H4"
                                        text_color: 1,1,1,1
                                        
                            MDBoxLayout:
                                size_hint_y: None
                                height: dp(90)
                                spacing: dp(8)
                                MDCard:
                                    orientation: "vertical"
                                    md_bg_color: [1, 0.4, 0.3, 1]
                                    radius: [12]
                                    MDLabel:
                                        text: "Temperature (°C)"
                                        halign: "center"
                                        theme_text_color: "Custom"
                                        text_color: 1,1,1,0.9
                                    MDLabel:
                                        id: temp_label
                                        text: "37.5"
                                        halign: "center"
                                        font_style: "H4"
                                        text_color: 1,1,1,1
    
                                MDCard:
                                    orientation: "vertical"
                                    md_bg_color: [0.2, 0.6, 1, 1]
                                    radius: [12]
                                    MDLabel:
                                        text: "Humidity (%)"
                                        halign: "center"
                                        theme_text_color: "Custom"
                                        text_color: 1,1,1,0.9
                                    MDLabel:
                                        id: hum_label
                                        text: "55"
                                        halign: "center"
                                        font_style: "H4"
                                        text_color: 1,1,1,1

                        # GRAPHS
                        MDCard:
                            orientation: "vertical"
                            radius: [12]
                            padding: dp(8)
                            spacing: dp(8)
                            adaptive_height: True
                            md_bg_color: [1, 0.4, 0.3, 1]
                            MDLabel:
                                text: "Temperature Graph"
                                halign: "center"
                                theme_text_color: "Primary"
                                bold: True
                            BoxLayout:
                                id: temp_graph_box
                                size_hint_y: None
                                height: dp(95)

                        MDCard:
                            orientation: "vertical"
                            radius: [12]
                            padding: dp(8)
                            spacing: dp(8)
                            adaptive_height: True
                            md_bg_color: [0.2, 0.6, 1, 1]
                            MDLabel:
                                text: "Humidity Graph"
                                halign: "center"
                                theme_text_color: "Primary"
                                bold: True
                            BoxLayout:
                                id: hum_graph_box
                                size_hint_y: None
                                height: dp(95)

            MDBottomNavigationItem:
                name: "nav_settings"
                icon: "cog"
                text: "Settings"
                on_tab_press: app.switch_screen("nav_settings")

                MDBoxLayout:
                    orientation: "vertical"
                    ScrollView:
                        do_scroll_x: False
                        size_hint_y: 1
                        MDBoxLayout:
                            orientation: "vertical"
                            padding: dp(8)
                            spacing: dp(8)
                            adaptive_size: True
                            width: self.parent.width
                            MDCard:
                                orientation: "horizontal"
                                radius: [12]
                                size_hint_y: None
                                height: dp(90)
                                padding: [8]
                                md_bg_color: "lightgrey"
                                MDBoxLayout:
                                    orientation: "vertical"
                                    adaptive_height: True
                                    MDLabel:
                                        text: "Set temperature & humidity" 
                                        font_size: 20
                                    MDLabel:
                                        id: stemp
                                        text: "Temperature: 37.5"
                                        font_size: 14
                                    MDLabel:
                                        id: shum
                                        text: "Humidity: 55"
                                        font_size: 14
                                MDIconButton:
                                    icon: "chevron-right"
                            
                            MDBoxLayout:
                                orientation: "vertical"
                                padding: [8]
                                spacing: dp(8)
                                adaptive_height: True
                                radius: [12]
                                md_bg_color: "lightgrey"
                                MDLabel:
                                    text: "Status"
                                    font_size: 24
                                MDCard:
                                    orientation: "horizontal"
                                    radius: [12]
                                    size_hint_y: None
                                    height: dp(45) 
                                    padding: [8]
                                    MDLabel:
                                        text: "Bulb"
                                        font_size: 20  
                                    MDRaisedButton:
                                        id: bulb
                                        text: "On"
                                        md_bg_color: "green"
                                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
    
    
                                MDCard:
                                    orientation: "horizontal"     
                                    radius: [12]
                                    size_hint_y: None
                                    height: dp(45) 
                                    padding: [8]
                                    MDLabel:
                                        text: "Fan"
                                        font_size: 20 
                                    MDRaisedButton:
                                        id: fan
                                        text: "Off"
                                        md_bg_color: "red"
                                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
    
                                MDCard:
                                    orientation: "horizontal"     
                                    radius: [12]
                                    size_hint_y: None
                                    height: dp(45) 
                                    padding: [8]
                                    MDLabel:
                                        text: "Humidifier"
                                        font_size: 20
                                    MDRaisedButton:
                                        id: hum
                                        text: "On"
                                        md_bg_color: "green"
                                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
    
                                MDCard:
                                    radius: [12]
                                    size_hint_y: None
                                    height: dp(45) 
                                    padding: [8]
                                    
                                    MDLabel:
                                        text: "Camera"
                                        font_size: 20
                                        
                                    MDRaisedButton:
                                        id: cam
                                        text: "Off"
                                        md_bg_color: "red"
                                        pos_hint: {"center_x": 0.5, "center_y": 0.5}


            MDBottomNavigationItem:
                name: "nav_camera"
                icon: "video"
                text: "Camera"
                on_tab_press: app.switch_screen("nav_camera")
'''


class EggCubatorApp(MDApp):
    def build(self):
        self.title = "Egg-cubator Mobile UI"
        self.theme_cls.primary_palette = "Orange"
        screen = Builder.load_string(KV)

        # Create temperature graph
        self.temp_graph = Graph(
            xlabel='Time (s)', ylabel='°C',
            x_ticks_minor=5, x_ticks_major=10, y_ticks_major=5,
            y_grid_label=True, x_grid_label=False,
            padding=5, x_grid=True, y_grid=False,
            xmin=0, xmax=30, ymin=30, ymax=45,
            size_hint=(1, 1)
        )
        self.temp_plot = MeshLinePlot(color=[1, 0.2, 0.2, 1])
        self.temp_graph.add_plot(self.temp_plot)
        screen.ids.temp_graph_box.add_widget(self.temp_graph)

        # Create humidity graph
        self.hum_graph = Graph(
            xlabel='Time (s)', ylabel='%',
            x_ticks_minor=5, x_ticks_major=10, y_ticks_major=10,
            y_grid_label=True, x_grid_label=False,
            padding=5, x_grid=True, y_grid=False,
            xmin=0, xmax=30, ymin=40, ymax=80,
            size_hint=(1, 1)
        )
        self.hum_plot = MeshLinePlot(color=[0.2, 0.6, 1, 1])
        self.hum_graph.add_plot(self.hum_plot)
        screen.ids.hum_graph_box.add_widget(self.hum_graph)

        # Sample data
        self.x_data = list(range(0, 31))
        self.temp_data = [37.5 for _ in self.x_data]
        self.hum_data = [55 for _ in self.x_data]
        self.temp_plot.points = list(zip(self.x_data, self.temp_data))
        self.hum_plot.points = list(zip(self.x_data, self.hum_data))

        # Auto update
        Clock.schedule_interval(self.update_data, 2)
        return screen

    def switch_screen(self, name):
        self.root.ids.current = name

    def update_data(self, *args):
        new_temp = 37 + randint(-3, 3) / 10.0
        new_hum = 55 + randint(-8, 8)
        self.temp_data.append(new_temp)
        self.hum_data.append(new_hum)

        self.temp_data = self.temp_data[-30:]
        self.hum_data = self.hum_data[-30:]

        self.temp_plot.points = list(zip(range(30), self.temp_data))
        self.hum_plot.points = list(zip(range(30), self.hum_data))

        self.root.ids.temp_label.text = f"{new_temp:.1f}"
        self.root.ids.hum_label.text = f"{new_hum:.0f}"

    def _toast(self):
        self.root.ids


if __name__ == "__main__":
    EggCubatorApp().run()
