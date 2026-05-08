class XORCipher:
    def __init__(self, key):
        self._key = key

    def encrypt(self, text):
        result = ""
        print("Plaintext: ",text)

        for ch in text:
            print("ch = ", ch)
            x = ord(ch)
            print("unicode = ",x)
            encrypted_number = x ^ self._key
            print("encrypted number = ", encrypted_number)
            encrypted_char = chr(encrypted_number)
            print("encrypted char = ", encrypted_char)
            result += encrypted_char
            print("partial result = ", result)
            print("--------")
        return result
    
    def decrypt(self, text):
        result = ""
        print("Ciphertext: ", text)

        for ch in text:
            print("ch = ", ch)
            x = ord(ch)
            print("unicode = ", x)
            # Nu există +key sau -key // XOR cu aceeași cheie
            decrypted_number = x ^ self._key
            print("decrypted number = ", decrypted_number)
            decrypted_char = chr(decrypted_number)
            print("decrypted char = ", decrypted_char)
            result += decrypted_char
            print("partial result = ", result)
            print("--------")
        return result
    
def attack(ciphertext):
    for key in range(256):
        cipher = XORCipher(key)
        plaintext = cipher.decrypt(ciphertext)
        print(key, "-->", plaintext)
    
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