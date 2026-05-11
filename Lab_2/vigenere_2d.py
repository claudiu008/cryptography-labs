from itertools import product


class Vigenere2D:
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self, key_matrix, columns):
        self._key_matrix = key_matrix
        self._columns = columns

    def text_to_matrix(self, text):
        matrix = []
        row = []

        for letter in text.lower():
            if letter in self.alphabet:
                row.append(letter)

                if len(row) == self._columns:
                    matrix.append(row)
                    row = []

        if len(row) > 0:
            while len(row) < self._columns:
                row.append("z")

            matrix.append(row)

        return matrix

    def matrix_to_text(self, matrix):
        text = ""

        for row in matrix:
            for letter in row:
                text += letter

        return text

    def get_key_letter(self, row_index, column_index):
        key_row = row_index % len(self._key_matrix)
        key_column = column_index % len(self._key_matrix[0])

        return self._key_matrix[key_row][key_column]

    def encrypt(self, plaintext):
        plaintext_matrix = self.text_to_matrix(plaintext)
        ciphertext_matrix = []

        for row_index, row in enumerate(plaintext_matrix):
            ciphertext_row = []

            for column_index, plaintext_letter in enumerate(row):
                key_letter = self.get_key_letter(row_index, column_index)

                plaintext_position = self.alphabet.index(plaintext_letter)
                key_position = self.alphabet.index(key_letter)

                ciphertext_position = (plaintext_position + key_position) % 26
                ciphertext_letter = self.alphabet[ciphertext_position]

                ciphertext_row.append(ciphertext_letter)

            ciphertext_matrix.append(ciphertext_row)

        return self.matrix_to_text(ciphertext_matrix)

    def decrypt(self, ciphertext):
        ciphertext_matrix = self.text_to_matrix(ciphertext)
        plaintext_matrix = []

        for row_index, row in enumerate(ciphertext_matrix):
            plaintext_row = []

            for column_index, ciphertext_letter in enumerate(row):
                key_letter = self.get_key_letter(row_index, column_index)

                ciphertext_position = self.alphabet.index(ciphertext_letter)
                key_position = self.alphabet.index(key_letter)

                plaintext_position = (ciphertext_position - key_position) % 26
                plaintext_letter = self.alphabet[plaintext_position]

                plaintext_row.append(plaintext_letter)

            plaintext_matrix.append(plaintext_row)

        return self.matrix_to_text(plaintext_matrix)

    def split_ciphertext_by_key_position(self, ciphertext):
        ciphertext_matrix = self.text_to_matrix(ciphertext)

        key_rows = len(self._key_matrix)
        key_columns = len(self._key_matrix[0])

        streams = []

        for key_row in range(key_rows):
            stream_row = []

            for key_column in range(key_columns):
                stream_row.append("")

            streams.append(stream_row)

        for row_index, row in enumerate(ciphertext_matrix):
            for column_index, ciphertext_letter in enumerate(row):
                key_row = row_index % key_rows
                key_column = column_index % key_columns

                streams[key_row][key_column] += ciphertext_letter

        return streams


def score_english_text(text):
    english_frequencies = {
        "a": 8.2, "b": 1.5, "c": 2.8, "d": 4.3, "e": 12.7,
        "f": 2.2, "g": 2.0, "h": 6.1, "i": 7.0, "j": 0.15,
        "k": 0.8, "l": 4.0, "m": 2.4, "n": 6.7, "o": 7.5,
        "p": 1.9, "q": 0.1, "r": 6.0, "s": 6.3, "t": 9.1,
        "u": 2.8, "v": 1.0, "w": 2.4, "x": 0.15, "y": 2.0,
        "z": 0.07
    }

    if len(text) == 0:
        return float("inf")

    score = 0

    for letter in Vigenere2D.alphabet:
        observed_count = text.count(letter)
        expected_count = len(text) * english_frequencies[letter] / 100

        if expected_count > 0:
            score += ((observed_count - expected_count) ** 2) / expected_count

    return score

def score_full_plaintext(text):
    score = score_english_text(text)

    common_patterns = [
        "the", "this", "that", "ing", "ion", "ent", "and", "ere",
        "her", "ter", "est", "for", "ate", "his",
        "is", "to", "of", "in", "er", "en", "an", "re", "ed", "on",
        "es", "se", "th"
    ]

    for pattern in common_patterns:
        score -= len(pattern) * 20 * text.count(pattern)

    rare_letters = "qjzx"

    for letter in rare_letters:
        score += 2 * text.count(letter)

    return score


def find_best_caesar_key_for_stream(stream):
    best_key = 0
    best_score = float("inf")
    best_decryption = ""

    for key in range(26):
        decrypted_stream = ""

        for letter in stream:
            position = Vigenere2D.alphabet.index(letter)
            new_position = (position - key) % 26
            decrypted_stream += Vigenere2D.alphabet[new_position]

        score = score_english_text(decrypted_stream)

        if score < best_score:
            best_score = score
            best_key = key
            best_decryption = decrypted_stream

    return best_key, best_decryption, best_score


