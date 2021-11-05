from PyQt5.QtWidgets import QDialog, QPushButton, QSizePolicy
from PyQt5.uic import loadUi


class UserScreen(QDialog):
    def __init__(self, lexicon):
        super().__init__()
        self.lexicon = lexicon

        loadUi("ui/user.ui", self)
        self.clean_see_also()

        self.find_btn.clicked.connect(self.define_from_input)
        self.term_input.returnPressed.connect(self.define_from_input)

    def update_see_also(self, terms=None):
        self.clean_see_also()
        if terms is not None and len(terms):
            self.display_see_also(terms)

    def clean_see_also(self):
        self.see_also_title.setHidden(True)
        self.remove_all_see_also_terms()

    def remove_all_see_also_terms(self):
        while self.see_also_terms.count() > 0:
            self.see_also_terms.itemAt(0).widget().setParent(None)

    def display_see_also(self, terms):
        self.see_also_title.setHidden(False)
        for btn in [self.create_see_also_button(term) for term in terms]:
            self.see_also_terms.addWidget(btn)

    def create_see_also_button(self, term):
        result = QPushButton()
        result.setText(term)
        result.setFlat(True)
        result.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        result.clicked.connect(lambda: self.define_term(term))
        return result

    def define_from_input(self):
        self.define_term(self.term_input.text())

    def define_term(self, term):
        lexeme = self.lexicon.define(term)
        if lexeme is not None:
            self.display_definition(lexeme)
        else:
            self.display_notFound_message()

    def display_definition(self, lexeme):
        self.term.setText(lexeme.lemma)
        self.definition.setText(lexeme.definition)
        self.update_see_also(lexeme.mentions)

    def display_notFound_message(self):
        self.term.setText("Term not found :(")
        self.definition.setText("")
        self.update_see_also()
