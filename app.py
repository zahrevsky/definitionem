from PyQt5.QtWidgets import QApplication, QStackedWidget

from ui import UserScreen, AdminScreen


class App(QApplication):
    def __init__(self, lexicon):
        super().__init__([])
        self.user_ui = UserScreen(lexicon)
        self.admin_ui = AdminScreen(lexicon)

        self.window = QStackedWidget()
        self.window.addWidget(self.user_ui),
        self.window.addWidget(self.admin_ui)

        self.user_ui.edit_btn.clicked.connect(self.switch_to_admin)
        self.admin_ui.open_dictionary_btn.clicked.connect(self.switch_to_user)

    def switch_to_admin(self):
        self.window.setCurrentWidget(self.admin_ui)

    def switch_to_user(self):
        self.window.setCurrentWidget(self.user_ui)

    def run(self):
        self.window.show()
        self.exec_()
