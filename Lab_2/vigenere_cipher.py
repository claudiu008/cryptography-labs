class Vigenere:
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self, key):
        self._key = key

    def encrypt(self, text):
        result = ""
        key_index = 0

        for letter in text:
            if letter in self.alphabet:
                letter_position = self.alphabet.index(letter)

                key_letter = self._key[key_index % len(self._key)]
                key_position = self.alphabet.index(key_letter)

                new_position = (letter_position + key_position) % 26
                new_letter = self.alphabet[new_position]

                result += new_letter
                key_index += 1
            else:
                result += letter

        return result

    def decrypt(self, text):
        result = ""
        key_index = 0

        for letter in text:
            if letter in self.alphabet:
                letter_position = self.alphabet.index(letter)

                key_letter = self._key[key_index % len(self._key)]
                key_position = self.alphabet.index(key_letter)

                new_position = (letter_position - key_position) % 26
                new_letter = self.alphabet[new_position]

                result += new_letter
                key_index += 1
            else:
                result += letter

        return result


def split_into_streams(ciphertext, key_length):
    streams = []

    for i in range(key_length):
        stream = ""

        for j in range(i, len(ciphertext), key_length):
            if ciphertext[j] in Vigenere.alphabet:
                stream += ciphertext[j]

        streams.append(stream)

    return streams


def score_english_text(text):
    common_letters = "etaoinshr"
    score = 0

    for letter in text:
        if letter in common_letters:
            score += 1

    return score


def find_best_caesar_key_for_stream(stream):
    best_key = 0
    best_score = -1
    best_decryption = ""

    for key in range(26):
        decrypted_stream = ""

        for letter in stream:
            position = Vigenere.alphabet.index(letter)
            new_position = (position - key) % 26
            decrypted_stream += Vigenere.alphabet[new_position]

        score = score_english_text(decrypted_stream)

        if score > best_score:
            best_score = score
            best_key = key
            best_decryption = decrypted_stream

    return best_key, best_decryption, best_score


def attack_vigenere_known_key_length(ciphertext, key_length):
    streams = split_into_streams(ciphertext, key_length)

    found_key = ""

    for index, stream in enumerate(streams):
        best_key, decrypted_stream, score = find_best_caesar_key_for_stream(stream)

        key_letter = Vigenere.alphabet[best_key]
        found_key += key_letter

        print(f"Stream {index}")
        print(f"Best key number: {best_key}")
        print(f"Best key letter: {key_letter}")
        print(f"Decrypted stream: {decrypted_stream}")
        print(f"Score: {score}")
        print()

    return found_key


if __name__ == "__main__":
    cipher = Vigenere("dog")

    plaintext = (
        "thisisaverylongenglishtextandweuseittotestthevigenereattack"
        "thelongerthetextisthebetterthestatisticalattackworks"
        "becauseletterfrequenciesbecomemorevisibleintheciphertext"
    )

    ciphertext = cipher.encrypt(plaintext)

    print("Plaintext:", plaintext)
    print("Ciphertext:", ciphertext)
    print("-----------")

    found_key = attack_vigenere_known_key_length(ciphertext, 3)

    print("Found key:", found_key)

    decrypted = Vigenere(found_key).decrypt(ciphertext)
    print("Decrypted:", decrypted)