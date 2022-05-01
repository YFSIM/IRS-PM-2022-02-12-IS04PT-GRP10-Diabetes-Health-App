from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.modalview import ModalView
from kivy.utils import platform
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooser
from kivy.uix.image import Image
from UserDatabase import User
from EyeImageProcessing import EyeImgProcessing
import os

if platform == "android":
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
    from android.storage import primary_external_storage_path

    primary_ext_storage = primary_external_storage_path()

kv = """
Screen:
    pw_txt: PWtext 
    user_txt: UserNametext
    screen_mgr: screen_manager
    label_user: mdlabelUser
    retina_img: retinaimg

    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: "Diabetes Management"
            left_action_items: [["menu", lambda x: nav_draw.set_state()]]
        Widget:
    MDNavigationLayout: 
        ScreenManager:
            id: screen_manager
            Screen:     
                name: "login"

                MDTextField:
                    id: UserNametext
                    hint_text: 'Enter User Name'
                    #helper_text: 'Forgot your password?'
                    helper_text_mode: "on_focus" 
                    pos_hint: {'center_x': 0.5, 'center_y': 0.6}
                    size_hint_x: None
                    width: 300
                    icon_right: "account"
                    required: True

                MDTextField:
                    id: PWtext
                    hint_text: 'Enter Password'
                    #helper_text: 'Forgot your password?'
                    helper_text_mode: "on_focus" 
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    size_hint_x: None
                    width: 300
                    icon_right: "account-search"
                    required: True

                MDRectangleFlatButton:
                    text: 'Submit'
                    pos_hint: {'center_x': 0.5, 'center_y': 0.3}
                    on_press:
                        app.auth()

                MDLabel:
                    text: ''
                    id: show
                    pos_hint: {'center_x': 1.0, 'center_y': 0.2}

            Screen:
                name: "retina"

                MDRectangleFlatButton:
                    text: "Browse"
                    pos_hint: {'center_x': 0.5, 'center_y': 0.3}
                    on_press:
                        app.file_manager_open()

                FitImage:
                    id: retinaimg
                    #size_hint_y: 3
                    #height: dp(40) 
                    size_hint: None, None
                    pos_hint: {'center_x': 0.5, 'center_y': 0.6}
                    size: "224dp", "224dp"
                    
                MDRectangleFlatButton:
                    text: "Analyse"
                    pos_hint: {'center_x': 0.5, 'center_y': 0.2}
                    on_press:
                        app.analyseimage()

            Screen:
                name: "logininformation"
                MDLabel:
                    text: "LoginInformation"
                    halign: "center"

            Screen:
                name: "scr2"
                MDLabel:
                    text: "About"
                    halign: "center"

        MDNavigationDrawer:
            id: nav_draw
            orientation: "vertical"
            padding: "8dp"
            spacing: "8dp"

            AnchorLayout:
                anchor_x: "left"
                size_hint_y: None
                height: avatar.height

                Image:
                    id: avatar
                    size_hint: None, None
                    size: "56dp", "56dp"
                    source: "Photo.jpeg"

            MDLabel:
                id: mdlabelUser
                font_style: "Button"
                size_hint_y: None
                height: self.texture_size[1]

            MDLabel:
                text: "sahendrapang@gmail.com"
                font_style: "Caption"
                size_hint_y: None
                height: self.texture_size[1]

            ScrollView:
                MDList:
                    OneLineAvatarListItem:
                        on_press:
                            nav_draw.set_state("close")
                            app.checkloginscreen()
                            #screen_manager.current = "login"

                        text: "Account"
                        IconLeftWidget:
                            icon: "account"
                            
                    OneLineAvatarListItem:
                        on_press:
                            nav_draw.set_state("close")
                            screen_manager.current = "retina"
                        text: "Stategy1"
                        IconLeftWidget:
                            icon: 'eye'

                    OneLineAvatarListItem:
                        on_press:
                            nav_draw.set_state("close")
                            screen_manager.current = "retina"
                        text: "Eye"
                        IconLeftWidget:
                            icon: 'eye'

                    OneLineAvatarListItem:
                        on_press:
                            nav_draw.set_state("close")
                            screen_manager.current = "scr2"
                        text: "About"
                        IconLeftWidget:
                            icon: 'information'

            Widget:
"""


class Main(MDApp):
    pw_txt = ObjectProperty(None)
    screen_mgr = ObjectProperty(None)
    user_txt = ObjectProperty(None)
    label_user = ObjectProperty(None)

    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    lbl_path = ObjectProperty(None)
    img = ObjectProperty(None)
    retina_img = ObjectProperty(None)
    picture_path = ""
    manager = None

    user1 = User('user.txt')
    eyeimgprocessing1 = EyeImgProcessing()

    def build(self):
        return Builder.load_string(kv)

    def auth(self):
        if self.user1.auth(self.root.user_txt.text, self.root.pw_txt.text) == True:
            self.root.label_user.text = self.root.user_txt.text
            self.root.screen_mgr.current = "logininformation"
        else:
            self.dialog = MDDialog(title='Password check',
                                   text="Wrong Password !", size_hint=(0.8, 1),
                                   buttons=[MDFlatButton(text='Close', on_release=self.close_dialog),
                                            MDFlatButton(text='More')]
                                   )
            self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def checkloginscreen(self):
        if self.user1._userlogin == True:
            self.root.screen_mgr.current = "logininformation"
        else:
            self.root.screen_mgr.current = "login"

    def file_manager_open(self):
        if not self.manager:
            self.file_manager = MDFileManager(
                exit_manager=self.exit_manager, select_path=self.select_path, preview=False, )
            if (platform != 'android'):
                self.file_manager.show('/')
            else:
                self.file_manager.show(primary_ext_storage)
        self.manager_open = True

    def select_path(self, path):
        self.exit_manager()
        toast(path)
        self.root.retina_img.source = path

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def analyseimage(self):
        self.eyeimgprocessing1.readLabel()


Main().run()