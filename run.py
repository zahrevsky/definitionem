from lexicon import Lexicon
from app import App


if __name__ == '__main__':
    with open('scrt', 'rb') as secret_file:
        password_hash = secret_file.read()

    lexicon = Lexicon('dictionary.json', password_hash)
    app = App(lexicon)
    app.run()
