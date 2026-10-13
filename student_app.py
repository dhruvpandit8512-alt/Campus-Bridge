from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import RoundedRectangle, Color, Ellipse
import database

Window.size = (400, 750)
Window.clearcolor = get_color_from_hex("#F0F9FF") 

TEXT_DARK = get_color_from_hex("#0F172A")
TEXT_MUTED = get_color_from_hex("#64748B")

CARD_WIDTH = 340
ELEM_WIDTH = 290

# FLUID BACKGROUND
class ModernBackground(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=get_color_from_hex("#BAE6FD"))
            self.blob1 = Ellipse(size=(350, 350))
            Color(rgba=get_color_from_hex("#7DD3FC"))
            self.blob2 = Ellipse(size=(450, 450))
            Color(rgba=get_color_from_hex("#38BDF8"), a=0.2)
            self.blob3 = Ellipse(size=(250, 250))
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.blob1.pos = (self.x - 100, self.top - 250)
        self.blob2.pos = (self.right - 250, self.y - 150)
        self.blob3.pos = (self.center_x - 125, self.center_y - 125)

# WHITE FLOATING CARD
class WhiteCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 25
        self.spacing = 15
        self.size_hint = (None, None)
        self.width = CARD_WIDTH
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.45}
        with self.canvas.before:
            Color(rgba=(0, 0, 0, 0.08))
            self.shadow = RoundedRectangle(radius=[20])
            Color(rgba=(1, 1, 1, 1))
            self.card = RoundedRectangle(radius=[20])
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.shadow.pos = (self.x, self.y - 6)
        self.shadow.size = self.size
        self.card.pos = self.pos
        self.card.size = self.size