def find_top_caesar_keys_for_stream(stream, top_count=4):
    candidates = []

    for key in range(26):
        decrypted_stream = ""

        for letter in stream:
            position = Vigenere2D.alphabet.index(letter)
            new_position = (position - key) % 26
            decrypted_stream += Vigenere2D.alphabet[new_position]

        score = score_english_text(decrypted_stream)

        candidates.append((key, decrypted_stream, score))

    candidates.sort(key=lambda item: item[2])

    return candidates[:top_count]


def attack_2d_vigenere(cipher, ciphertext):
    streams = cipher.split_ciphertext_by_key_position(ciphertext)

    found_key_matrix = []

    for row_index, stream_row in enumerate(streams):
        found_key_row = []

        for column_index, stream in enumerate(stream_row):
            best_key, decrypted_stream, score = find_best_caesar_key_for_stream(stream)
            key_letter = Vigenere2D.alphabet[best_key]

            found_key_row.append(key_letter)

            print(f"Key position [{row_index}][{column_index}]")
            print(f"Stream: {stream}")
            print(f"Best key number: {best_key}")
            print(f"Best key letter: {key_letter}")
            print(f"Decrypted stream: {decrypted_stream}")
            print(f"Score: {score}")
            print()

        found_key_matrix.append(found_key_row)

    return found_key_matrix


def build_key_matrix_from_flat_key(flat_key, key_rows, key_columns):
    key_matrix = []
    index = 0

    for row_index in range(key_rows):
        row = []

        for column_index in range(key_columns):
            row.append(flat_key[index])
            index += 1

        key_matrix.append(row)

    return key_matrix


def attack_2d_vigenere_with_combinations(cipher, ciphertext, top_count=3):
    streams = cipher.split_ciphertext_by_key_position(ciphertext)

    key_rows = len(cipher._key_matrix)
    key_columns = len(cipher._key_matrix[0])

    all_candidates = []

    for row_index, stream_row in enumerate(streams):
        for column_index, stream in enumerate(stream_row):
            top_keys = find_top_caesar_keys_for_stream(stream, top_count)

            key_letters = []

            for key, decrypted_stream, score in top_keys:
                key_letter = Vigenere2D.alphabet[key]
                key_letters.append(key_letter)

            all_candidates.append(key_letters)

    best_key_matrix = None
    best_plaintext = ""
    best_score = float("inf")

    for candidate_combination in product(*all_candidates):
        candidate_key_matrix = build_key_matrix_from_flat_key(
            candidate_combination,
            key_rows,
            key_columns
        )

        candidate_cipher = Vigenere2D(candidate_key_matrix, cipher._columns)
        candidate_plaintext = candidate_cipher.decrypt(ciphertext)

        score = score_full_plaintext(candidate_plaintext)

        if score < best_score:
            best_score = score
            best_key_matrix = candidate_key_matrix
            best_plaintext = candidate_plaintext

    return best_key_matrix, best_plaintext, best_score


def print_matrix(title, matrix):
    print(title)

    for row in matrix:
        print(" ".join(row))

    print()


if __name__ == "__main__":
    key_matrix = [
        ["k", "e", "y"],
        ["m", "a", "t"],
        ["r", "i", "x"]
    ]

    columns = 4

    cipher = Vigenere2D(key_matrix, columns)

    plaintext = (
        "thisisaverylongenglishtextusedtotestthetwodimensionalvigenerecipher"
        "theattackworksbetterwhentheciphertextislongerbecauseletterfrequencies"
        "becomemorevisibleandtheprogramcanestimateeachkeyletterseparately"
        "thisisnotperfectbutitisagoodalgorithmicattackfordemonstration"
    )

    plaintext_matrix = cipher.text_to_matrix(plaintext)
    ciphertext = cipher.encrypt(plaintext)
    decrypted = cipher.decrypt(ciphertext)

    print("Original plaintext:")
    print(plaintext)
    print()

    print_matrix("Plaintext matrix:", plaintext_matrix)

    print("Ciphertext:")
    print(ciphertext)
    print()

    print("Decrypted text:")
    print(decrypted)
    print()

    print("Decryption successful:", decrypted.startswith(plaintext))
    print("---------------------")
    print()

    print("Simple attack:")
    found_key_matrix = attack_2d_vigenere(cipher, ciphertext)

    print_matrix("Original key matrix:", key_matrix)
    print_matrix("Found key matrix with simple attack:", found_key_matrix)

    found_cipher = Vigenere2D(found_key_matrix, columns)
    decrypted_with_found_key = found_cipher.decrypt(ciphertext)

    print("Decrypted with simple attack key:")
    print(decrypted_with_found_key)
    print()

    print("Simple attack successful:", decrypted_with_found_key.startswith(plaintext))
    print("---------------------")
    print()

    print("Attack with combinations:")
    found_key_matrix_2, found_plaintext_2, score_2 = attack_2d_vigenere_with_combinations(
        cipher,
        ciphertext,
        top_count=4
    )

    print_matrix("Found key matrix with combinations:", found_key_matrix_2)

    print("Decrypted with combination attack:")
    print(found_plaintext_2)
    print()

    print("Combination attack score:", score_2)
    print("Combination attack successful:", found_plaintext_2.startswith(plaintext))