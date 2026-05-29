# ============================================================
# Lab 7 – DES Cipher
# ============================================================
#
# DES = Data Encryption Standard
#
# It encrypts one block of 64 bits using a 64-bit key.
# Internally, DES generates 16 round keys of 48 bits.
#
# Main stages:
#   1. Generate 16 subkeys from the 64-bit key.
#   2. Apply the initial permutation to the plaintext block.
#   3. Run 16 Feistel rounds.
#   4. Apply the final permutation.
#
# This implementation is for educational purposes.
# DES is not secure today because the key space is too small.
# ============================================================


# ============================================================
# DES tables
# ============================================================

PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

EXPANSION = [
    32, 1, 2, 3, 4, 5, 4, 5,
    6, 7, 8, 9, 8, 9, 10, 11,
    12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21,
    22, 23, 24, 25, 24, 25, 26, 27,
    28, 29, 28, 29, 30, 31, 32, 1
]

SBOX = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

INITIAL_PERMUTATION = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

FINAL_PERMUTATION = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

PBOX = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

SHIFT_SCHEDULE = [
    1, 1, 2, 2,
    2, 2, 2, 2,
    1, 2, 2, 2,
    2, 2, 2, 1
]


# ============================================================
# Utility functions
# ============================================================

def permute(bits: str, table: list[int]) -> str:
    """
    Applies a permutation table to a bit string.
    DES tables are 1-indexed, so we use position - 1.
    """

    return "".join(bits[position - 1] for position in table)


def xor_bits(bits1: str, bits2: str) -> str:
    """
    XOR between two bit strings of equal length.
    """

    if len(bits1) != len(bits2):
        raise ValueError("The two bit strings must have the same length.")

    return "".join(str(int(a) ^ int(b)) for a, b in zip(bits1, bits2))


def left_shift(bits: str, number_of_shifts: int) -> str:
    """
    Circular left shift.
    """

    return bits[number_of_shifts:] + bits[:number_of_shifts]


def string2Bits(text: str) -> str:
    """
    Converts ASCII text to bits.
    One character = 8 bits.
    """

    bits = ""

    for character in text:
        value = ord(character)

        if value > 255:
            raise ValueError("Only ASCII / one-byte characters are supported.")

        bits += format(value, "08b")

    return bits


def bits2String(bits: str) -> str:
    """
    Converts bits back to ASCII text.
    """

    if len(bits) % 8 != 0:
        raise ValueError("The number of bits must be divisible by 8.")

    text = ""

    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        text += chr(int(byte, 2))

    return text


def hex2Bits(hex_text: str, expected_bits: int | None = None) -> str:
    """
    Converts hexadecimal text to bits.
    """

    clean_hex = hex_text.replace("0x", "").replace("0X", "").replace(" ", "")

    if clean_hex == "":
        raise ValueError("Empty hexadecimal string.")

    bits = bin(int(clean_hex, 16))[2:]
    bits = bits.zfill(len(clean_hex) * 4)

    if expected_bits is not None:
        if len(bits) > expected_bits:
            raise ValueError(f"Hex value is larger than {expected_bits} bits.")

        bits = bits.zfill(expected_bits)

    return bits


def bits2Hex(bits: str) -> str:
    """
    Converts bits to uppercase hexadecimal.
    """

    if len(bits) % 4 != 0:
        raise ValueError("The number of bits must be divisible by 4.")

    result = ""

    for i in range(0, len(bits), 4):
        nibble = bits[i:i + 4]
        result += format(int(nibble, 2), "X")

    return result


# ============================================================
# DES Cipher
# ============================================================

