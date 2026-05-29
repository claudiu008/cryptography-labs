3DES CBC Assignment

This assignment implements the 3DES block cipher and one mode of operation for encrypting plaintexts of any length.

The implementation uses the DES cipher developed in Lab 7. The DES block cipher works on 64-bit blocks. The class DES3Cipher combines three DES instances using the EDE construction:

Encryption:
C = E_K3(D_K2(E_K1(P)))

Decryption:
P = D_K1(E_K2(D_K3(C)))

The DES3Cipher class has:
1. an initializer that receives three 64-bit keys written as 16 hexadecimal digits each;
2. an encrypt method that encrypts one 64-bit block;
3. a decrypt method that decrypts one 64-bit block.

For plaintexts of any length, CBC mode was implemented.

CBC encryption:
C0 = IV
Ci = E_K(Pi XOR C(i-1))

CBC decryption:
Pi = D_K(Ci) XOR C(i-1)

Because DES and 3DES work on 8-byte blocks, PKCS#7 padding is used. If the plaintext is not a multiple of 8 bytes, padding bytes are added. If the plaintext is already a multiple of 8 bytes, a full padding block is added.

The encryption method returns the IV concatenated with the ciphertext in hexadecimal format:

IV || ciphertext

Files:
1. des3_cbc_assignment.py – implementation of DES3Cipher and DES3CBCMode.
2. README_3DES_CBC.txt – explanation of the work.
3. Lab_7/des_cipher.py – DES implementation used by this assignment.

How to run:
python .\Assignments\des3_cbc_assignment.py

Expected result:
3DES block test: SUCCESS
3DES-CBC test: SUCCESS

This implementation is educational. DES and 3DES should not be used for new real-world cryptographic systems.