class Playfair:
    alphabet = "abcdefghiklmnopqrstuvwxyz"

    def __init__(self, key):
        self._key = key
        self._alphabet = ""
        self._grid = []
        self._grid_size = 5

        self._build_alphabet()
        self._build_grid()

    def _build_alphabet(self):
        cleaned_key = self._key.lower().replace("j", "i")

        for letter in cleaned_key:
            if letter in self.alphabet and letter not in self._alphabet:
                self._alphabet += letter

        for letter in self.alphabet:
            if letter not in self._alphabet:
                self._alphabet += letter

    def _build_grid(self):
        for row in range(self._grid_size):
            current_row = []

            for column in range(self._grid_size):
                letter = self._alphabet[row * self._grid_size + column]
                current_row.append(letter)

            self._grid.append(current_row)

    def preprocess(self, plaintext):
        cleaned_text = ""

        plaintext = plaintext.lower().replace("j", "i")

        for letter in plaintext:
            if letter in self.alphabet:
                cleaned_text += letter

        result = ""
        index = 0

        while index < len(cleaned_text):
            first_letter = cleaned_text[index]

            if index + 1 < len(cleaned_text):
                second_letter = cleaned_text[index + 1]

                if first_letter == second_letter:
                    result += first_letter + "x"
                    index += 1
                else:
                    result += first_letter + second_letter
                    index += 2
            else:
                result += first_letter
                index += 1

        if len(result) % 2 != 0:
            result += "z"

        return result

    def find_position(self, letter):
        for row_index, row in enumerate(self._grid):
            for column_index, current_letter in enumerate(row):
                if current_letter == letter:
                    return row_index, column_index

        return None

    def encrypt_digraph(self, first_letter, second_letter):
        row1, col1 = self.find_position(first_letter)
        row2, col2 = self.find_position(second_letter)

        if row1 == row2:
            encrypted_first = self._grid[row1][(col1 + 1) % self._grid_size]
            encrypted_second = self._grid[row2][(col2 + 1) % self._grid_size]

        elif col1 == col2:
            encrypted_first = self._grid[(row1 + 1) % self._grid_size][col1]
            encrypted_second = self._grid[(row2 + 1) % self._grid_size][col2]

        else:
            encrypted_first = self._grid[row1][col2]
            encrypted_second = self._grid[row2][col1]

        return encrypted_first + encrypted_second

    def decrypt_digraph(self, first_letter, second_letter):
        row1, col1 = self.find_position(first_letter)
        row2, col2 = self.find_position(second_letter)

        if row1 == row2:
            decrypted_first = self._grid[row1][(col1 - 1) % self._grid_size]
            decrypted_second = self._grid[row2][(col2 - 1) % self._grid_size]

        elif col1 == col2:
            decrypted_first = self._grid[(row1 - 1) % self._grid_size][col1]
            decrypted_second = self._grid[(row2 - 1) % self._grid_size][col2]

        else:
            decrypted_first = self._grid[row1][col2]
            decrypted_second = self._grid[row2][col1]

        return decrypted_first + decrypted_second

    def encrypt(self, plaintext):
        processed_text = self.preprocess(plaintext)
        ciphertext = ""

        for index in range(0, len(processed_text), 2):
            first_letter = processed_text[index]
            second_letter = processed_text[index + 1]

            ciphertext += self.encrypt_digraph(first_letter, second_letter)

        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ""

        for index in range(0, len(ciphertext), 2):
            first_letter = ciphertext[index]
            second_letter = ciphertext[index + 1]

            plaintext += self.decrypt_digraph(first_letter, second_letter)

        return plaintext


