from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import RoundedRectangle, Color, Ellipse
import database

Window.size = (1100, 750)
Window.clearcolor = get_color_from_hex("#FFF1F2") 

TEXT_DARK = get_color_from_hex("#0F172A")
TEXT_MUTED = get_color_from_hex("#64748B")

CARD_WIDTH = 450
ELEM_WIDTH = 380

class AdminBackground(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=get_color_from_hex("#FECDD3")) 
            self.blob1 = Ellipse(size=(500, 500))
            Color(rgba=get_color_from_hex("#FDA4AF")) 
            self.blob2 = Ellipse(size=(600, 600))
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.blob1.pos = (self.x - 100, self.top - 400)
        self.blob2.pos = (self.right - 400, self.y - 200)

class WhiteCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 35
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

class RoundedButton(Button):
    def __init__(self, bg_color_hex="#E11D48", text_color_hex="#FFFFFF", **kwargs):
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
        self.padding_y = [18, 18]
        self.padding_x = [18, 18]
        self.font_size = 16
        self.size_hint_x = None
        self.width = ELEM_WIDTH
        self.pos_hint = {'center_x': 0.5}

class AdminApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_staff_name = ""
        self.current_staff_role = ""

    def build(self):
        self.root_layout = AdminBackground()
        database.connect_db()
        self.show_login()
        return self.root_layout

    def create_header(self, title, subtitle):
        box = BoxLayout(orientation='vertical', size_hint=(1, None), height=140, pos_hint={'top': 0.95})
        box.add_widget(Label(text="🛡️", font_size=40, size_hint_y=None, height=50))
        box.add_widget(Label(text="CAMPUS BRIDGE", font_size=28, bold=True, color=get_color_from_hex("#BE123C"), size_hint_y=None, height=40))
        box.add_widget(Label(text=title, font_size=18, color=TEXT_DARK, size_hint_y=None, height=30))
        if subtitle:
            box.add_widget(Label(text=subtitle, font_size=16, color=TEXT_MUTED, size_hint_y=None, height=20))
        return box

    def show_login(self):
        self.current_staff_name = ""
        self.current_staff_role = ""
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.create_header("Admin Access Center", "Authorized Personnel Only"))

        card = WhiteCard(height=390)
        card.add_widget(Label(text="Faculty Login", font_size=20, bold=True, color=TEXT_DARK, size_hint_y=None, height=40))
        
        self.staff_name_input = StyledTextInput(hint_text="👤 Enter Your Name", multiline=False, size_hint_y=None, height=55)
        card.add_widget(self.staff_name_input)

        self.staff_id_input = StyledTextInput(hint_text="📧 Staff ID / Email", multiline=False, size_hint_y=None, height=55)
        card.add_widget(self.staff_id_input)

        self.role_spinner = Spinner(
            text="Select Role", values=("HOD", "Faculty", "Principal"), 
            size_hint_y=None, height=55, size_hint_x=None, width=ELEM_WIDTH, pos_hint={'center_x': 0.5},
            background_normal='', background_color=get_color_from_hex("#F1F5F9"), color=TEXT_DARK
        )
        card.add_widget(self.role_spinner)
        
        login_btn = RoundedButton(bg_color_hex="#E11D48", text="ACCESS DASHBOARD", font_size=18, bold=True, size_hint_y=None, height=55)
        login_btn.bind(on_release=self.process_login)
        card.add_widget(login_btn)

        self.login_error = Label(text="", size_hint_y=None, height=20, color=get_color_from_hex("#EF4444"))
        card.add_widget(self.login_error)
        self.root_layout.add_widget(card)

    def process_login(self, _button):
        name = self.staff_name_input.text.strip()
        staff_id = self.staff_id_input.text.strip()
        role = self.role_spinner.text
        if not name or not staff_id or role == "Select Role":
            self.login_error.text = "Please fill all fields."
            return
        self.current_staff_name = name
        self.current_staff_role = role
        self.show_dashboard()

    def show_dashboard(self):
        self.root_layout.clear_widgets()
        
        header_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, pos_hint={'top': 1})
        header_box.add_widget(Label(
            text=f"  Welcome {self.current_staff_role}, {self.current_staff_name}", 
            font_size=20, bold=True, color=TEXT_DARK, halign="left"
        ))
        
        logout_btn = RoundedButton(bg_color_hex="#FEE2E2", text_color_hex="#E11D48", text="LOGOUT", size_hint_x=None, width=150)
        logout_btn.pos_hint = {'center_y': 0.5}
        logout_btn.bind(on_release=lambda *_: self.show_login())
        header_box.add_widget(logout_btn)
        
        self.root_layout.add_widget(header_box)

        content = FloatLayout(size_hint=(1, 0.85), pos_hint={'y': 0})
        concerns = database.get_all_concerns()

        scroll = ScrollView(size_hint=(None, 1), width=800, pos_hint={'center_x': 0.5})
        grid = GridLayout(cols=1, spacing=15, padding=[0,20], size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        if not concerns:
            grid.add_widget(Label(text="No active concerns.", color=TEXT_DARK, size_hint_y=None, height=50))
        else:
            for c in concerns:
                s_col = "#10B981" if c[5] == "Resolved" else "#EF4444" if c[5] == "Rejected" else "#3B82F6"
                
                txt = f"[b]Track ID: #{c[0]}[/b]  |  [b]Student: {c[1]}[/b]\nDept: {c[2]}  |  Category: {c[3]}\n[color={s_col}]Status: {c[5]}[/color]\n{c[4]}"
                
                card = RoundedButton(bg_color_hex="#FFFFFF", text_color_hex="#0F172A", text=txt, markup=True, size_hint_y=None, height=140)
                card.width = 750
                card.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0]-40, None)))
                card.bind(on_release=lambda ins, cur_c=c: self.show_concern_details(cur_c))
                grid.add_widget(card)

        scroll.add_widget(grid)
        content.add_widget(scroll)
        self.root_layout.add_widget(content)

    def show_concern_details(self, concern_data):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.create_header(f"Update Concern #{concern_data[0]}", "Change the live status below"))

        card = WhiteCard(height=350)
        details = f"Student: {concern_data[1]}\nDept: {concern_data[2]}\nCategory: {concern_data[3]}\n\nDescription:\n{concern_data[4]}"
        card.add_widget(Label(text=details, font_size=16, color=TEXT_DARK, size_hint_y=0.4))

        self.update_spinner = Spinner(
            text="Update Status", values=("Assigned to Faculty", "In Progress", "Resolved", "Rejected"), 
            size_hint_y=None, height=55, size_hint_x=None, width=ELEM_WIDTH, pos_hint={'center_x': 0.5},
            background_normal='', background_color=get_color_from_hex("#F1F5F9"), color=TEXT_DARK
        )
        card.add_widget(self.update_spinner)

        update_btn = RoundedButton(bg_color_hex="#10B981", text="SAVE NEW STATUS", bold=True, size_hint_y=None, height=55)
        update_btn.bind(on_release=lambda *_: self.save_new_status(concern_data[0]))
        card.add_widget(update_btn)

        back_btn = RoundedButton(bg_color_hex="#94A3B8", text="BACK", size_hint_y=None, height=55)
        back_btn.bind(on_release=lambda *_: self.show_dashboard())
        card.add_widget(back_btn)
        
        self.root_layout.add_widget(card)

    def save_new_status(self, concern_id):
        new_status = self.update_spinner.text
        if new_status != "Update Status":
            database.update_status(concern_id, new_status)
            self.show_dashboard()

if __name__ == "__main__":
    AdminApp().run()