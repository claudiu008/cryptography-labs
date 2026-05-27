class Playfair:
    alphabet = "abcdefghiklmnopqrstuvwxyz"

    def __init__(self, key):
        self.key = key
        self.alphabet = ""
        self.grid = []

        