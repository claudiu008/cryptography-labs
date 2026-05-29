import random


# ============================================================
# Lab 6 – Pseudo One Time Pad Cipher
# ============================================================
#
# Idea:
#   Classical One-Time Pad needs a key as long as the message.
#   Pseudo One-Time Pad uses a short seed and expands it with
#   a pseudo-random sequence generator.
#
#   ciphertext_bits = plaintext_bits XOR pseudo_key_bits
#
# In this lab, the pseudo-random sequence generator is based
# on the Hamming expansion.
# ============================================================


# ============================================================
# Utility functions
# ============================================================

def string2Bits(text: str) -> str:
    """
    Converts a string into a sequence of bits.

    Example:
        'A' -> 01000001
    """

    bits = ""

    for character in text:
        character_bits = bin(ord(character))[2:]
        character_bits = "0" * (8 - len(character_bits)) + character_bits
        bits += character_bits

    return bits


def bits2String(bits: str) -> str:
    """
    Converts a sequence of bits into a string.

    The number of bits must be divisible by 8.
    """

    if len(bits) % 8 != 0:
        raise ValueError("The number of bits must be divisible by 8.")

    text = ""

    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        character = chr(int(byte, 2))
        text += character

    return text


def bits2Hex(bits: str) -> str:
    """
    Converts bits to hexadecimal.
    Useful because encrypted text may contain non-printable characters.
    """

    if len(bits) % 8 != 0:
        raise ValueError("The number of bits must be divisible by 8.")

    result = ""

    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        result += format(int(byte, 2), "02x")

    return result


def hex2Bits(hex_text: str) -> str:
    """
    Converts hexadecimal text back to bits.
    """

    bits = ""

    for i in range(0, len(hex_text), 2):
        hex_byte = hex_text[i:i + 2]
        bits += format(int(hex_byte, 16), "08b")

    return bits


def xor_bits(bits1: str, bits2: str) -> str:
    """
    XOR between two bit strings of equal length.
    """

    if len(bits1) != len(bits2):
        raise ValueError("Bit strings must have the same length.")

    result = ""

    for bit1, bit2 in zip(bits1, bits2):
        result += str(int(bit1) ^ int(bit2))

    return result


def minimum_n_for_bits(number_of_bits: int) -> int:
    """
    Finds the minimum n such that:

        2**n - 1 >= number_of_bits

    Because the Hamming expansion generates 2**n - 1 bits.
    """

    n = 1

    while (2 ** n - 1) < number_of_bits:
        n += 1

    return n


# ============================================================
# Task 1 – PRSG Hamming
# ============================================================

class PRSGHamming:
    """
    Pseudo Random Sequence Generator based on Hamming expansion.

    For a seed x with n bits, the generator produces 2**n - 1 bits.

    For every j from 1 to 2**n - 1:
        compute j & x
        count how many 1 bits are in the result
        if the count is odd, output 1
        otherwise, output 0
    """

    def __init__(self, n: int):
        if n <= 0:
            raise ValueError("n must be greater than 0.")

        self._n = n

    def G(self, x: int) -> str:
        """
        Expands seed x into a longer pseudo-random bit sequence.
        """

        if x < 0:
            raise ValueError("Seed x must be non-negative.")

        # Keep only n bits from x.
        x = x % (2 ** self._n)

        generated_bits = ""

        for j in range(1, 2 ** self._n):
            # j & x keeps only the common 1 bits between j and x.
            common_bits = j & x

            # Convert to binary and count the number of 1 bits.
            ones_count = bin(common_bits).count("1")

            # Hamming rule: odd number of 1 bits -> 1, even -> 0.
            if ones_count % 2 == 1:
                generated_bits += "1"
            else:
                generated_bits += "0"

        return generated_bits

    def random_seed(self) -> int:
        """
        Generates a random seed with n bits.
        """

        return random.randint(1, 2 ** self._n - 1)

    def generate(self) -> tuple[int, str]:
        """
        Generates a random seed and expands it.

        Returns:
            seed, expanded_bits
        """

        seed = self.random_seed()
        expanded_bits = self.G(seed)

        return seed, expanded_bits


# ============================================================
# Task 2 – Pseudo One Time Pad Cipher
# ============================================================