class PlayfairExtended:
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"

    def __init__(self, key):
        self._key = key
        self._alphabet = ""
        self._grid = []
        self._grid_size = 6

        self._build_alphabet()
        self._build_grid()

    def _build_alphabet(self):
        cleaned_key = self._key.lower()

        for character in cleaned_key:
            if character in self.alphabet and character not in self._alphabet:
                self._alphabet += character

        for character in self.alphabet:
            if character not in self._alphabet:
                self._alphabet += character

    def _build_grid(self):
        for row in range(self._grid_size):
            current_row = []

            for column in range(self._grid_size):
                character = self._alphabet[row * self._grid_size + column]
                current_row.append(character)

            self._grid.append(current_row)

    def preprocess(self, plaintext):
        cleaned_text = ""

        plaintext = plaintext.lower()

        for character in plaintext:
            if character in self.alphabet:
                cleaned_text += character

        result = ""
        index = 0

        while index < len(cleaned_text):
            first_character = cleaned_text[index]

            if index + 1 < len(cleaned_text):
                second_character = cleaned_text[index + 1]

                if first_character == second_character:
                    result += first_character + "x"
                    index += 1
                else:
                    result += first_character + second_character
                    index += 2
            else:
                result += first_character
                index += 1

        if len(result) % 2 != 0:
            result += "z"

        return result

    def find_position(self, character):
        for row_index, row in enumerate(self._grid):
            for column_index, current_character in enumerate(row):
                if current_character == character:
                    return row_index, column_index

        return None

    def encrypt_digraph(self, first_character, second_character):
        row1, col1 = self.find_position(first_character)
        row2, col2 = self.find_position(second_character)

        if row1 == row2:
            encrypted_first = self._grid[row1][(col1 + 1) % self._grid_size]
            encrypted_second = self._grid[row2][(col2 + 1) % self._grid_size]

        elif col1 == col2:
            encrypted_first = self._grid[(row1 + 1) % self._grid_size][col1]
            encrypted_second = self._grid[(row2 + 1) % self._grid_size][col2]

        else:
            encrypted_first = self._grid[row1][col2]
            encrypted_second = self._grid[row2][col1]

        return encrypted_first + encrypted_second

    def decrypt_digraph(self, first_character, second_character):
        row1, col1 = self.find_position(first_character)
        row2, col2 = self.find_position(second_character)

        if row1 == row2:
            decrypted_first = self._grid[row1][(col1 - 1) % self._grid_size]
            decrypted_second = self._grid[row2][(col2 - 1) % self._grid_size]

        elif col1 == col2:
            decrypted_first = self._grid[(row1 - 1) % self._grid_size][col1]
            decrypted_second = self._grid[(row2 - 1) % self._grid_size][col2]

        else:
            decrypted_first = self._grid[row1][col2]
            decrypted_second = self._grid[row2][col1]

        return decrypted_first + decrypted_second

    def encrypt(self, plaintext):
        processed_text = self.preprocess(plaintext)
        ciphertext = ""

        for index in range(0, len(processed_text), 2):
            first_character = processed_text[index]
            second_character = processed_text[index + 1]

            ciphertext += self.encrypt_digraph(first_character, second_character)

        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ""

        for index in range(0, len(ciphertext), 2):
            first_character = ciphertext[index]
            second_character = ciphertext[index + 1]

            plaintext += self.decrypt_digraph(first_character, second_character)

        return plaintext


def print_grid(title, grid):
    print(title)

    for row in grid:
        print(" ".join(row))

    print()


if __name__ == "__main__":
    print("NORMAL PLAYFAIR")
    cipher = Playfair("dog")

    print("Playfair alphabet:")
    print(cipher._alphabet)
    print()

    print_grid("Playfair grid:", cipher._grid)

    plaintext = "hello world"

    encrypted = cipher.encrypt(plaintext)
    decrypted = cipher.decrypt(encrypted)

    print("Original plaintext:", plaintext)
    print("Preprocessed plaintext:", cipher.preprocess(plaintext))
    print("Ciphertext:", encrypted)
    print("Decrypted:", decrypted)
    print()

    print("EXTENDED PLAYFAIR")
    extended = PlayfairExtended("dog123")

    print("Extended Playfair alphabet:")
    print(extended._alphabet)
    print()

    print_grid("Extended Playfair grid:", extended._grid)

    extended_plaintext = "hello 2026!!"

    extended_encrypted = extended.encrypt(extended_plaintext)
    extended_decrypted = extended.decrypt(extended_encrypted)

    print("Original plaintext:", extended_plaintext)
    print("Preprocessed plaintext:", extended.preprocess(extended_plaintext))
    print("Ciphertext:", extended_encrypted)
    print("Decrypted:", extended_decrypted)