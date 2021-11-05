from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from datatypes import *


class AdminScreen(QDialog):
    def __init__(self, lexicon):
        super().__init__()
        self.lexicon = lexicon
        loadUi("ui/admin.ui", self)

        self.add_btn.clicked.connect(self.add_term)
        self.clean_status()

    def add_term(self):
        term = self.term_input.text()
        definition = self.definition_input.toPlainText()
        password = self.password_input.text()
        response = self.lexicon.store(term, definition, bytes(password, 'utf-8'))
        self.update_status(response)

    def update_status(self, status: StoreStatus):
        is_ok = status == StoreStatus.SUCCESS
        message = {
            StoreStatus.ALREADY_STORED: "This term is already in dictionary",
            StoreStatus.WRONG_PASSWORD: "Incorrect password",
            StoreStatus.EMPTY_LEMMA: "You forgot to specify a term!",
            StoreStatus.EMPTY_DEFINITION: "You forgot to specify a definition!",
            StoreStatus.SUCCESS: "Stored!"
        }.get(status, "Unexpected error happened")

        self.clean_status()
        self.display_status(is_ok, message)

    def clean_status(self):
        self.status_label.setText('')
        self.status_label.setHidden(True)

    def display_status(self, is_ok, message):
        stylesheet = {True: "color: #70E892;", False: "color: red;"}[is_ok]
        self.status_label.setStyleSheet(stylesheet)
        self.status_label.setText(message)
        self.status_label.setHidden(False)
