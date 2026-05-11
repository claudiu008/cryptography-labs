# 2D Vigenere Cipher - Homework

## What this project does

This homework implements a 2D version of the Vigenere cipher.

In the normal Vigenere cipher, the key is a string, for example:

```text
dog

The key is repeated over the plaintext and each letter is shifted using the corresponding key letter.

In this homework, the key is a small matrix of letters, for example:

k e y
m a t
r i x

The plaintext is also placed in a matrix with a fixed number of columns.
If the last row is not complete, it is filled with the letter z.

Example of plaintext matrix

If the plaintext is:

dog

and the number of columns is:

4

then the plaintext matrix becomes:

d o g z

The last z is added only as padding.

How the key is used

The key matrix is repeated over the plaintext matrix.

Example key matrix:

c a
t d

Plaintext matrix:

d o g z

The first row of the key is repeated over the plaintext row:

c a c a

So the encryption is:

d + c = f
o + a = o
g + c = i
z + a = z

The ciphertext is:

foiz
Encryption

The program uses the alphabet:

a = 0, b = 1, c = 2, ..., z = 25

Encryption formula:

cipher = (plaintext + key) mod 26

Example:

d = 3
c = 2

3 + 2 = 5
5 = f

So:

d + c = f
Decryption

Decryption is the reverse operation.

Formula:

plaintext = (ciphertext - key) mod 26

Example:

f = 5
c = 2

5 - 2 = 3
3 = d

So:

f - c = d

If the result is negative, modulo 26 brings it back inside the alphabet.

Main class

The main class is:

Vigenere2D

It has:

__init__(self, key_matrix, columns)

This initializes:

the key matrix;
the number of columns used for the plaintext matrix.

Other important methods are:

text_to_matrix(self, text)

This transforms the plaintext into a matrix and adds z padding if needed.

matrix_to_text(self, matrix)

This transforms a matrix back into a string.

get_key_letter(self, row_index, column_index)

This returns the correct key letter for a position in the plaintext matrix.

encrypt(self, plaintext)

This encrypts the plaintext.

decrypt(self, ciphertext)

This decrypts the ciphertext.

split_ciphertext_by_key_position(self, ciphertext)

This is used for the attack. It groups ciphertext letters depending on which key matrix position encrypted them.

Attack idea

The attack is based on the same idea as the attack on the normal Vigenere cipher.

In Vigenere, letters encrypted with the same key letter can be grouped together.
Each group behaves like a Caesar cipher.

The same happens here, but in 2D.

For example, with this key matrix:

k e y
m a t
r i x

all ciphertext letters encrypted with k are placed in one group.
All ciphertext letters encrypted with e are placed in another group.
All ciphertext letters encrypted with y are placed in another group, and so on.

Then each group can be attacked like a Caesar cipher.

Simple attack

The simple attack does this:

split ciphertext into groups based on key matrix position;
try all Caesar shifts from 0 to 25 for each group;
score the result using English letter frequency;
choose the best key letter for each group;
rebuild the key matrix.

This works sometimes, but it can also fail.

The problem is that some groups are short, so the letter frequency is not always reliable.

In my test, the simple attack did not always recover the full key matrix correctly.

Improved attack with combinations

To improve the attack, I used a second method.

Instead of keeping only the best key for each group, the program keeps several good candidates.

For example, with:

top_count = 4

the program keeps the best 4 possible key letters for every key position.

Then it tries combinations of those candidates.

For each possible key matrix:

decrypt the whole ciphertext;
score the full plaintext;
keep the key matrix that gives the best plaintext.

This works better because the final decision is made using the whole decrypted message, not only small separated groups.

What is the score?

The score is used to decide if a decrypted text looks like English.

The program uses letter frequency.
For example, in English, letters like:

e, t, a, o, i, n

appear often.

Letters like:

q, x, z, j

appear rarely.

The program uses a chi-square style score.

In simple words:

small score = more similar to English
large score = less similar to English

For the full plaintext attack, I also added common English patterns like:

the, this, ing, and, for

This helps the program choose a better final key matrix.

Demo used in main

The demo uses this key matrix:

k e y
m a t
r i x

and:

columns = 4

The program shows:

the original plaintext;
the plaintext matrix;
the ciphertext;
decryption using the known key;
simple attack;
improved attack with combinations.

Expected result:

Decryption successful: True
Combination attack successful: True

The decrypted text may end with extra z characters because the last row of the plaintext matrix is padded.

Limitations

The attack depends on statistical analysis, so it works better when the ciphertext is long.
If the ciphertext is short, the attack may fail because there is not enough text for good frequency analysis.
