import os
import sys
from pathlib import Path


# ============================================================
# Assignment – 3DES with CBC Mode
# ============================================================
#
# Requirements:
#   1) DES3Cipher class with init, encrypt and decrypt methods.
#      It works on 64-bit blocks.
#
#   2) One mode of operation for any length plaintext/ciphertext.
#      I implemented CBC mode.
#
# This file uses the DES implementation from Lab_7/des_cipher.py.
# Run from project root:
#
#   python .\Assignments\des3_cbc_assignment.py
# ============================================================


# Make sure Python can import Lab_7/des_cipher.py
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Lab_7.des_cipher import DESCipher, xor_bits, bits2Hex, hex2Bits


# ============================================================
# Utility functions
# ============================================================

BLOCK_SIZE_BYTES = 8
BLOCK_SIZE_BITS = 64


def bytes_to_bits(data: bytes) -> str:
    """
    Converts bytes to a bit string.
    """

    return "".join(format(byte, "08b") for byte in data)


def bits_to_bytes(bits: str) -> bytes:
    """
    Converts a bit string to bytes.
    """

    if len(bits) % 8 != 0:
        raise ValueError("The number of bits must be divisible by 8.")

    result = bytearray()

    for i in range(0, len(bits), 8):
        result.append(int(bits[i:i + 8], 2))

    return bytes(result)


def split_blocks(data: bytes, block_size: int = BLOCK_SIZE_BYTES) -> list[bytes]:
    """
    Splits data into blocks of block_size bytes.
    """

    return [
        data[i:i + block_size]
        for i in range(0, len(data), block_size)
    ]


def pkcs7_pad(data: bytes, block_size: int = BLOCK_SIZE_BYTES) -> bytes:
    """
    Adds PKCS#7 padding.

    DES has 8-byte blocks.
    If the plaintext is already a multiple of 8 bytes,
    a full block of padding is added.
    """

    padding_length = block_size - (len(data) % block_size)

    if padding_length == 0:
        padding_length = block_size

    padding = bytes([padding_length]) * padding_length

    return data + padding


def pkcs7_unpad(data: bytes, block_size: int = BLOCK_SIZE_BYTES) -> bytes:
    """
    Removes PKCS#7 padding.
    """

    if not data:
        raise ValueError("Cannot unpad empty data.")

    padding_length = data[-1]

    if padding_length < 1 or padding_length > block_size:
        raise ValueError("Invalid padding length.")

    expected_padding = bytes([padding_length]) * padding_length

    if data[-padding_length:] != expected_padding:
        raise ValueError("Invalid PKCS#7 padding.")

    return data[:-padding_length]


def clean_hex(hex_text: str) -> str:
    """
    Cleans a hexadecimal string.
    """

    return hex_text.replace("0x", "").replace("0X", "").replace(" ", "").replace("\n", "")


# ============================================================
# Task 1 – DES3Cipher
# ============================================================

