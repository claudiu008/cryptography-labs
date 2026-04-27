class CaesarCipher:
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self,key):
        self._key = key

    def encrypt(self, text):
        result = ''

        for char in text.lower():
            if char in self.alphabet:
                position = self.alphabet.index(char)
                new_position = (position + self._key) % len(self.alphabet)
                new_char = self.alphabet[new_position]
                result += new_char.upper()
            else:
                result += char

        return result

    def decrypt(self, text):
        result = ''

        for char in text:
            char = char.lower()

            if char in self.alphabet:
                position = self.alphabet.index(char)
                new_position = (position - self._key) % len(self.alphabet)
                result += self.alphabet[new_position]
            else:
                result += char

        return result


def attack(ciphertext):
    for key in range(len(CaesarCipher.alphabet)):
        cipher = CaesarCipher(key)
        decrypted = cipher.decrypt(ciphertext)
        print(f'Key: {key}, Decrypted: {decrypted}')    
   
    
cipher = CaesarCipher(3)

encrypted = cipher.encrypt('hello world!')
print(f'Encrypted: {encrypted}')

decrypted = cipher.decrypt(encrypted)
print(f'Decrypted: {decrypted}')

print("Attack results:")
attack(encrypted)