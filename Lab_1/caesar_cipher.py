class CaesarCipher:
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self, key):
        self._key = key

    def encrypt(self, text):
        result = ""

        for letter in text:
            if letter in self.alphabet:
                position = self.alphabet.index(letter)
                new_position = (position + self._key) % 26
                new_letter = self.alphabet[new_position]
                result += new_letter
            else:
                result += letter
        return result

    def decrypt(self, text):
        result = ""

        for letter in text:
            if letter in self.alphabet:
                position = self.alphabet.index(letter)
                new_position = (position - self._key) % 26
                new_letter = self.alphabet[new_position]
                result += new_letter
            else:
                result += letter
        return result

def attack(ciphertext):
    for key in range(26):
        cipher = CaesarCipher(key)
        possible_plaintext = cipher.decrypt(ciphertext)
        print(f"Key {key}: --> {possible_plaintext}")

cipher = CaesarCipher(3)

encrypted = cipher.encrypt("hello world!")
print("Encrypted 'hello world!':", encrypted)

decrypted = cipher.decrypt(encrypted)
print("Decrypted ciphertext:", decrypted)

print("Attack results: ")
attack(encrypted)

# The security of the Caesar cipher can be slightly improved by increasing the size of the alphabet and by using multiple keys (e.g., the Vigenère cipher). Removing spaces and language structure can also make attacks more difficult. However, the cipher remains fundamentally insecure due to its very small key space, which allows efficient brute-force attacks.