class DES3Cipher:
    """
    3DES block cipher.

    This class works only on 64-bit blocks.

    I use the common EDE construction:

        Encryption:
            C = E_K3(D_K2(E_K1(P)))

        Decryption:
            P = D_K1(E_K2(D_K3(C)))

    Where:
        E = DES encryption
        D = DES decryption

    The keys are written as 16 hexadecimal digits each.
    16 hex digits = 64 bits.
    """

    def __init__(self, key1_hex: str, key2_hex: str, key3_hex: str):
        self._des1 = DESCipher(key1_hex)
        self._des2 = DESCipher(key2_hex)
        self._des3 = DESCipher(key3_hex)

    def encrypt(self, plaintext64_bits: str) -> str:
        """
        Encrypts one 64-bit block.

        Input:
            plaintext64_bits – string of exactly 64 bits

        Output:
            ciphertext64_bits – string of exactly 64 bits
        """

        if len(plaintext64_bits) != BLOCK_SIZE_BITS:
            raise ValueError("3DES encrypt works with exactly 64 bits.")

        step1 = self._des1.encrypt_block_bits(plaintext64_bits)
        step2 = self._des2.decrypt_block_bits(step1)
        step3 = self._des3.encrypt_block_bits(step2)

        return step3

    def decrypt(self, ciphertext64_bits: str) -> str:
        """
        Decrypts one 64-bit block.

        Input:
            ciphertext64_bits – string of exactly 64 bits

        Output:
            plaintext64_bits – string of exactly 64 bits
        """

        if len(ciphertext64_bits) != BLOCK_SIZE_BITS:
            raise ValueError("3DES decrypt works with exactly 64 bits.")

        step1 = self._des3.decrypt_block_bits(ciphertext64_bits)
        step2 = self._des2.encrypt_block_bits(step1)
        step3 = self._des1.decrypt_block_bits(step2)

        return step3

    def encrypt_hex_block(self, plaintext_hex: str) -> str:
        """
        Encrypts one 64-bit block written as 16 hex digits.
        """

        plaintext_bits = hex2Bits(plaintext_hex, expected_bits=64)
        ciphertext_bits = self.encrypt(plaintext_bits)

        return bits2Hex(ciphertext_bits)

    def decrypt_hex_block(self, ciphertext_hex: str) -> str:
        """
        Decrypts one 64-bit block written as 16 hex digits.
        """

        ciphertext_bits = hex2Bits(ciphertext_hex, expected_bits=64)
        plaintext_bits = self.decrypt(ciphertext_bits)

        return bits2Hex(plaintext_bits)


# Alias included because the assignment text says "DES3Chiper"
DES3Chiper = DES3Cipher


# ============================================================
# Task 2 – CBC mode for any length plaintext/ciphertext
# ============================================================

class DES3CBCMode:
    """
    CBC mode using DES3Cipher.

    CBC encryption:

        C0 = IV
        Ci = E_K(Pi XOR C(i-1))

    CBC decryption:

        Pi = D_K(Ci) XOR C(i-1)

    The encryption method returns:
        IV || ciphertext

    in hexadecimal format.
    """

    def __init__(self, key1_hex: str, key2_hex: str, key3_hex: str, iv_hex: str | None = None):
        self._cipher = DES3Cipher(key1_hex, key2_hex, key3_hex)

        if iv_hex is None:
            self._iv = os.urandom(BLOCK_SIZE_BYTES)
        else:
            iv_clean = clean_hex(iv_hex)

            if len(iv_clean) != 16:
                raise ValueError("IV must have exactly 16 hex digits = 64 bits.")

            self._iv = bytes.fromhex(iv_clean)

    def encrypt_bytes(self, plaintext: bytes) -> str:
        """
        Encrypts any length plaintext bytes using 3DES-CBC.

        Returns:
            hexadecimal string containing IV || ciphertext
        """

        padded_plaintext = pkcs7_pad(plaintext)
        plaintext_blocks = split_blocks(padded_plaintext)

        previous_block_bits = bytes_to_bits(self._iv)
        ciphertext = bytearray()

        for plaintext_block in plaintext_blocks:
            plaintext_block_bits = bytes_to_bits(plaintext_block)

            mixed_bits = xor_bits(plaintext_block_bits, previous_block_bits)
            ciphertext_block_bits = self._cipher.encrypt(mixed_bits)
            ciphertext_block_bytes = bits_to_bytes(ciphertext_block_bits)

            ciphertext.extend(ciphertext_block_bytes)

            previous_block_bits = ciphertext_block_bits

        final_result = self._iv + bytes(ciphertext)

        return final_result.hex().upper()

    def decrypt_bytes(self, ciphertext_hex: str) -> bytes:
        """
        Decrypts a hexadecimal ciphertext produced by encrypt_bytes().

        The first 8 bytes are interpreted as the IV.
        """

        ciphertext_clean = clean_hex(ciphertext_hex)
        raw_data = bytes.fromhex(ciphertext_clean)

        if len(raw_data) < BLOCK_SIZE_BYTES * 2:
            raise ValueError("Ciphertext must contain IV and at least one ciphertext block.")

        if len(raw_data) % BLOCK_SIZE_BYTES != 0:
            raise ValueError("Ciphertext length must be a multiple of 8 bytes.")

        iv = raw_data[:BLOCK_SIZE_BYTES]
        ciphertext = raw_data[BLOCK_SIZE_BYTES:]

        ciphertext_blocks = split_blocks(ciphertext)

        previous_block_bits = bytes_to_bits(iv)
        plaintext_padded = bytearray()

        for ciphertext_block in ciphertext_blocks:
            ciphertext_block_bits = bytes_to_bits(ciphertext_block)

            decrypted_block_bits = self._cipher.decrypt(ciphertext_block_bits)
            plaintext_block_bits = xor_bits(decrypted_block_bits, previous_block_bits)
            plaintext_block_bytes = bits_to_bytes(plaintext_block_bits)

            plaintext_padded.extend(plaintext_block_bytes)

            previous_block_bits = ciphertext_block_bits

        plaintext = pkcs7_unpad(bytes(plaintext_padded))

        return plaintext

    def encrypt_text(self, plaintext: str) -> str:
        """
        Encrypts any length text using UTF-8.
        Returns IV || ciphertext as hex.
        """

        return self.encrypt_bytes(plaintext.encode("utf-8"))

    def decrypt_text(self, ciphertext_hex: str) -> str:
        """
        Decrypts hex ciphertext and returns UTF-8 text.
        """

        plaintext_bytes = self.decrypt_bytes(ciphertext_hex)

        return plaintext_bytes.decode("utf-8")