class PseudoOneTimePadCipher:
    """
    Pseudo One-Time Pad Cipher using PRSGHamming.

    Encryption:
        1. Convert plaintext to bits.
        2. Generate pseudo-random key bits with PRSGHamming.
        3. Crop the key to the plaintext length.
        4. XOR plaintext bits with key bits.
        5. Return ciphertext.

    Decryption:
        Same operation, because XOR reverses itself.
    """

    def __init__(self, n: int | None = None, seed: int | None = None):
        self._n = n
        self._seed = seed

    def _prepare_generator(self, number_of_bits: int) -> PRSGHamming:
        """
        Creates the Hamming generator.

        If n is not given, it is automatically calibrated so that:
            2**n - 1 >= number_of_bits
        """

        if self._n is None:
            self._n = minimum_n_for_bits(number_of_bits)

        if (2 ** self._n - 1) < number_of_bits:
            self._n = minimum_n_for_bits(number_of_bits)

        return PRSGHamming(self._n)

    def _prepare_seed(self, generator: PRSGHamming) -> int:
        """
        Uses the existing seed or generates a new one.
        """

        if self._seed is None:
            self._seed = generator.random_seed()

        return self._seed

    def _generate_key_bits(self, number_of_bits: int) -> str:
        """
        Generates and crops the pseudo-random key bits.
        """

        generator = self._prepare_generator(number_of_bits)
        seed = self._prepare_seed(generator)

        key_bits = generator.G(seed)

        return key_bits[:number_of_bits]

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypts plaintext and returns ciphertext as a string.

        Warning:
            The ciphertext may contain non-printable characters.
            For display, use encrypt_to_hex().
        """

        plaintext_bits = string2Bits(plaintext)
        key_bits = self._generate_key_bits(len(plaintext_bits))

        cipher_bits = xor_bits(plaintext_bits, key_bits)
        ciphertext = bits2String(cipher_bits)

        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypts ciphertext produced by encrypt().
        """

        ciphertext_bits = string2Bits(ciphertext)
        key_bits = self._generate_key_bits(len(ciphertext_bits))

        plaintext_bits = xor_bits(ciphertext_bits, key_bits)
        plaintext = bits2String(plaintext_bits)

        return plaintext

    def encrypt_to_hex(self, plaintext: str) -> str:
        """
        Encrypts plaintext and returns ciphertext in hexadecimal format.
        This is safer for printing and saving.
        """

        plaintext_bits = string2Bits(plaintext)
        key_bits = self._generate_key_bits(len(plaintext_bits))

        cipher_bits = xor_bits(plaintext_bits, key_bits)
        cipher_hex = bits2Hex(cipher_bits)

        return cipher_hex

    def decrypt_from_hex(self, cipher_hex: str) -> str:
        """
        Decrypts ciphertext from hexadecimal format.
        """

        cipher_bits = hex2Bits(cipher_hex)
        key_bits = self._generate_key_bits(len(cipher_bits))

        plaintext_bits = xor_bits(cipher_bits, key_bits)
        plaintext = bits2String(plaintext_bits)

        return plaintext

    @property
    def n(self) -> int:
        return self._n

    @property
    def seed(self) -> int:
        return self._seed


# ============================================================
# Demo / Testing
# ============================================================

def demo_prsg_hamming() -> None:
    print("=== Task 1: PRSG Hamming ===")

    n = 4
    seed = 9

    generator = PRSGHamming(n)
    expanded_bits = generator.G(seed)

    print(f"n = {n}")
    print(f"seed = {seed}")
    print(f"Generated bits length = {len(expanded_bits)}")
    print(f"Generated bits = {expanded_bits}")
    print()


def demo_pseudo_one_time_pad() -> None:
    print("=== Task 2: Pseudo One Time Pad ===")

    plaintext = "hello cryptography"

    # We can give n and seed manually.
    # n must be large enough to generate at least len(plaintext_bits) bits.
    plaintext_bits = string2Bits(plaintext)
    n = minimum_n_for_bits(len(plaintext_bits))
    seed = 12345

    cipher = PseudoOneTimePadCipher(n=n, seed=seed)

    cipher_hex = cipher.encrypt_to_hex(plaintext)
    decrypted_text = cipher.decrypt_from_hex(cipher_hex)

    print(f"Plaintext: {plaintext}")
    print(f"Plaintext bits length: {len(plaintext_bits)}")
    print(f"n used: {cipher.n}")
    print(f"seed used: {cipher.seed}")
    print(f"Ciphertext hex: {cipher_hex}")
    print(f"Decrypted text: {decrypted_text}")
    print()


def demo_auto_n_and_seed() -> None:
    print("=== Automatic n and seed example ===")

    plaintext = "unitbv"

    cipher = PseudoOneTimePadCipher()

    cipher_hex = cipher.encrypt_to_hex(plaintext)

    # For decryption, we must use the same n and the same seed.
    decipher = PseudoOneTimePadCipher(n=cipher.n, seed=cipher.seed)
    decrypted_text = decipher.decrypt_from_hex(cipher_hex)

    print(f"Plaintext: {plaintext}")
    print(f"n automatically chosen: {cipher.n}")
    print(f"seed automatically chosen: {cipher.seed}")
    print(f"Ciphertext hex: {cipher_hex}")
    print(f"Decrypted text: {decrypted_text}")
    print()


def main() -> None:
    demo_prsg_hamming()
    demo_pseudo_one_time_pad()
    demo_auto_n_and_seed()


if __name__ == "__main__":
    main()