class DESCipher:
    """
    Educational DES implementation.

    The key is given as 16 hexadecimal digits = 64 bits.

    Example:
        key = 133457799BBCDFF1
    """

    def __init__(self, key_hex: str):
        self._key64 = hex2Bits(key_hex, expected_bits=64)
        self._round_keys = self.generate_keys()

    def generate_keys(self) -> list[str]:
        """
        Task 1:
        Generate the 16 DES round keys.

        Steps:
            1. Apply PC1: 64-bit key -> 56-bit key.
            2. Split into left and right halves of 28 bits.
            3. Apply circular shifts according to DES schedule.
            4. Apply PC2: 56-bit key -> 48-bit round key.
        """

        key56 = permute(self._key64, PC1)

        left = key56[:28]
        right = key56[28:]

        round_keys = []

        for shift in SHIFT_SCHEDULE:
            left = left_shift(left, shift)
            right = left_shift(right, shift)

            combined_key56 = left + right
            round_key48 = permute(combined_key56, PC2)

            round_keys.append(round_key48)

        return round_keys

    def f_function(self, right32: str, round_key48: str) -> str:
        """
        Task 2:
        DES F function.

        Steps:
            1. Expand right half from 32 bits to 48 bits.
            2. XOR with the 48-bit round key.
            3. Apply the 8 S-boxes:
                each 6-bit group becomes 4 bits.
            4. Apply the P-box permutation.
        """

        if len(right32) != 32:
            raise ValueError("right32 must have exactly 32 bits.")

        if len(round_key48) != 48:
            raise ValueError("round_key48 must have exactly 48 bits.")

        right48 = permute(right32, EXPANSION)
        xor_result48 = xor_bits(right48, round_key48)

        sbox_result32 = ""

        for box_index in range(8):
            start = box_index * 6
            block6 = xor_result48[start:start + 6]

            row = int(block6[0] + block6[5], 2)
            column = int(block6[1:5], 2)

            value = SBOX[box_index][row][column]
            block4 = format(value, "04b")

            sbox_result32 += block4

        final32 = permute(sbox_result32, PBOX)

        return final32

    def _process_block(self, block64: str, round_keys: list[str]) -> str:
        """
        Common DES block processing.

        Encryption uses round keys in normal order.
        Decryption uses round keys in reverse order.
        """

        if len(block64) != 64:
            raise ValueError("DES works with blocks of exactly 64 bits.")

        permuted_block = permute(block64, INITIAL_PERMUTATION)

        left = permuted_block[:32]
        right = permuted_block[32:]

        for round_key in round_keys:
            new_left = right
            f_result = self.f_function(right, round_key)
            new_right = xor_bits(left, f_result)

            left = new_left
            right = new_right

        # DES swaps the two halves before the final permutation.
        pre_output = right + left

        result64 = permute(pre_output, FINAL_PERMUTATION)

        return result64

    def encrypt_block_bits(self, plaintext64: str) -> str:
        """
        Task 3:
        Encrypt one 64-bit block.
        """

        return self._process_block(plaintext64, self._round_keys)

    def decrypt_block_bits(self, ciphertext64: str) -> str:
        """
        Task 4:
        Decrypt one 64-bit block.
        """

        reversed_keys = list(reversed(self._round_keys))
        return self._process_block(ciphertext64, reversed_keys)

    def encrypt_hex_block(self, plaintext_hex: str) -> str:
        """
        Encrypt one 64-bit block written as 16 hexadecimal digits.
        """

        plaintext_bits = hex2Bits(plaintext_hex, expected_bits=64)
        ciphertext_bits = self.encrypt_block_bits(plaintext_bits)

        return bits2Hex(ciphertext_bits)

    def decrypt_hex_block(self, ciphertext_hex: str) -> str:
        """
        Decrypt one 64-bit block written as 16 hexadecimal digits.
        """

        ciphertext_bits = hex2Bits(ciphertext_hex, expected_bits=64)
        plaintext_bits = self.decrypt_block_bits(ciphertext_bits)

        return bits2Hex(plaintext_bits)

    def encrypt_text_block_to_hex(self, plaintext: str) -> str:
        """
        Encrypt exactly 8 ASCII characters and return ciphertext in hex.
        """

        if len(plaintext) != 8:
            raise ValueError("DES text block must contain exactly 8 characters.")

        plaintext_bits = string2Bits(plaintext)
        ciphertext_bits = self.encrypt_block_bits(plaintext_bits)

        return bits2Hex(ciphertext_bits)

    def decrypt_hex_block_to_text(self, ciphertext_hex: str) -> str:
        """
        Decrypt one 64-bit hex block and return ASCII text.
        """

        ciphertext_bits = hex2Bits(ciphertext_hex, expected_bits=64)
        plaintext_bits = self.decrypt_block_bits(ciphertext_bits)

        return bits2String(plaintext_bits)

    @property
    def round_keys(self) -> list[str]:
        """
        Returns the 16 generated round keys.
        """

        return self._round_keys


# ============================================================
# Demo / Testing
# ============================================================

def demo_known_des_test_vector() -> None:
    """
    Standard DES test vector.

    Key:
        133457799BBCDFF1

    Plaintext:
        0123456789ABCDEF

    Expected ciphertext:
        85E813540F0AB405
    """

    print("=== DES known test vector ===")

    key_hex = "133457799BBCDFF1"
    plaintext_hex = "0123456789ABCDEF"
    expected_cipher_hex = "85E813540F0AB405"

    des = DESCipher(key_hex)

    ciphertext_hex = des.encrypt_hex_block(plaintext_hex)
    decrypted_hex = des.decrypt_hex_block(ciphertext_hex)

    print(f"Key:                 {key_hex}")
    print(f"Plaintext hex:       {plaintext_hex}")
    print(f"Ciphertext hex:      {ciphertext_hex}")
    print(f"Expected ciphertext: {expected_cipher_hex}")
    print(f"Decrypted hex:       {decrypted_hex}")

    if ciphertext_hex == expected_cipher_hex and decrypted_hex == plaintext_hex:
        print("Test result: SUCCESS")
    else:
        print("Test result: FAILED")

    print()


def demo_text_block() -> None:
    """
    Text example.
    DES works on 8-character blocks because:
        8 characters * 8 bits = 64 bits.
    """

    print("=== DES text block demo ===")

    key_hex = "133457799BBCDFF1"
    plaintext = "unitbv!!"

    des = DESCipher(key_hex)

    ciphertext_hex = des.encrypt_text_block_to_hex(plaintext)
    decrypted_text = des.decrypt_hex_block_to_text(ciphertext_hex)

    print(f"Key:            {key_hex}")
    print(f"Plaintext:      {plaintext}")
    print(f"Ciphertext hex: {ciphertext_hex}")
    print(f"Decrypted text: {decrypted_text}")
    print()


def demo_round_keys() -> None:
    """
    Prints the 16 round keys generated by DES.
    """

    print("=== DES round keys ===")

    key_hex = "133457799BBCDFF1"
    des = DESCipher(key_hex)

    for index, round_key in enumerate(des.round_keys, start=1):
        print(f"K{index:02d}: {round_key}")

    print()


def main() -> None:
    demo_known_des_test_vector()
    demo_text_block()
    demo_round_keys()


if __name__ == "__main__":
    main()