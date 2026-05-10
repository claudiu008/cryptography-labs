class Vigenere:
    alphabet = "abcdefghijklmnopqrstuvwyxz"

    def __init__(self, key):
        self._key = key
    
    def encrypt(self, text):
        result = ""

        for i in range(len(text)):
            ch = text[i]
            print("plaintext character = ", ch)

            if ch in self.alphabet:
                position = self.alphabet.index(ch)
                print("alphabet position = ", position)
                key_char = self._key[i % len(self._key)]
                print("key character = ", key_char)
                key_position = self.alphabet.index(key_char)
                print("key position = ", key_position)
                new_position = (position + key_position) % 26
                print("Vigenere shift = ",new_position)
                new_char = self.alphabet[new_position]
                print("encrypted character = ", new_char)
                result += new_char
                print("partial result = ", result)
                print("-----------")
            else:
                result += ch
                print("-----------")

        return result
    
    def decrypt(self, text):
        result = ""

        for i in range(len(text)):
            ch = text[i]

            if ch in self.alphabet:
                position = self.alphabet.index(ch)
                key_char = self._key[i % len(self._key)]
                key_position = self.alphabet.index(key_char)
                new_position = (position - key_position) % 26
                new_char = self.alphabet[new_position]
                result += new_char
            else:
                result += ch

        return result
    
    def attack(ciphertext):
        pass

cipher = Vigenere("red")
print("key =", cipher._key)
print("-----------")
encrypted = cipher.encrypt("hellow world!")
print("Encrypted:",encrypted)
print("-----------")
decrypted = cipher.decrypt(encrypted)
print("Decrypted:", decrypted)