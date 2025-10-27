import random
import string
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
import os

def random_ssid():
    """Generate a random Wi-Fi SSID-like name."""
    prefixes = ["Net", "Link", "Home", "Office", "Cafe", "Galaxy", "Router", "XNet"]
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return random.choice(prefixes) + "-" + suffix

class WifiBox(BoxLayout):
    def __init__(self, total_names=20, target_name="Delower 5G", step_interval=1.0, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.total_names = total_names
        self.target_name = target_name
        self.step_interval = step_interval
        self.index = 0

        # create Wi-Fi name list (19 random + 1 correct)
        self.name_list = [random_ssid() for _ in range(self.total_names - 1)]
        self.name_list.append(self.target_name)

        # automatically choose gif if available, else png
        icon_source = "wifi_anim.gif" if os.path.exists("wifi_anim.gif") else "wifi_icon.png"

        # UI setup
        self.icon = Image(source=icon_source, allow_stretch=True, size_hint=(1, 0.7))
        self.add_widget(self.icon)

        self.label = Label(text="Starting Wi-Fi Scan...", color=(1, 0, 0, 1), font_size="20sp")
        self.add_widget(self.label)

        # start animation and scanning
        Clock.schedule_once(self.start_animation, 0.5)
        Clock.schedule_once(self.start_scan, 1)

    def start_animation(self, *args):
        # Light pulsing animation over gif
        anim = (
            Animation(opacity=0.4, duration=0.5) +
            Animation(opacity=1.0, duration=0.5)
        )
        anim.repeat = True
        anim.start(self.icon)

    def start_scan(self, *args):
        self.label.text = "Scanning Wi-Fi..."
        Clock.schedule_interval(self.step_one, self.step_interval)

    def step_one(self, dt):
        if self.index < self.total_names - 1:
            name = self.name_list[self.index]
            self.label.text = f"Trying... {name}"
            self.label.color = (1, 0, 0, 1)  # red text
            self.index += 1
        else:
            # success message
            name = self.target_name
            self.label.text = f"Connected: {name} ✅ "
            self.label.color = (0, 1, 0, 1)  # green
            return False  # stop timer

class WifiAnimApp(App):
    def build(self):
        return WifiBox(total_names=20, target_name="Delower 5G", step_interval=1.0)

if __name__ == "__main__":
    WifiAnimApp().run()
