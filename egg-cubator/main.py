from kivy.config import Config

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

import cv2
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.slider import MDSlider
from kivy_garden.graph import Graph, MeshLinePlot
from random import randint
from kivymd.toast import toast
import threading
from datetime import timedelta

KV = '''
MDScreen:
    md_bg_color: app.theme_cls.bg_normal
    
    MDScreenManager:
        id: screen_manager
        MDScreen:

            MDBoxLayout:
                orientation: "vertical"
                size_hint: (1, 1)
            
                MDBoxLayout:
                    size_hint_y: None
                    height: dp(420)
                    Image:
                        source: 'source/chick.png'
                        fit_mode: 'scale-down'
                        keep_data: True
            
                FloatLayout:
                    MDLabel:
                        text: "EGG-CUBATOR"
                        font_style: "H3"
                        pos_hint: {"center_x": 0.5, "top": 1}
                        halign: "center"
                        valign: "top"
                        size_hint_y: None
                        height: dp(64)
            
                    MDLabel:
                        text: "You must connect first to a device!"
                        halign: "center"
                        size_hint_y: None
                        height: dp(12)
                        pos_hint: {"center_x": 0.5, "top": 0.4}
            
                    MDRaisedButton:
                        text: "Scan"
                        pos_hint: {"center_x": 0.5, "top": 0.3}
                        on_press: app._switch_screen("home_screen")

                    
        MDScreen:
            name: "home_screen"

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
                                                text: "Day"
                                                halign: "center"
                                                theme_text_color: "Custom"
                                                text_color: 1,1,1,0.9
                                            MDLabel:
                                                id: days_label
                                                text: "0"
                                                halign: "center"
                                                font_style: "H4"
                                                text_color: 1,1,1,1
                                                
                                        MDCard:
                                            orientation: "vertical"
                                            md_bg_color: [0.1, 1, 0.2, 1]
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
                                            on_press: app.show_confirmation_dialog()
                                            
                                    MDCard:
                                        orientation: "horizontal"
                                        radius: [12]
                                        size_hint_y: None
                                        height: dp(45) 
                                        padding: [8]
                                        md_bg_color: "lightgrey"
                                        MDLabel:
                                            text: "Mode"
                                            font_size: 20
                                        MDRaisedButton:
                                            id: mode
                                            text: "Automatic"
                                            size_hint: (0.5, 1)
                                            md_bg_color: [0.2, 0.6, 1, 1]
                                            pos_hint: {"center_x": 0.5, "center_y": 0.5}
                                            on_press: app.mode()
                                            
                                    
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        padding: [8]
                                        spacing: dp(8)
                                        adaptive_height: True
                                        radius: [12]
                                        md_bg_color: "lightgrey"
                                        MDLabel:
                                            text: "Status"
                                            font_size: 20
                                            size_hint_y: None
                                            height: dp(25)
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
                                                md_bg_color: [0, 1, 0, 1]
                                                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                                                on_press: app._toast("bulb")
                                                disabled: True
            
            
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
                                                on_press: app._toast("fan")
                                                disabled: True
            
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
                                                md_bg_color: [0, 1, 0, 1]
                                                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                                                on_press: app._toast("hum")
                                                disabled: True
            
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
                                                on_press: app._toast("cam")
                                                disabled: True
        
        
                    MDBottomNavigationItem:
                        name: "nav_camera"
                        icon: "video"
                        text: "Camera"
                        on_tab_press: app.switch_screen("nav_camera")
                        MDBoxLayout:
                            orientation: "vertical"
                            size_hint: (1, 1)
                            spacing: dp(8)
                            MDBoxLayout:
                                id: camera
                                orientation: "vertical"
                                size_hint: (1, 0.5)
                                pos_hint: {"center_x": 0.5}
                                padding: dp(8)
                                md_bg_color: "lightgrey"
                                
                            MDBoxLayout:
                                orientation: 'horizontal'
                                padding: dp(8)
                                spacing: dp(8)
                                adaptive_size: True
                                pos_hint: {'center_x': 0.5}
                                MDIconButton:
                                    icon: 'skip-backward'
                                MDIconButton:
                                    id: play
                                    icon: 'play'
                                    on_press: app.play_pause()
                                MDIconButton:
                                    icon: 'skip-forward'
'''