# FIXED UI ELEMENTS
class RoundedButton(Button):
    def __init__(self, bg_color_hex="#3B82F6", text_color_hex="#FFFFFF", **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.bg_color = get_color_from_hex(bg_color_hex)
        self.color = get_color_from_hex(text_color_hex)
        self.size_hint_x = None
        self.width = ELEM_WIDTH
        self.pos_hint = {'center_x': 0.5}
        with self.canvas.before:
            Color(rgba=self.bg_color)
            self.rect = RoundedRectangle(radius=[15]) 
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class StyledTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = get_color_from_hex("#F8FAFC")
        self.foreground_color = TEXT_DARK
        self.cursor_color = TEXT_DARK
        self.padding_y = [15, 15]
        self.padding_x = [15, 15]
        self.font_size = 14
        self.size_hint_x = None
        self.width = ELEM_WIDTH
        self.pos_hint = {'center_x': 0.5}

class StudentApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user_name = ""
        self.current_user_roll = ""

    def build(self):
        self.root_layout = ModernBackground() 
        database.connect_db()
        self.show_login()
        return self.root_layout

    def create_header(self, title, subtitle):
        box = BoxLayout(orientation='vertical', size_hint=(1, None), height=140, pos_hint={'top': 0.95})
        box.add_widget(Label(text="🌉", font_size=40, size_hint_y=None, height=50))
        box.add_widget(Label(text="CAMPUS BRIDGE", font_size=24, bold=True, color=get_color_from_hex("#1E3A8A"), size_hint_y=None, height=40))
        box.add_widget(Label(text=title, font_size=16, color=TEXT_DARK, size_hint_y=None, height=30))
        if subtitle:
            box.add_widget(Label(text=subtitle, font_size=14, color=TEXT_MUTED, size_hint_y=None, height=20))
        return box

    # 1. LOGIN WITH NAME & ROLL NO
    def show_login(self):
        self.current_user_name = ""
        self.current_user_roll = ""
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.create_header("Student Portal", "Sign in to continue"))

        card = WhiteCard(height=340, pos_hint={'center_x': 0.5, 'center_y': 0.40})
        
        card.add_widget(Label(text="Login Card", font_size=18, bold=True, color=TEXT_DARK, size_hint_y=None, height=30))
        
        self.name_input_login = StyledTextInput(hint_text="👤 Enter Your Name", multiline=False, size_hint_y=None, height=55)
        card.add_widget(self.name_input_login)

        self.roll_input_login = StyledTextInput(hint_text="🎓 Enter Roll No.", multiline=False, size_hint_y=None, height=55)
        card.add_widget(self.roll_input_login)
        
        login_btn = RoundedButton(bg_color_hex="#10B981", text="LOGIN SECURELY", font_size=16, bold=True, size_hint_y=None, height=55)
        login_btn.bind(on_release=self.process_login)
        card.add_widget(login_btn)

        self.login_error = Label(text="", size_hint_y=None, height=20, color=get_color_from_hex("#EF4444"))
        card.add_widget(self.login_error)
        self.root_layout.add_widget(card)

    def process_login(self, _button):
        name = self.name_input_login.text.strip()
        roll_no = self.roll_input_login.text.strip()
        if not name or not roll_no:
            self.login_error.text = "Both Name and Roll No. required!"
            return
        self.current_user_name = name
        self.current_user_roll = roll_no
        self.show_home()

    def show_home(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.create_header("How can we help?", f"Hello, {self.current_user_name} ({self.current_user_roll})"))

        card = WhiteCard(height=280, pos_hint={'center_x': 0.5, 'center_y': 0.45})
        
        raise_btn = RoundedButton(bg_color_hex="#2563EB", text="RAISE A CONCERN", font_size=16, bold=True, size_hint_y=None, height=60)
        raise_btn.bind(on_release=lambda *_: self.show_form())
        card.add_widget(raise_btn)

        track_btn = RoundedButton(bg_color_hex="#8B5CF6", text="TRACK MY REQUEST", font_size=16, bold=True, size_hint_y=None, height=60)
        track_btn.bind(on_release=lambda *_: self.show_tracking_form())
        card.add_widget(track_btn)

        logout_btn = RoundedButton(bg_color_hex="#FEE2E2", text_color_hex="#EF4444", text="LOGOUT", font_size=16, bold=True, size_hint_y=None, height=60)
        logout_btn.bind(on_release=lambda *_: self.show_login())
        card.add_widget(logout_btn)

        self.root_layout.add_widget(card)

    def show_form(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.create_header("Raise Concern", "Submit your issue"))

        card = WhiteCard(height=450, pos_hint={'center_x': 0.5, 'center_y': 0.40})
        
        
        self.name_input = StyledTextInput(text=self.current_user_name, hint_text="Your Full Name", multiline=False, size_hint_y=None, height=50)
        self.department_input = StyledTextInput(hint_text="Department (e.g., BCA)", multiline=False, size_hint_y=None, height=50)
        
        self.category_input = Spinner(
            text="Select Category", values=("Academic", "Examination", "Infrastructure", "Faculty", "Fees", "Other"), 
            size_hint_y=None, height=50, size_hint_x=None, width=ELEM_WIDTH, pos_hint={'center_x': 0.5},
            background_normal='', background_color=get_color_from_hex("#F8FAFC"), color=TEXT_DARK
        )
        
        self.details_input = StyledTextInput(hint_text="Describe the issue...", multiline=True, size_hint_y=None, height=80)
        
        self.status_label = Label(text="", size_hint_y=None, height=20)

        submit_btn = RoundedButton(bg_color_hex="#10B981", text="SUBMIT", font_size=16, bold=True, size_hint_y=None, height=50)
        submit_btn.bind(on_release=self.submit_concern)

        back_btn = RoundedButton(bg_color_hex="#94A3B8", text="BACK", size_hint_y=None, height=50)
        back_btn.bind(on_release=lambda *_: self.show_home())

        for w in (self.name_input, self.department_input, self.category_input, self.details_input, self.status_label, submit_btn, back_btn):
            card.add_widget(w)
        self.root_layout.add_widget(card)

    def submit_concern(self, _button):
        name = self.name_input.text.strip()
        department = self.department_input.text.strip()
        category = self.category_input.text
        details = self.details_input.text.strip()

        if not name or not department or not details or category == "Select Category":
            self.status_label.text = "Please fill all fields!"
            self.status_label.color = get_color_from_hex("#EF4444")
            return

        concern_id = database.save_concern(name, department, category, details)
        self.show_feedback_screen(concern_id) 

    def show_feedback_screen(self, concern_id):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.create_header("Success!", f"Tracking ID: #{concern_id}"))

        card = WhiteCard(height=250, pos_hint={'center_x': 0.5, 'center_y': 0.45})
        card.add_widget(Label(text="How was your experience?", font_size=18, color=TEXT_DARK, size_hint_y=None, height=40))

        feedback_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60, size_hint_x=None, width=ELEM_WIDTH, pos_hint={'center_x': 0.5})
        for emoji, text in [("😡", "Bad"), ("😐", "Okay"), ("😍", "Great")]:
            btn = RoundedButton(bg_color_hex="#F1F5F9", text_color_hex="#0F172A", text=f"{emoji}\n{text}")
            btn.width = 90
            btn.bind(on_release=lambda *_: self.show_home()) 
            feedback_box.add_widget(btn)
        card.add_widget(feedback_box)

        card.add_widget(Label(size_hint_y=None, height=10))
        home_btn = RoundedButton(bg_color_hex="#2563EB", text="BACK TO HOME", size_hint_y=None, height=55)
        home_btn.bind(on_release=lambda *_: self.show_home())
        card.add_widget(home_btn)
        self.root_layout.add_widget(card)

    def show_tracking_form(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.create_header("Track Request", "Check live status"))

        card = WhiteCard(height=340, pos_hint={'center_x': 0.5, 'center_y': 0.45})
        
        self.track_input = StyledTextInput(hint_text="Enter ID (e.g., 49201)", multiline=False, size_hint_y=None, height=55, input_filter='int', halign="center")
        card.add_widget(self.track_input)

        self.track_result_label = Label(text="Enter ID to view status.", size_hint_y=None, height=80, color=TEXT_MUTED, halign="center")
        card.add_widget(self.track_result_label)

        check_btn = RoundedButton(bg_color_hex="#3B82F6", text="CHECK NOW", font_size=16, bold=True, size_hint_y=None, height=55)
        check_btn.bind(on_release=self.check_status)
        card.add_widget(check_btn)

        back_btn = RoundedButton(bg_color_hex="#94A3B8", text="BACK", size_hint_y=None, height=55)
        back_btn.bind(on_release=lambda *_: self.show_home())
        card.add_widget(back_btn)

        self.root_layout.add_widget(card)

    def check_status(self, _button):
        track_id = self.track_input.text.strip()
        if not track_id:
            self.track_result_label.text = "Please enter an ID!"
            self.track_result_label.color = get_color_from_hex("#EF4444")
            return
        try:
            concern = database.get_concern_by_id(int(track_id))
            if concern:
                s_color = "#10B981" if concern[5] == "Resolved" else "#EF4444" if concern[5] == "Rejected" else "#3B82F6"
                self.track_result_label.text = f"Category: {concern[3]}\nStatus: [b][color={s_color}]{concern[5]}[/color][/b]"
                self.track_result_label.markup = True
            else:
                self.track_result_label.text = "Record not found."
                self.track_result_label.color = get_color_from_hex("#EF4444")
        except:
            self.track_result_label.text = "Error fetching details."

if __name__ == "__main__":
    StudentApp().run()