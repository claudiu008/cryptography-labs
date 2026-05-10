class XORCipher:
    def __init__(self, key):
        self._key = key

    def encrypt(self, text):
        result = ""
     
        for character in text:
            character_code = ord(character)
            encrypted_code = character_code ^ self._key
            encrypted_character = chr(encrypted_code)
            result += encrypted_character
        return result
    
    def decrypt(self, text):
        result = ""
    
        for character in text:
            character_code = ord(character)
            # Nu există +key sau -key // XOR cu aceeași cheie
            decrypted_code = character_code ^ self._key
            decrypted_character = chr(decrypted_code)
            result += decrypted_character
        return result
    
def attack(ciphertext):
    for key in range(256):
        cipher = XORCipher(key)
        possible_plaintext = cipher.decrypt(ciphertext)
        print(f"{key}: --> {possible_plaintext}")
    
cipher = XORCipher(10)
encrypted = cipher.encrypt("Hi!")
print("Encrypted: ", encrypted)
print("--------")

decrypted = cipher.decrypt(encrypted)
print("Decrypted: ", decrypted)
print("--------")

print("Attack results: ")
attack(encrypted)

# The security of the XOR cipher can be increased by using a longer key instead of a single byte, ideally a key with the same length as the message (one-time pad). The key should be random and must not be reused. Using pseudorandom key streams (stream ciphers) also improves security. A single-byte key is insecure due to the small key space, which allows brute-force attacks.