# ============================================================
# Demo / testing
# ============================================================

def demo_3des_single_block() -> None:
    print("=== Task 1: 3DES single block demo ===")

    key1 = "133457799BBCDFF1"
    key2 = "0123456789ABCDEF"
    key3 = "AABB09182736CCDD"

    plaintext_hex = "0123456789ABCDEF"

    des3 = DES3Cipher(key1, key2, key3)

    ciphertext_hex = des3.encrypt_hex_block(plaintext_hex)
    decrypted_hex = des3.decrypt_hex_block(ciphertext_hex)

    print(f"Plaintext hex:  {plaintext_hex}")
    print(f"Ciphertext hex: {ciphertext_hex}")
    print(f"Decrypted hex:  {decrypted_hex}")

    if decrypted_hex == plaintext_hex:
        print("3DES block test: SUCCESS")
    else:
        print("3DES block test: FAILED")

    print()


def demo_3des_cbc_any_length_text() -> None:
    print("=== Task 2: 3DES-CBC any length text demo ===")

    key1 = "133457799BBCDFF1"
    key2 = "0123456789ABCDEF"
    key3 = "AABB09182736CCDD"

    # Fixed IV for reproducible lab output.
    # In real use, the IV should be random and unique for each encryption.
    iv = "0001020304050607"

    plaintext = (
        "This is a 3DES CBC mode assignment. "
        "The plaintext may have any length."
    )

    cbc = DES3CBCMode(key1, key2, key3, iv)

    ciphertext_hex = cbc.encrypt_text(plaintext)
    decrypted_text = cbc.decrypt_text(ciphertext_hex)

    print(f"Plaintext:      {plaintext}")
    print(f"Ciphertext hex: {ciphertext_hex}")
    print(f"Decrypted text: {decrypted_text}")

    if decrypted_text == plaintext:
        print("3DES-CBC test: SUCCESS")
    else:
        print("3DES-CBC test: FAILED")

    print()


def main() -> None:
    demo_3des_single_block()
    demo_3des_cbc_any_length_text()


if __name__ == "__main__":
    main()