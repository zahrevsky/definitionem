from typing import Optional
import json
import bcrypt

from datatypes import *


class Lexicon(object):
    def __init__(self, vocabulary_filename, password_hash) -> None:
        self._vocabulary_filename = vocabulary_filename
        self._password_hash = password_hash

        self._stored_lexemes = {}
        with open(vocabulary_filename) as vocabulary_file:
            for lexeme in json.load(vocabulary_file):
                self._store(Lexeme.parse_obj(lexeme))

    def define(self, term) -> Optional[Lexeme]:
        return self._stored_lexemes.get(term.lower().strip(), None)

    def store(self, lemma, definition, password) -> StoreStatus:
        if not bcrypt.checkpw(password, self._password_hash):
            return StoreStatus.WRONG_PASSWORD

        if len(lemma) == 0:
            return StoreStatus.EMPTY_LEMMA
        if len(definition) == 0:
            return StoreStatus.EMPTY_DEFINITION

        if lemma.lower() in self._stored_lexemes:
            return StoreStatus.ALREADY_STORED
        else:
            self._store(Lexeme(lemma=lemma, definition=definition, is_built_in=False))
            self._dump()
            return StoreStatus.SUCCESS

    def _store(self, lexeme) -> None:
        headword = lexeme.lemma.lower().strip()
        self._stored_lexemes[headword] = lexeme

    def _dump(self) -> None:
        with open(self._vocabulary_filename, 'w') as vocabulary_file:
            json.dump([lexeme.dict() for lexeme in self._stored_lexemes.values()], vocabulary_file)