day = 0
days_of_incubation = timedelta(days=21)

class CameraWidget(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = None
        threading.Thread(target=self.init_camera, daemon=True).start()

    def init_camera(self):
        self.capture = cv2.VideoCapture(0) #"http://100.67.254.128:8080/video"
        if not self.capture.isOpened():
            toast("Could not open camera. Skipping video stream.")
            return
        Clock.schedule_interval(self.update, 1.0 / 30.0)


    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Convert to texture
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture

class EggCubatorApp(MDApp):
    dialog = None
    def build(self):
        self.title = "Egg-cubator Mobile UI"
        self.theme_cls.primary_palette = "Orange"
        screen = Builder.load_string(KV)

        camera = CameraWidget()
        screen.ids.camera.add_widget(camera)

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
        Clock.schedule_interval(self.update_day, 10)  # for testing only
        return screen

    def switch_screen(self, name): #para sa MDBottomNavigation
        self.root.ids.current = name

    def _switch_screen(self, name): #para sa scanning og home screen
        self.root.ids.screen_manager.current = name

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

    def update_day(self, *args):
        global day
        if day < days_of_incubation.days:
            day += 1
            self.root.ids.days_label.text = str(day)
        else:
            toast("Incubation complete!")

    def _toast(self, button):
        btn = self.root.ids[button]
        if btn.text == "Off":
            btn.text = "On"
            toast(f"Successfully turned {btn.text}")
            btn.md_bg_color = [0, 1, 0, 1]  # green
        else:
            btn.text = "Off"
            toast(f"Successfully turned {btn.text}")
            btn.md_bg_color = [1, 0, 0, 1]  # red

    def mode(self):
        mode_btn = self.root.ids.mode

        new_mode = "Manual" if mode_btn.text == "Automatic" else "Automatic"
        mode_btn.text = new_mode

        mode_btn.md_bg_color = [1, 0.6, 0, 1] if new_mode == "Manual" else [0.2, 0.6, 1, 1]

        control_buttons = ["bulb", "fan", "hum", "cam"]

        is_manual = new_mode == "Manual"
        for btn_id in control_buttons:
            self.root.ids[btn_id].disabled = not is_manual

    def show_confirmation_dialog(self):
        if not self.dialog:
            box = MDBoxLayout(orientation="vertical", spacing="15dp", size_hint_y=None, height="180dp")

            # Temperature slider
            self.temp_label = MDLabel(
                text="Temperature: 37.5°C",
                halign="center",
                theme_text_color="Primary"
            )
            self.temp_slider = MDSlider(
                min=30,
                max=40,
                value=37.5,
                step=0.1,
                hint=True
            )
            self.temp_slider.bind(value=self.update_temp_label)

            # Humidity slider
            self.hum_label = MDLabel(
                text="Humidity: 55%",
                halign="center",
                theme_text_color="Primary"
            )
            self.hum_slider = MDSlider(
                min=40,
                max=80,
                value=55,
                step=1,
                hint=True
            )
            self.hum_slider.bind(value=self.update_hum_label)

            box.add_widget(self.temp_label)
            box.add_widget(self.temp_slider)
            box.add_widget(self.hum_label)
            box.add_widget(self.hum_slider)

            self.dialog = MDDialog(
                title="Setting environment",
                type="custom",
                content_cls=box,
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press=lambda x: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press=lambda x: self.update_stemp_shum(self.temp_slider.value, self.hum_slider.value)
                    ),
                ],

            )

        self.dialog.open()

    def update_temp_label(self, instance, value):
        self.temp_label.text = f"Temperature: {value:.1f}°C"

    def update_hum_label(self, instance, value):
        self.hum_label.text = f"Humidity: {int(value)}%"

    def update_stemp_shum(self, temp, hum):
        self.root.ids.stemp.text = f"Temperature: {temp} °C"
        self.root.ids.shum.text = f"Humidity: {hum}%"
        self.dialog.dismiss()

    def play_pause(self):
        self.root.ids.play.icon = 'pause' if self.root.ids.play.icon == 'play' else 'play'

    def on_stop(self):
        """Release camera safely on app close."""
        try:
            if hasattr(self, 'capture') and self.capture.isOpened():
                self.capture.release()
        except:
            pass

if __name__ == "__main__":
    EggCubatorApp().run()
