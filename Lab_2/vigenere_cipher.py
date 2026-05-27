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

def index_of_coincidence(text):
    n = len(text)

    if n <= 1:
        return 0

    total = 0

    for letter in Vigenere.alphabet:
        count = text.count(letter)
        total += count * (count - 1)

    return total / (n * (n - 1))

def find_key_length(ciphertext, max_key_length):
    best_key_length = 1
    best_score = 0

    for key_length in range(1, max_key_length + 1):
        streams = split_into_streams(ciphertext, key_length)

        total_ic = 0

        for stream in streams:
            total_ic += index_of_coincidence(stream)

        average_ic = total_ic / key_length

        print(f"Key length {key_length}: IC = {average_ic}")

        if average_ic > best_score:
            best_score = average_ic
            best_key_length = key_length

    return best_key_length

if __name__ == "__main__":
    key = "cryptographyxx"  # 14 characters

    plaintext = (
        "thisisaverylongenglishtextusedtotestthevigenerecipher"
        "theattackworksbetterwhentheciphertextislongerbecause"
        "letterfrequenciesbecomemorevisible"
    )

    cipher = Vigenere(key)

    ciphertext = cipher.encrypt(plaintext)
    decrypted = cipher.decrypt(ciphertext)

    print("Key:", key)
    print("Key length:", len(key))
    print("Plaintext:", plaintext)
    print("Ciphertext:", ciphertext)
    print()
    print("Trying to find key length...")
    found_key_length = find_key_length(ciphertext, 20)
    print("Found key length:", found_key_length)
    print()
    print("Decrypted:", decrypted)
    print("Decryption successful:", decrypted == plaintext)