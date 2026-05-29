def gcd(a, b):
    a = abs(a)
    b = abs(b)

    while b != 0:
        remainder = a % b
        a = b
        b = remainder

    return a


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0

    d, x1, y1 = extended_gcd(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return d, x, y


def modular_inverse(a, n):
    d, x, y = extended_gcd(a, n)

    if d != 1:
        raise ValueError("Key A is not invertible modulo n")

    return x % n


class AffineCipher:
    def __init__(self, key_a, key_b):
        self._modulus = 128
        self._keyA = key_a
        self._keyB = key_b

        if gcd(self._keyA, self._modulus) != 1:
            raise ValueError("key_a must be invertible modulo 128")

        self._inverseKeyA = modular_inverse(self._keyA, self._modulus)

    def affine_function(self, value):
        return (self._keyA * value + self._keyB) % self._modulus

    def inverse_affine_function(self, value):
        return (self._inverseKeyA * (value - self._keyB)) % self._modulus

    def encode(self, plaintext):
        ciphertext = ""

        for character in plaintext:
            plain_value = ord(character)
            cipher_value = self.affine_function(plain_value)
            cipher_character = chr(cipher_value)

            ciphertext += cipher_character

        return ciphertext

    def decode(self, ciphertext):
        plaintext = ""

        for character in ciphertext:
            cipher_value = ord(character)
            plain_value = self.inverse_affine_function(cipher_value)
            plain_character = chr(plain_value)

            plaintext += plain_character

        return plaintext


def text_to_hex(text):
    result = ""

    for character in text:
        result += format(ord(character), "02x")

    return result


if __name__ == "__main__":
    print("GCD tests")
    print("gcd(48, 18):", gcd(48, 18))
    print("gcd(5, 128):", gcd(5, 128))
    print("gcd(4, 128):", gcd(4, 128))
    print()

    print("Extended GCD test")
    d, x, y = extended_gcd(5, 128)
    print("d:", d)
    print("x:", x)
    print("y:", y)
    print("Check: 5*x + 128*y =", 5 * x + 128 * y)
    print()

    print("Modular inverse test")
    inverse = modular_inverse(5, 128)
    print("inverse of 5 modulo 128:", inverse)
    print("Check: (5 * inverse) % 128 =", (5 * inverse) % 128)
    print()

    print("Affine Cipher test")
    key_a = 5
    key_b = 8

    cipher = AffineCipher(key_a, key_b)

    plaintext = "Hello Affine Cipher!"

    encoded = cipher.encode(plaintext)
    decoded = cipher.decode(encoded)

    print("Key A:", key_a)
    print("Key B:", key_b)
    print("Inverse Key A:", cipher._inverseKeyA)
    print("Plaintext:", plaintext)
    print("Ciphertext hex:", text_to_hex(encoded))
    print("Decoded:", decoded)
    print("Successful:", decoded == plaintext)