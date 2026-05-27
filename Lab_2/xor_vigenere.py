class XORVigenere:
    def __init__(self, key):
        self._key = key

    def encrypt(self, text):
        result = ""

        for index, character in enumerate(text):
            key_character = self._key[index % len(self._key)]

            character_code = ord(character)
            key_code = ord(key_character)

            encrypted_code = character_code ^ key_code
            encrypted_character = chr(encrypted_code)

            result += encrypted_character

        return result

    def decrypt(self, text):
        result = ""

        for index, character in enumerate(text):
            key_character = self._key[index % len(self._key)]

            character_code = ord(character)
            key_code = ord(key_character)

            decrypted_code = character_code ^ key_code
            decrypted_character = chr(decrypted_code)

            result += decrypted_character

        return result


def text_to_hex(text):
    result = ""

    for character in text:
        result += format(ord(character), "02x")

    return result


def split_into_streams(text, key_length):
    streams = []

    for i in range(key_length):
        stream = ""

        for j in range(i, len(text), key_length):
            stream += text[j]

        streams.append(stream)

    return streams


def score_readable_text(text):
    common_characters = " etaoinshrdluETAOINSHRDLU"
    score = 0

    for character in text:
        if character in common_characters:
            score += 2
        elif character.isalpha():
            score += 1
        elif character.isdigit():
            score += 1
        elif character in ".,!?;:'\"-()":
            score += 1
        elif character == "\n":
            score += 0
        elif ord(character) < 32 or ord(character) > 126:
            score -= 5

    return score


def find_best_xor_key_for_stream(stream):
    best_key = 0
    best_score = -999999
    best_decryption = ""

    for key in range(256):
        decrypted = ""

        for character in stream:
            decrypted_character = chr(ord(character) ^ key)
            decrypted += decrypted_character

        score = score_readable_text(decrypted)

        if score > best_score:
            best_score = score
            best_key = key
            best_decryption = decrypted

    return best_key, best_decryption, best_score


def attack_xor_vigenere_known_key_length(ciphertext, key_length):
    streams = split_into_streams(ciphertext, key_length)

    found_key = ""

    for index, stream in enumerate(streams):
        best_key, decrypted_stream, score = find_best_xor_key_for_stream(stream)

        key_character = chr(best_key)
        found_key += key_character

        print("Stream", index)
        print("Best key:", best_key)
        print("Best key character:", key_character)
        print("Decrypted stream:", decrypted_stream)
        print("Score:", score)
        print()

    return found_key


if __name__ == "__main__":
    key = "cat"

    plaintext = (
        "this is a long english message used to test the xor vigenere attack "
        "the longer the plaintext is the better the statistical attack works "
        "because readable characters and common letters become more visible"
    )

    cipher = XORVigenere(key)

    ciphertext = cipher.encrypt(plaintext)
    decrypted = cipher.decrypt(ciphertext)

    print("Key:", key)
    print("Plaintext:", plaintext)
    print("Ciphertext hex:", text_to_hex(ciphertext))
    print()

    found_key = attack_xor_vigenere_known_key_length(ciphertext, len(key))

    print("Original key:", key)
    print("Found key:", found_key)

    found_cipher = XORVigenere(found_key)
    decrypted_with_found_key = found_cipher.decrypt(ciphertext)

    print("Decrypted with found key:", decrypted_with_found_key)
    print("Attack successful:", decrypted_with_found_key == plaintext)
    print()

    print("Decrypted:", decrypted)
    print("Decryption successful:", decrypted == plaintext)