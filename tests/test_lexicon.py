import json
import unittest
from unittest.mock import patch, mock_open
from lexicon import Lexicon
from datatypes import *
import bcrypt


def init_lexicon(*lexemes: Lexeme):
    password = b"admin"
    file_content = json.dumps([lexeme.dict() for lexeme in lexemes])

    with patch("lexicon.open", mock_open(read_data=file_content)):
        return Lexicon(
            vocabulary_filename='./vocabulary',
            password_hash=bcrypt.hashpw(password, bcrypt.gensalt())
        ), password


class ReadFromLexicon_TestCase(unittest.TestCase):
    def test_read_fromEmpty(self) -> None:
        lexicon, _ = init_lexicon()
        result = lexicon.define('  foo')
        self.assertEqual(None, result)

    def test_read_nonExisting(self) -> None:
        lexeme = Lexeme(lemma="foobar", definition="foobar", mentions=[], is_built_in=True)
        lexicon, _ = init_lexicon(lexeme)
        self.assertEqual(None, lexicon.define("hello"))

    def test_read_existing(self) -> None:
        lexeme1 = Lexeme(
            lemma="foobar",
            definition="Fucked Up Beyond All Recognition",
            mentions=[],
            is_built_in=True
        )
        lexeme2 = Lexeme(
            lemma="Hello world",
            definition="From the author of 'C programming language'",
            mentions=[],
            is_built_in=True
        )
        lexeme3 = Lexeme(
            lemma="String placeholder",
            definition="Most common are foobar and Hello world",
            mentions=['foobar', 'hello world'],
            is_built_in=True
        )
        lexicon, _ = init_lexicon(lexeme1, lexeme2, lexeme3)
        self.assertEqual(lexeme1, lexicon.define('  foobar'))
        self.assertEqual(lexeme2, lexicon.define('Hello world   '))
        self.assertEqual(lexeme3, lexicon.define('   string placeholder    '))


class StoreToLexicon_TestCase(unittest.TestCase):
    def test_store_thenRead(self) -> None:
        lemma, definition = "Hello", " world!"
        lexicon, password = init_lexicon()

        with patch("lexicon.open", mock_open()) as file_mock:
            response = lexicon.store(lemma, definition, password)

        self.assertEqual(StoreStatus.SUCCESS, response)

        retrieved_lexeme: Lexeme = lexicon.define("   helLO ")
        self.assertIsNotNone(retrieved_lexeme)
        self.assertEqual(lemma, retrieved_lexeme.lemma)
        self.assertEqual(definition, retrieved_lexeme.definition)
        self.assertEqual(0, len(retrieved_lexeme.mentions))
        self.assertFalse(retrieved_lexeme.is_built_in)

    def test_store_withWrongPassword(self) -> None:
        lexicon, password = init_lexicon()
        response = lexicon.store("foobar", "foobar", password + b"rubbish to make password wrong")
        self.assertEqual(StoreStatus.WRONG_PASSWORD, response)

    def test_store_override(self) -> None:
        lemma = "foobar"

        lexeme = Lexeme(
            lemma=lemma,
            definition="some definition",
            mentions=[],
            is_built_in=True
        )
        lexicon, password = init_lexicon(lexeme)

        response = lexicon.store(lemma, "some other definition", password)
        self.assertEqual(StoreStatus.ALREADY_STORED, response)


if __name__ == '__main__':
    unittest.main()
